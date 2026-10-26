"""Qt smoke test: screen/page fades, modal exit, ordered briefing, card roles.

Run on the game machine, for example:
  QT_QPA_PLATFORM=offscreen python scripts/check_fades.py

Requires PySide6 and the project's Qt Quick dependencies. No audio device needed.
"""
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

    screen = one("tabotaScreenLoader")
    assert screen.opacity() > .9
    api.navigate("help")
    QTest.qWait(80)
    assert screen.opacity() < .95, "Outgoing page did not fade"
    QTest.qWait(400)
    assert screen.opacity() > .95 and screen.isVisible(), "Incoming page did not fade in"

    # A standalone detail dialog uses FadeBox, preserving its contents on close.
    api.inspect("01")
    detail = one("tabotaDetailDialog")
    QTest.qWait(240)
    assert detail.isVisible() and detail.opacity() > .95
    api.closeDetail()
    QTest.qWait(75)
    assert detail.opacity() < 1, "Detail dialog did not fade out"
    QTest.qWait(220)
    assert not detail.isVisible(), "Closed detail dialog must not catch input"

    api.store.data["slots"][0] = new_profile("Fade QA")
    api.mission = 2
    api.begin_match(False)
    QTest.qWait(410)
    rule = one("tabotaRuleWindow")
    exchange = one("tabotaExchangePanel")
    assert rule.isVisible() and rule.opacity() > .95
    assert not exchange.isVisible(), "Exchange overlapped the rule popup"
    api.acknowledgeRule()
    QTest.qWait(70)
    assert rule.isVisible() and not exchange.isVisible(), "Rule and exchange overlapped during fade out"
    QTest.qWait(360)
    assert not rule.isVisible() and exchange.isVisible() and exchange.opacity() > .95

    api.exchange()
    QTest.qWait(260)
    cards = [item for item in descendants(window.contentItem()) if item.objectName() == "tabotaHandCard"]
    assert cards
    first = cards[0]
    overlays = [item for item in descendants(first) if item.objectName() == "tabotaInspectAffordance"]
    assert len(overlays) == 1
    assert overlays[0].parentItem().objectName() == "tabotaCardMotion", "Affordance is not animated with the card"
    played = (ROOT / "tabota/ui/Battle.qml").read_text(encoding="utf-8")
    assert 'splitClickDetails: false; onClicked: api.inspect(info.id)' in played

    for root in engine.rootObjects():
        root.hide()
        root.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    assert not warnings, "QML warnings:\n" + "\n".join(warnings)
print("PASS: screen exit/entry fades, detail close, rule→exchange sequencing, card overlay parent, Qt warnings")
