"""Drag/drop regression checks, including a Bridge test without an installed Qt.

These tests do not claim to measure the rendered frame rate. The runtime
smoke test in scripts/check_drag.py should be run with PySide6 on the target PC.
"""
from pathlib import Path
import importlib
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]


def fake_qt():
    qt = types.ModuleType('PySide6')
    core = types.ModuleType('PySide6.QtCore')
    widgets = types.ModuleType('PySide6.QtWidgets')

    class DummySignal:
        def __init__(self, *args):
            self.calls = []
            self.receivers = []

        def connect(self, callback):
            self.receivers.append(callback)

        def emit(self, *args):
            self.calls.append(args)
            for receiver in self.receivers:
                receiver(*args)

    class QObject:
        def __init__(self, *args, **kwargs):
            pass

    class QTimer:
        def __init__(self, *args):
            self.timeout = DummySignal()
            self.running = False
            self.interval = 0

        def setSingleShot(self, value):
            pass

        def setInterval(self, value):
            self.interval = value

        def start(self, *args):
            self.running = True

        def stop(self):
            self.running = False

        def isActive(self):
            return self.running

    class QUrl:
        def __init__(self, value):
            self.value = value

        @classmethod
        def fromLocalFile(cls, value):
            return cls('file://' + value)

        def toString(self):
            return self.value

    def Slot(*types):
        return lambda f: f

    def Property(*args, **kwargs):
        return lambda f: property(f)

    core.QObject = QObject
    core.QTimer = QTimer
    core.QUrl = QUrl
    core.QRunnable = QObject
    core.QThreadPool = QObject
    core.Signal = DummySignal
    core.Slot = Slot
    core.Property = Property
    widgets.QFileDialog = type('QFileDialog', (), {})
    qt.QtCore = core
    qt.QtWidgets = widgets
    return {'PySide6': qt, 'PySide6.QtCore': core, 'PySide6.QtWidgets': widgets}


class DragOptimizationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.battle = (BASE/'tabota/ui/Battle.qml').read_text(encoding='utf-8')
        cls.card = (BASE/'tabota/ui/Card.qml').read_text(encoding='utf-8')
        cls.bridge = (BASE/'tabota/bridge.py').read_text(encoding='utf-8')

    def test_motion_uses_local_coordinates_and_one_card(self):
        self.assertIn('dragCoordinateSpace: table', self.battle)
        self.assertIn('mouse.mapToItem(card.dragCoordinateSpace || card', self.card)
        self.assertIn('table.mapFromItem(handCard, 0, 0)', self.battle)
        self.assertIn('table.dragX - table.dragOffsetX', self.battle)
        self.assertIn('table.dragY - table.dragOffsetY', self.battle)
        self.assertEqual(self.battle.count('ParentChange { target: handCard; parent: table }'), 1)
        self.assertNotIn('api.selectCard(handSlot.handInfo.uid)\n                            table.dragUid', self.battle)

    def test_pointer_move_does_not_call_python_and_drop_is_deferred(self):
        self.assertIn('onDragMoved: (localX, localY) => table.trackDrag(localX, localY)', self.battle)
        move = self.battle.split('function trackDrag(localX, localY)')[1].split('function dropLane')[0]
        self.assertNotIn('api.', move)
        self.assertIn('Qt.callLater(function() { api.dropCard(uid, lane) })', self.battle)
        self.assertIn('const lane = table.dropLane(localX, localY)', self.battle)
        self.assertIn('table.dragLegalLanes = handSlot.handInfo.legalLanes || []', self.battle)

    def test_drop_avoids_full_refresh_and_sync_disk_write(self):
        start = self.bridge.index('    def chooseOption(')
        end = self.bridge.index('    @Slot(str)\n    def ritual', start)
        body = self.bridge[start:end]
        self.assertIn('self.schedule_save()', body)
        self.assertIn('self.refresh_battle(projected)', body)
        self.assertNotIn('self.safe_save()', body)
        self.assertNotIn('self.refresh()', body)
        self.assertIn('self.save_timer.setSingleShot(True)', self.bridge)

    def test_bridge_can_drop_a_legal_card_in_one_action(self):
        # The bridge is mostly pure Python; emulate just the Qt signal/timer
        # boundary so behavioral tests work on computers without PySide6.
        original_bridge = sys.modules.pop('tabota.bridge', None)
        try:
            with patch.dict(sys.modules, fake_qt()):
                bridge_module = importlib.import_module('tabota.bridge')
                from tabota.content import ENCOUNTERS
                from tabota.storage import new_profile
                with tempfile.TemporaryDirectory() as tmp:
                    api = bridge_module.Bridge(tmp)
                    api.store.data['slots'][0] = new_profile('Drop QA')
                    api.mission = 1
                    api.begin_match(tutorial=True)
                    before = len(api.plan)
                    step = api.match.tutorial_move()
                    uid, lane = step['uid'], step['lane']
                    # Wrong card/lane never causes a valid action in tutorial.
                    api.dropCard('u999999', lane)
                    self.assertEqual(len(api.plan), before)
                    api.dropCard(uid, (lane + 1) % 3)
                    self.assertEqual(len(api.plan), before)
                    api.notice = ''
                    api.dropCard(uid, lane)
                    self.assertEqual(len(api.plan), before + 1)
                    self.assertEqual(api.plan[-1]['uid'], uid)
                    self.assertEqual(api.plan[-1]['lane'], lane)
                    self.assertFalse(api.options)
                    self.assertTrue(api.save_timer.running)
                    # Pressing undo or submitting/quit can force the last plan to disk.
                    api.safe_save()
                    self.assertFalse(api.save_timer.running)
                    api.loadSlot(0)
                    self.assertEqual(len(api.plan), before + 1)
        finally:
            sys.modules.pop('tabota.bridge', None)
            if original_bridge is not None:
                sys.modules['tabota.bridge'] = original_bridge


if __name__ == '__main__':
    unittest.main()
