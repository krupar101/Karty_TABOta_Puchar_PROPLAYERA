"""Render Macko's real protection status from a story replay at two window sizes."""
import json
import os
from pathlib import Path
import sys
import tempfile
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('QT_QUICK_BACKEND', 'software')
os.environ.setdefault('QT_QUICK_CONTROLS_STYLE', 'Basic')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QUrl, QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from tabota.bridge import Bridge
from tabota.content import ROOT
from tabota.engine import Match
from tabota.storage import new_profile
from scripts.audit_campaign import play


def descendants(item):
    for child in item.childItems():
        yield child
        yield from descendants(child)


def protected_state():
    for seed in range(500000, 500100):
        trace, _ = play(5, seed)
        m = Match(5, seed=seed)
        m.mulligan(0, trace['exchange'])
        m.mulligan(1, [])
        for turn in trace['turns']:
            m.commit(turn['plans'])
            for uid in turn['discards']:
                m.discard_choice(uid)
            if any(u['card'] == '18' and u['protected'] for u in m.units(1)):
                return m
    raise AssertionError('No protected Macko found in story games')


app = QApplication([])
with tempfile.TemporaryDirectory(prefix='tabota-protection-') as directory:
    api = Bridge(directory)
    api.store.data['slots'][0] = new_profile()
    api.store.settings['reduced'] = True
    api.mission = 5
    api.match = protected_state()
    api.match.s['flags']['ruleBriefingSeen'] = True
    api.screen = 'battle'
    api.refresh()
    engine = QQmlApplicationEngine()
    warnings = []
    engine.warnings.connect(lambda entries: warnings.extend(e.toString() for e in entries))
    engine.rootContext().setContextProperty('api', api)
    engine.load(QUrl.fromLocalFile(str(ROOT / 'tabota/ui/Main.qml')))
    window = engine.rootObjects()[0]
    output = ROOT / 'test-artifacts'
    output.mkdir(exist_ok=True)
    for width, height in [(1280, 720), (960, 600)]:
        window.resize(width, height)
        QTest.qWait(500)
        badges = [i for i in descendants(window.contentItem())
                  if i.objectName() == 'tabotaProtectionBadge' and i.isVisible()]
        assert badges
        for badge in badges:
            texts = [c for c in badge.childItems() if c.property('text') == 'OCHRONA']
            assert texts and texts[0].property('contentWidth') <= badge.width()
            assert badge.y() >= 24  # Below the energy and name-rule rail.
        assert window.grabWindow().save(str(output / f'protection-{width}.png'))
    assert not warnings, '\n'.join(warnings)
    window.hide()
    window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
    engine.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
print('PASS: protected Macko in story duel 05; readable badges at 1280x720 and 960x600; no QML warnings')
