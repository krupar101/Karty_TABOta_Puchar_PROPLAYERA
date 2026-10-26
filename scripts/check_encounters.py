"""Render all 40 rule variants, start modals and boards at two window sizes."""
import os
from pathlib import Path
import sys
import tempfile
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QObject, QUrl, QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlExpression, qmlContext
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from tabota.bridge import Bridge
from tabota.content import ROOT, ENCOUNTERS
from tabota.engine import Match, ai_plan
from tabota.storage import new_profile

app = QApplication([])
temporary = tempfile.TemporaryDirectory(prefix="tabota-encounters-")
api = Bridge(temporary.name)
api.store.data["slots"][0] = new_profile()
api.store.settings["reduced"] = True
engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("api", api)
warnings = []
engine.warnings.connect(lambda messages: warnings.extend(m.toString() for m in messages))
engine.load(QUrl.fromLocalFile(str(ROOT / "tabota/ui/Main.qml")))
window = engine.rootObjects()[0]
output = ROOT / "test-artifacts/encounters"
output.mkdir(parents=True, exist_ok=True)
captures = 0


def item(name):
    result = window.findChild(QObject, name)
    assert result is not None, name
    return result


def descendants(parent):
    for child in parent.childItems():
        yield child
        yield from descendants(child)


def capture(label, screen):
    global captures
    api.screen = screen
    api.refresh()
    deadline = time.monotonic() + 4
    loader = item("tabotaScreenLoader")
    expected = "Briefing.qml" if screen == "briefing" else "Battle.qml"
    while time.monotonic() < deadline:
        QTest.qWait(30)
        if loader.property("source").fileName() == expected and loader.property("opacity") >= .999:
            break
    assert loader.property("source").fileName() == expected, screen
    deadline = time.monotonic() + 4
    while True:
        pictures = [i for i in descendants(window.contentItem()) if
                    i.property("sourceSize") is not None and i.property("source")]
        statuses = [QQmlExpression(qmlContext(i), i, "Number(status)").evaluate()[0] for i in pictures]
        assert 3 not in statuses, "Image failed to load"
        if 2 not in statuses: break
        assert time.monotonic() < deadline, "Image loading timeout"
        QTest.qWait(30)
    QTest.qWait(30)  # Paint the decoded textures before grabbing the window.
    assert not warnings, "\n".join(warnings)
    if screen == "briefing":
        scroll, actions = item("tabotaBriefingScroll"), item("tabotaBriefingActions")
        assert scroll.property("y") + scroll.property("height") < actions.property("y")
        assert actions.property("y") + actions.property("height") <= 746
    else:
        controls, plan = item("tabotaRuleControls"), item("tabotaPlanList")
        assert controls.property("y") + controls.property("height") < plan.property("y")
        assert plan.property("y") + plan.property("height") <= 560
    assert window.grabWindow().save(str(output / f"{label}.png"))
    captures += 1


for width, height in [(1280, 720), (960, 600)]:
    window.resize(width, height)
    for hard in [False, True]:
        api.hard = hard
        for mission in range(1, 21):
            api.mission = mission
            api.match = Match(mission, hard, seed=mission*2030)
            api.plan = []
            api.dialogue = ENCOUNTERS[mission-1]["dialogue"]["START"]
            label = f"{width}-{mission:02}-{'hard' if hard else 'normal'}"
            capture(label + "-briefing", "briefing")
            api.match.s["flags"]["ruleBriefingSeen"] = False
            capture(label + "-rule", "battle")
            api.match.s["flags"]["ruleBriefingSeen"] = True
            capture(label + "-mulligan", "battle")
            for p in range(2): api.match.mulligan(p, [])
            for _ in range(3):
                api.match.commit([ai_plan(api.match, p, "easy") for p in range(2)])
                while api.match.s["choices"]:
                    p = api.match.s["choices"][0]["owner"]
                    api.match.discard_choice(api.match.s["hand"][p][0]["uid"])
            capture(label + "-turn4", "battle")
            if mission == 16:
                for _ in range(3): api.match.commit([[], []])
                capture(label + "-turn7", "battle")
            print("PASS", label, flush=True)

print(f"{captures} captures; no QML warnings; briefing and rule controls fit.")
window.hide()
window.deleteLater()
QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
engine.deleteLater()
QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
temporary.cleanup()
