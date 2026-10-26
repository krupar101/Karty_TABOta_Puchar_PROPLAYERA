"""End-to-end mouse/keyboard tutorial, save/resume, draft and fortune checks."""
import os
from pathlib import Path
import sys
import tempfile
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PySide6.QtCore import QPoint, QPointF, Qt, QUrl, QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlExpression, qmlContext
from PySide6.QtQuick import QQuickItem, QQuickWindow
from PySide6.QtTest import QTest
from tabota.bridge import Bridge
from tabota.content import ROOT
from tabota.storage import Storage

app=QApplication([])
temp=tempfile.TemporaryDirectory(prefix="tabota-interaction-")
api=Bridge(temp.name)
api.store.settings["reduced"]=True
engine=QQmlApplicationEngine()
warnings=[]
exceptions=[]
def report_exception(kind, value, tb):
    exceptions.append(str(value))
    sys.__excepthook__(kind, value, tb)
sys.excepthook = report_exception
sounds = []
api.soundRequested.connect(sounds.append)
engine.warnings.connect(lambda ws: warnings.extend(w.toString() for w in ws))
engine.rootContext().setContextProperty("api",api)
engine.load(QUrl.fromLocalFile(str(ROOT/"tabota/ui/Main.qml")))
assert engine.rootObjects(), "Window failed to load"
window=engine.rootObjects()[0]
QTest.qWait(150)


def descendants(item):
    for child in item.childItems():
        yield child
        yield from descendants(child)


def click_button(text):
    deadline = time.monotonic() + 3
    while True:
        candidates=[i for i in descendants(window.contentItem()) if i.isVisible() and i.isEnabled() and i.property("text")==text and i.property("down") is not None]
        if candidates or time.monotonic() >= deadline: break
        QTest.qWait(30)
    assert candidates, f"Button missing: {text}"
    button=candidates[0]
    point=button.mapToScene(QPointF(button.width()/2,button.height()/2))
    QTest.mouseClick(window,Qt.LeftButton,Qt.NoModifier,QPoint(round(point.x()),round(point.y())))
    QTest.qWait(100)  # Exit and entrance fades (reduced motion mode).


click_button("ROZPOCZNIJ PUCHAR     →")
assert api.screen=="slots"
click_button("Rozpocznij")
assert api.screen=="intro"
click_button("Zacznij naukę")
assert api.screen=="battle" and api.match.s["tutorial"]
script=[[("06",0)],[("04",1)],[("10",2)],[("41",0),("E01",0),("31",2)],[("10",1),("04",2)],[("01",0)]]
for turn,moves in enumerate(script,1):
    for cid,lane in moves:
        deadline = time.monotonic() + 3
        loader = next(c for c in descendants(window.contentItem()) if c.objectName() == "tabotaScreenLoader")
        while not loader.isEnabled() and time.monotonic() < deadline: QTest.qWait(30)
        hand=api.match.s["hand"][0]
        index=next(i for i,u in enumerate(hand) if u["card"]==cid and not any(a.get("uid")==u["uid"] for a in api.plan))
        card = next(c for c in descendants(window.contentItem()) if c.objectName() == "tabotaHandCard" and c.property("info")["uid"] == hand[index]["uid"])
        point = card.mapToScene(QPointF(card.width()*.4, card.height()*.25))
        QTest.mouseClick(window,Qt.LeftButton,Qt.NoModifier,QPoint(round(point.x()),round(point.y())))
        QTest.qWait(30)
        assert api.selected==hand[index]["uid"],(cid,api.selected, card.isEnabled(), loader.opacity(), api.notice)
        QTest.keyClick(window,[Qt.Key_1,Qt.Key_2,Qt.Key_3][lane])
        QTest.qWait(30)
        if api.options:
            choice=next((i for i,a in enumerate(api.options) if cid=="E01" and a["targets"] and api.match.project(0,api.plan).find(a["targets"][0])["card"]=="06"),0)
            QTest.qWait(80)
            view = next(c for c in descendants(window.contentItem()) if c.objectName() == "tabotaTargetOptionList")
            QQmlExpression(qmlContext(view), view, f"positionViewAtIndex({choice}, ListView.Beginning)").evaluate()
            QTest.qWait(40)
            tile = next(c for c in descendants(window.contentItem()) if c.objectName() == "tabotaTargetOption" and c.property("modelData")["index"] == choice)
            point = tile.mapToScene(QPointF(40,40))
            QTest.mouseClick(window,Qt.LeftButton,Qt.NoModifier,QPoint(round(point.x()),round(point.y())))
            QTest.qWait(80)
        assert api.plan, "Card was not planned"
    if turn==3:
        before=api.match.s.copy()
        plan=api.plan[:]
        api.navigate("menu")
        api.loadSlot(0)
        assert api.match.s==before and api.plan==plan
        QTest.qWait(30)
    click_button("Zakończ turę  →")
    deadline=time.monotonic()+10
    while api.busy and time.monotonic()<deadline:QTest.qWait(20)
    assert not api.busy, "Resolution stalled"
    assert not api.notice, api.notice
assert api.screen=="result"
assert api.match.scores()==[[15,10,13],[20,8,5]]
assert api.store.profile["completed"]==[1]
assert "08" in Storage(temp.name).profile["unlocked"]
click_button("Dalej  →")
assert api.screen=="map"
api.chooseMission(2)
QTest.qWait(40)
click_button("Rozpocznij pojedynek  →")
assert api.state["board"]["rulePending"]
click_button("Rozumiem · przejdź do wymiany kart  →")
assert not api.state["board"]["rulePending"]
assert api.state["board"]["mulligan"]
api.selectCard(api.match.s["hand"][0][0]["uid"])
assert api.state["board"]["exchangeCount"] == 1
click_button("Wymień 1 i zacznij")
assert api.match.s["mulligan"][0]
assert api.state["board"]["exchangeCount"] == 0
api.navigate("menu")
api.setting("veteran",True)
api.campaignMode(True,False)
api.chooseMission(1)
api.start(False)
api.confirm(True)  # Replace the saved ordinary match with this draft.
assert api.screen=="builder" and api.draft
assert len(api.offer)==24 and len(api.deck)==18
api.autoDeck()
assert not api.state["deckErrors"]
api.savePreset("Test draft")
api.dismiss()
api.start(False)
api.confirm(True)
assert api.screen=="battle" and api.match.s["hard"]
assert api.state["board"]["rulePending"]
api.acknowledgeRule()
api.navigate("fortune")
api.divine("  Zachowaj moje pytanie?  ",5,17)
order=api.reading["cards"][:]
api.reveal(0)
rid=api.reading["id"]
api.navigate("history")
api.openReading(rid)
assert api.reading["cards"]==order and api.reading["revealed"]==[0]
for i in range(1,5):api.reveal(i)
api.saveNote("Dokładnie ten sam układ.")
assert Storage(temp.name).tarot["readings"][0]["note"]=="Dokładnie ten sam układ."
api.inspect(order[0])
QTest.qWait(80)
assert api.state["detailTarot"]
api.closeDetail()
api.dismiss()
window.resize(1280,720)
QTest.qWait(150)
out=ROOT/"test-artifacts";out.mkdir(exist_ok=True)
window.grabWindow().save(str(out/"reading-1280x720.png"))
assert not warnings, "\n".join(warnings)
assert not exceptions, "\n".join(exceptions)
assert {"click", "select", "card", "shuffle", "turn", "win", "reveal"} <= set(sounds), sounds
print("PASS: mouse/keyboard tutorial, exact score, autosave/resume, rewards, explained mulligan, HARD draft, presets, fortune restore, 1280×720, zero QML warnings.")
# Destroy the QML scene before its context object.
for root_window in engine.rootObjects():
    root_window.hide()
    root_window.deleteLater()
QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
engine.deleteLater()
QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
temp.cleanup()
