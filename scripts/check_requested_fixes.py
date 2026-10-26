"""Qt smoke tests for confirmations, restart, ritual and packaged font glyphs."""
import os
from pathlib import Path
import sys
import tempfile
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QT_QUICK_BACKEND', 'software')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QRawFont
from PySide6.QtCore import QUrl, QObject, QCoreApplication, QEvent, Qt, QPointF
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QTest
from PySide6.QtQuick import QQuickWindow
from tabota.bridge import Bridge
from tabota.engine import Match
from tabota.content import ROOT
from tabota.storage import new_profile
app = QApplication([])
with tempfile.TemporaryDirectory() as directory:
    api = Bridge(directory)
    api.store.data['slots'][0] = new_profile()
    api.mission = 4
    api.begin_match()
    original = api.match.s['initialDecks']
    api.match.s['turn'] = 4
    api.match.s['mulligan'] = [True, True]
    api.match.s['flags']['ruleBriefingSeen'] = True
    api.refresh()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('api', api)
    warnings = []
    engine.warnings.connect(lambda messages: warnings.extend(m.toString() for m in messages))
    engine.load(QUrl.fromLocalFile(str(ROOT / 'tabota/ui/Main.qml')))
    window = engine.rootObjects()[0]
    QTest.qWait(700)
    assert api.options and not api.plan, 'Ritual must open automatically without choosing'
    panel = window.findChild(QObject, 'tabotaTargetPanel')
    def visual_items(item):
        for child in item.childItems():
            yield child
            yield from visual_items(child)
    option = next(i for i in visual_items(window.contentItem()) if i.objectName() == 'tabotaTargetOption')
    QTest.mouseClick(window, Qt.LeftButton, pos=option.mapToScene(QPointF(25, 25)).toPoint())
    assert panel.property('selectedOption') == 0
    assert not api.plan, 'Selecting is not confirming'
    confirm = window.findChild(QObject, 'tabotaConfirmTarget')
    QTest.mouseClick(window, Qt.LeftButton, pos=confirm.mapToScene(QPointF(80, 18)).toPoint())
    assert len(api.plan) == 1
    api.restartMatch()
    api.confirm(False)
    assert api.match.s['turn'] == 4 and api.plan
    api.restartMatch()
    api.confirm(True)
    assert api.match.s['turn'] == 1 and not api.plan and not api.options
    assert api.match.s['initialDecks'] == original
    api.acknowledgeRule()
    api.exchange()
    QTest.qWait(400)
    hand = next(i for i in visual_items(window.contentItem()) if i.objectName() == 'tabotaHandCard')
    dialog = window.findChild(QObject, 'tabotaDetailDialog')
    detail_panel = window.findChild(QObject, 'tabotaDetailPanel')
    for width, height in [(1440, 900), (960, 600)]:
        window.resize(width, height)
        QTest.qWait(200)
        focus_before = window.activeFocusItem()
        QTest.mouseMove(window, hand.mapToScene(QPointF(45, 120)).toPoint())
        QTest.qWait(300)
        assert dialog.property('open') and not dialog.isEnabled()
        assert not api.detail and not api.plan, 'Hover preview must stay local and non-modal'
        assert window.activeFocusItem() == focus_before, 'Preview must not steal focus'
        center = detail_panel.mapToScene(QPointF(detail_panel.width()/2, detail_panel.height()/2))
        assert abs(center.x() - width / 2) < 1 and abs(center.y() - height / 2) < 1
        assert detail_panel.width() == 800 and detail_panel.height() == 520
        QTest.mouseMove(window, hand.mapToScene(QPointF(45, 20)).toPoint())
        QTest.qWait(200)
        assert not dialog.property('open'), 'Leaving only the details region must hide preview'
    window.resize(1440, 900)
    QTest.qWait(200)
    QTest.mouseMove(window, hand.mapToScene(QPointF(45, 120)).toPoint())
    QTest.qWait(300)
    assert dialog.property('open'), 'Preview must reopen on each hover'
    window.grabWindow().save(str(ROOT / 'test-artifacts/quick-details.png'))
    QTest.mouseMove(window, QPointF(1420, 880).toPoint())
    QTest.qWait(200)
    assert not dialog.property('open')
    api.match.s['turn'] = 4
    api.ritual('clip')
    assert len(api.options) == 1 and not api.plan, 'Even a sole ritual requires confirmation'
    api.cancelOptions()
    api.mission = 3
    api.match = Match(3)
    api.match.s['mulligan'] = [True, True]
    for owner in (0, 1):
        api.match.s['board'][owner][0].append(api.match.new_unit('30', owner, 0))
    api.refresh()
    QTest.qWait(500)
    roles = set()
    for badge in visual_items(window.contentItem()):
        if badge.objectName() != 'tabotaNameRuleBadge' or not badge.isVisible(): continue
        card = badge.parentItem().parentItem()
        placed = card.property('onTable')
        roles.add(placed)
        assert badge.property('y') == (23 if placed else -8)
    assert roles == {True, False}, 'Check badges on both the table and the hand'
    window.grabWindow().save(str(ROOT / 'test-artifacts/restored-badges.png'))
    font = QRawFont(str(ROOT / 'tabota/ui/fonts/NotoSansSymbols2-Regular.ttf'), 20)
    assert font.supportsCharacter(0x26a1) and font.supportsCharacter(0x2726)
    QTest.qWait(250)
    assert not warnings, '\n'.join(warnings)
    window.hide()
    window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
print('Qt: automatic ritual, staged selection, restart/cancel and icon glyphs OK')
