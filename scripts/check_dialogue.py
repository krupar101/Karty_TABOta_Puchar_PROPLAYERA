"""Qt regression: opponent speech, header bounds and ten-second lifetime."""
from pathlib import Path
import os
import sys
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtCore import QCoreApplication, QEvent, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from tabota.bridge import Bridge
from tabota.content import ROOT
from tabota.storage import new_profile


def descendants(parent):
    for child in parent.childItems():
        yield child
        yield from descendants(child)


app = QApplication([])
with tempfile.TemporaryDirectory(prefix="tabota-fades-") as directory:
    api = Bridge(directory)
    engine = QQmlApplicationEngine()
    warnings = []
    engine.warnings.connect(lambda entries: warnings.extend(item.toString() for item in entries))
    engine.rootContext().setContextProperty("api", api)
    engine.load(QUrl.fromLocalFile(str(ROOT / "tabota/ui/Main.qml")))
    assert engine.rootObjects(), "QML failed to load"
    window = engine.rootObjects()[0]
    QTest.qWait(400)  # Initial state delivery can start the page's entry fade.

    def one(object_name):
        matches = [item for item in descendants(window.contentItem()) if item.objectName() == object_name]
        assert len(matches) == 1, f"Expected one {object_name}, got {len(matches)}"
        return matches[0]

    api.newGame(0, "Dialogue QA")
    api.mission = 2
    api.begin_match(False)
    QTest.qWait(500)
    bubble = one("tabotaOpponentSpeech")
    assert not bubble.isVisible(), "Opening dialogue must wait for the rule modal"
    api.acknowledgeRule()
    QTest.qWait(650)
    assert bubble.isVisible() and bubble.opacity() > .95
    assert bubble.y() + bubble.height() < 108, "Speech overlaps the board"
    assert bubble.x() + bubble.width() < 880, "Speech overlaps Pause"
    assert one("tabotaOpponentSpeechText").property("text") == api.dialogue
    window.grabWindow().save("/tmp/tabota-dialogue-review.png")

    api.dialogue = "Nowa wypowiedź rywala."
    api.refresh()
    QTest.qWait(5500)
    api.refresh()  # Unrelated updates must not reset the ten-second lifetime.
    QTest.qWait(4000)
    assert bubble.isVisible() and bubble.opacity() > .95
    # Allow scheduling jitter from the offscreen software renderer.
    QTest.qWait(1500)
    assert not bubble.isVisible(), "Speech did not disappear"
    assert one("tabotaOpponentSpeechText").property("text") == api.dialogue
    api.refresh()
    QTest.qWait(650)
    assert not bubble.isVisible(), "Old dialogue reappeared after a refresh"

    api.dialogue = "Kolejna kwestia."
    api.refresh()
    QTest.qWait(650)
    assert bubble.isVisible() and bubble.opacity() > .95
    api.dialogue = ""
    api.refresh()
    QTest.qWait(650)
    assert not bubble.isVisible(), "Empty speech should have no visible bubble"

    for root in engine.rootObjects():
        root.hide()
        root.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    assert not warnings, "QML warnings:\n" + "\n".join(warnings)
print("PASS: opponent speech placement, 10-second lifetime, fades, replacement and empty dialogue")
