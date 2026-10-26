"""Qt Quick smoke: one hand card, smooth detail affordance and clean teardown.

Run: QT_QPA_PLATFORM=offscreen python scripts/check_hover.py
This file requires a locally working PySide6/Qt installation.
"""
from pathlib import Path
import os
import sys
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtCore import QPoint, QPointF, Qt, QUrl, QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from tabota.bridge import Bridge
from tabota.content import ROOT
from tabota.storage import new_profile


def descendants(item):
    for child in item.childItems():
        yield child
        yield from descendants(child)


def point_for(card, relative_y):
    pt = card.mapToScene(QPointF(card.width() * .4, card.height() * relative_y))
    return QPoint(round(pt.x()), round(pt.y()))


app = QApplication([])
with tempfile.TemporaryDirectory(prefix="tabota-hover-") as temp:
    api = Bridge(temp)
    api.store.data["slots"][0] = new_profile("QA Hover")
    api.mission = 2
    api.begin_match(False)
    api.acknowledgeRule()
    api.exchange()
    assert api.screen == "battle" and not api.state["board"]["rulePending"]
    assert not api.state["board"]["mulligan"]

    engine = QQmlApplicationEngine()
    warnings = []
    engine.warnings.connect(lambda entries: warnings.extend(e.toString() for e in entries))
    engine.rootContext().setContextProperty("api", api)
    engine.load(QUrl.fromLocalFile(str(ROOT / "tabota/ui/Main.qml")))
    assert engine.rootObjects(), "QML root failed to load"
    window = engine.rootObjects()[0]
    QTest.qWait(250)

    def lookup(name):
        return [c for c in descendants(window.contentItem()) if c.objectName() == name]

    cards = lookup("tabotaHandCard")
    assert cards, "Hand is missing"
    card = cards[0]
    uid = card.property("info")["uid"]
    slot = card.parentItem()
    assert slot.objectName() == "tabotaHandSlot"

    QTest.mouseMove(window, point_for(card, .25))
    QTest.qWait(300)
    assert card.parentItem().objectName() == "tabotaBattleTable", "Hover card still inside clipped hand"
    assert len(lookup("tabotaHandCard")) == len(cards), "An independent hover Card was created"
    overlay = next(c for c in descendants(card) if c.objectName() == "tabotaInspectAffordance")
    assert overlay.isVisible() and overlay.opacity() > .85, "Details overlay must fade in even from the top"

    QTest.mouseMove(window, point_for(card, .75))
    QTest.qWait(220)
    assert overlay.opacity() > .85, "Overlay disappeared over the bottom half"
    QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, point_for(card, .75))
    QTest.qWait(100)
    assert api.state["detail"]["id"] == card.property("info")["id"], "Bottom click did not inspect"
    api.closeDetail()
    QTest.qWait(70)

    QTest.mouseMove(window, point_for(card, .25))
    QTest.qWait(100)
    QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, point_for(card, .25))
    QTest.qWait(100)
    assert api.selected == uid, "Upper click did not select"
    QTest.mouseMove(window, QPoint(10, 110))
    QTest.qWait(240)
    assert card.parentItem() == slot, "Card did not return to its original slot"
    assert overlay.opacity() < .15, "Details overlay did not fade out"

    for root_window in engine.rootObjects():
        root_window.hide()
        root_window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    assert not warnings, "QML warnings:\n" + "\n".join(warnings)
print("PASS: one reparented hover card, whole-card detail fade, split clicks, clean QML log")
