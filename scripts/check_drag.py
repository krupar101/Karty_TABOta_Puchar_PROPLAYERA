"""Real Qt Quick drag/drop smoke and latency probe.

Run on the game PC:
    QT_QPA_PLATFORM=offscreen python scripts/check_drag.py
or, for the usual GPU-backed window:
    python scripts/check_drag.py

Qt rendering time depends on the platform; this smoke test checks behavior,
not a stable FPS target. It logs wall-clock times of QtTest events.
"""
from pathlib import Path
import os
import sys
import tempfile
from time import perf_counter

os.environ.setdefault('QT_QUICK_CONTROLS_STYLE', 'Basic')
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


def to_point(item, x, y):
    p = item.mapToScene(QPointF(x, y))
    return QPoint(round(p.x()), round(p.y()))


app = QApplication([])
with tempfile.TemporaryDirectory(prefix='tabota-drag-') as temp:
    api = Bridge(temp)
    api.store.data['slots'][0] = new_profile('Drag QA')
    api.mission = 2
    api.begin_match(False)
    api.acknowledgeRule()
    api.exchange()
    assert api.match and api.screen == 'battle'

    engine = QQmlApplicationEngine()
    warnings = []
    engine.warnings.connect(lambda entries: warnings.extend(e.toString() for e in entries))
    engine.rootContext().setContextProperty('api', api)
    engine.load(QUrl.fromLocalFile(str(ROOT / 'tabota/ui/Main.qml')))
    assert engine.rootObjects(), 'Failed to load QML root'
    window = engine.rootObjects()[0]
    QTest.qWait(280)

    def find(name):
        matches = [c for c in descendants(window.contentItem()) if c.objectName() == name]
        assert matches, f'Missing QML item: {name}'
        return matches[0]

    table = find('tabotaBattleTable')
    cards = [c for c in descendants(window.contentItem()) if c.objectName() == 'tabotaHandCard']
    info = api.battleBoard
    choice = next((c for c in cards if any(c.property('info').get('legalLanes', [])) and c.property('info').get('kind') == 'unit'), None)
    assert choice is not None, 'No legal hand unit to drag'
    uid = choice.property('info')['uid']
    lane = next(i for i, ok in enumerate(choice.property('info')['legalLanes']) if ok)
    start = to_point(choice, choice.width() / 2, choice.height() * .25)
    dest = to_point(table, lane * 345 + 165, 380)

    QTest.mouseMove(window, start)
    QTest.qWait(180)
    # Reparenting on hover must not create a replacement card.
    assert choice.parentItem() == table
    elapsed = []
    t = perf_counter()
    QTest.mousePress(window, Qt.LeftButton, Qt.NoModifier, start)
    press_ms = (perf_counter() - t) * 1000
    t = perf_counter()
    for n in range(1, 17):
        x = start.x() + (dest.x() - start.x()) * n / 16
        y = start.y() + (dest.y() - start.y()) * n / 16
        move_start = perf_counter()
        QTest.mouseMove(window, QPoint(round(x), round(y)))
        elapsed.append((perf_counter() - move_start) * 1000)
    motion_ms = (perf_counter() - t) * 1000
    assert table.property('dragActive'), 'Drag was not initiated'
    assert api.selected == '', 'Mouse movement refreshed the Python selection'
    t = perf_counter()
    QTest.mouseRelease(window, Qt.LeftButton, Qt.NoModifier, dest)
    release_ms = (perf_counter() - t) * 1000
    QTest.qWait(130)
    assert not table.property('dragActive'), 'Drag remained active after releasing'
    assert api.plan or api.options, 'Dropping a legal card did not plan a move or request a target'
    assert not any('TypeError' in w or 'Unable to assign' in w for w in warnings), warnings

    print('OK drag/drop: press %.2f ms; moves %.2f ms total (max %.2f); release %.2f ms'
          % (press_ms, motion_ms, max(elapsed), release_ms))
    print('A QtTest smoke result is not an FPS measurement on the player GPU.')
    for root_window in engine.rootObjects():
        root_window.hide()
        root_window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
