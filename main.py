"""Run with python main.py. Packaging entry point for all three desktop systems."""
import argparse
import os
from pathlib import Path
import sys

from tabota import __version__


def main():
    parser = argparse.ArgumentParser(description="Karty TABOta: WSZYSCY DO BANA! - Puchar PROPLAYERA")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("--screenshot", help="Save a PNG screenshot then exit (for UI verification).")
    parser.add_argument("--screen", default="menu", choices=["menu", "map", "battle", "fortune", "reading", "collection", "builder", "settings", "briefing", "help", "journal", "slots", "intro", "history", "result", "ending", "pause"])
    parser.add_argument("--demo", action="store_true", help="Temporary in-memory content for screenshots; use an isolated TABOTA_DATA_DIR.")
    parser.add_argument("--software", action="store_true", help="Use Qt Quick's software renderer.")
    args = parser.parse_args()
    if args.software: os.environ["QT_QUICK_BACKEND"] = "software"
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    from PySide6.QtCore import QTimer, QUrl, QCoreApplication, QEvent
    from PySide6.QtGui import QIcon, QPalette, QColor, QFont, QFontDatabase
    from PySide6.QtWidgets import QApplication
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuick import QQuickWindow  # Register the concrete root-window wrapper.
    from tabota.content import ROOT
    from tabota.bridge import Bridge
    app = QApplication(sys.argv[:1])
    app.setApplicationName("Karty TABOta")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("TABOt")
    for font_file in (ROOT / "tabota/ui/fonts").glob("*.ttf"):
        QFontDatabase.addApplicationFont(str(font_file))
    font = QFont()
    font.setFamilies(["Noto Sans", "Noto Sans Symbols 2"])
    app.setFont(font)
    app.setWindowIcon(QIcon(str(ROOT/"ikona.png")))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#171122"))
    palette.setColor(QPalette.WindowText, QColor("#f8f2ff"))
    palette.setColor(QPalette.Base, QColor("#100b17"))
    palette.setColor(QPalette.Text, QColor("#f8f2ff"))
    palette.setColor(QPalette.Button, QColor("#30203d"))
    palette.setColor(QPalette.ButtonText, QColor("#f8f2ff"))
    palette.setColor(QPalette.Highlight, QColor("#a771d7"))
    palette.setColor(QPalette.PlaceholderText, QColor("#a99bb6"))
    app.setPalette(palette)
    bridge = Bridge()
    if args.demo:
        from tabota.storage import new_profile, make_reading
        from tabota.content import CARDS, ENCOUNTERS
        from tabota.engine import Match, ai_plan
        bridge.store.data["slots"][bridge.store.data["active"]] = new_profile("TaboRETRO")
        bridge.store.profile["unlocked"] = [c for c in CARDS if CARDS[c]["kind"] != "token"]
        bridge.store.profile["completed"] = list(range(1, 9))
        bridge.mission = 9
        bridge.match = Match(9, seed=2030)
        bridge.match.mulligan(0, [])
        bridge.match.mulligan(1, [])
        for _ in range(3):
            bridge.match.commit([ai_plan(bridge.match, 0), ai_plan(bridge.match, 1)])
            while bridge.match.s["choices"]:
                p = bridge.match.s["choices"][0]["owner"]
                bridge.match.discard_choice(bridge.match.s["hand"][p][0]["uid"])
        bridge.deck = ENCOUNTERS[0]["storyDeck"][:]
        bridge.reading = make_reading("Co dziś zasługuje na moją uwagę?", 5)
        bridge.reading["revealed"] = list(range(5))
        bridge.store.tarot["readings"] = [bridge.reading]
        bridge.dialogue = ENCOUNTERS[8]["dialogue"]["START"]
    bridge.screen = args.screen
    bridge.refresh()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("api", bridge)
    errors = []
    engine.warnings.connect(lambda warnings: errors.extend(str(w.toString()) for w in warnings))
    engine.load(QUrl.fromLocalFile(str(ROOT/"tabota/ui/Main.qml")))
    if not engine.rootObjects():
        return 1
    from tabota.cursor import GameCursor
    game_cursor = GameCursor(engine.rootObjects()[0])
    bridge.quitRequested.connect(app.quit)
    if not args.screenshot and not os.environ.get("TABOTA_NO_AUDIO"):
        from tabota.audio import Audio
        audio = Audio(bridge.store.settings)
        audio.music.spectrumChanged.connect(bridge.updateSpectrum)
        bridge.soundRequested.connect(audio.play)
        bridge.volumeChanged.connect(audio.apply_volumes)
        bridge.changed.connect(lambda: audio.sync(bridge.screen, bridge.mission))
        audio.sync(bridge.screen, bridge.mission)
    if args.screenshot:
        def capture():
            target = Path(args.screenshot)
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                ok = engine.rootObjects()[0].grabWindow().save(str(target))
            except Exception as exc:
                print(f"Screenshot failed: {exc}", file=sys.stderr)
                app.exit(2)
                return
            if errors:
                print("\n".join(errors), file=sys.stderr)
            app.exit(0 if ok and not errors else 2)
        QTimer.singleShot(1500, capture)
    result = app.exec()
    # Explicitly destroy the QML tree BEFORE releasing its `api` context object.
    # Otherwise live bindings in Main/Card/Menu access `api.state` after Qt has
    # nulled the context property (reproduces the exit-time TypeErrors in logs).
    for root_window in engine.rootObjects():
        root_window.hide()
        root_window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
