"""OST routing, legacy audio preferences, UI policy and match-rule gating."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from tabota.music import MUSIC_DIR, soundtrack_for, soundtrack_path
from tabota.storage import Storage, SCHEMA

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'tabota/ui'


class MusicTests(unittest.TestCase):
    def test_every_screen_uses_intended_ost(self):
        cases = dict(menu='M01.mp3', slots='M01.mp3', settings='M01.mp3',
                     map='M02.mp3', briefing='M02.mp3', result='M02.mp3',
                     collection='M03.mp3', builder='M03.mp3',
                     fortune='M04.mp3', reading='M04.mp3', history='M04.mp3')
        for screen, filename in cases.items():
            self.assertEqual(soundtrack_for(screen), filename)
            self.assertTrue(soundtrack_path(screen).is_file(), filename)
        for i in range(1, 21):
            for screen in ('battle', 'pause'):
                self.assertEqual(soundtrack_for(screen, i), f'Stage{i:02}.mp3')
                self.assertTrue(soundtrack_path(screen, i).is_file())
        self.assertEqual(len(list(MUSIC_DIR.glob('*.mp3'))), 26)
        for s in ('X02.mp3', 'X03.mp3'):
            self.assertTrue((MUSIC_DIR / s).is_file())

    def test_audio_prefs_are_backwards_compatible(self):
        with tempfile.TemporaryDirectory() as dir:
            old = dict(schema=SCHEMA, reduced=False, sound=True, volume=.62,
                       fullscreen=False, veteran=False, autoReadings=True, contrast=False)
            (Path(dir)/'settings.json').write_text(json.dumps(old), encoding='utf-8')
            store=Storage(dir)
            self.assertEqual(store.settings['volume'], .62)
            self.assertEqual(store.settings['musicVolume'], .35)
            self.assertTrue(store.settings['music'])
            self.assertFalse(store.warnings)
            store.settings['musicVolume']=.23
            store.settings['music']=False
            store.write('settings.json',store.settings)
            again=Storage(dir)
            self.assertEqual(again.settings['musicVolume'], .23)
            self.assertFalse(again.settings['music'])
            for invalid in [-.1,1.1,'loud',None]:
                bad=dict(again.settings,musicVolume=invalid)
                with self.assertRaises(ValueError): again.check('settings.json', bad)

    def test_ui_obvious_affordances_and_layering(self):
        card = (UI/'Card.qml').read_text(encoding='utf-8')
        battle = (UI/'Battle.qml').read_text(encoding='utf-8')
        main = (UI/'Main.qml').read_text(encoding='utf-8')
        settings = (UI/'Settings.qml').read_text(encoding='utf-8')
        self.assertNotIn('LOKALNIE / OFFLINE', main)
        self.assertIn('property bool lowerHalfHovered:', card)
        self.assertIn('card.splitClickDetails && event.y >= card.height/2', card)
        self.assertIn('⌕  SZCZEGÓŁY', card)
        self.assertIn('ParentChange { target: handCard; parent: table }', battle)
        self.assertIn('when: !b.rulePending && (handCard.pointerHover', battle)
        self.assertNotIn('hoverUid', battle)
        self.assertNotIn('hoverInfo', battle)
        self.assertNotIn('detailPreview', battle)
        self.assertIn('opacity: card.lowerHalfHovered && !card.moving ? 1 : 0', card)
        self.assertIn('Behavior on opacity {', card)
        self.assertNotIn('visible: table.dragActive', battle)
        self.assertIn('table.dragX - table.dragOffsetX', battle)
        self.assertIn('open: b.mulligan && !b.rulePending && !ruleWindow.visible', battle)
        self.assertIn('open: !!b.rulePending; z: 400', battle)
        self.assertIn('onClicked: api.acknowledgeRule()', battle)
        self.assertIn('musicVolume', settings)
        self.assertIn('({key:"music",', settings)


@unittest.skipUnless(importlib.util.find_spec('PySide6'), 'Qt runtime unavailable in this environment')
class BridgeRuleTests(unittest.TestCase):
    def test_rule_first_then_mulligan_and_saved_dismissal(self):
        from tabota.bridge import Bridge
        from tabota.storage import new_profile
        with tempfile.TemporaryDirectory() as d:
            api=Bridge(d)
            api.store.data['slots'][0]=new_profile()
            api.begin_match(False)
            self.assertTrue(api.state['board']['rulePending'])
            self.assertTrue(api.state['board']['mulligan'])
            uid=api.match.s['hand'][0][0]['uid']
            api.selectCard(uid)
            api.exchange()
            self.assertEqual(api.mulligan_ids, [])
            self.assertFalse(api.match.s['mulligan'][0])
            api.acknowledgeRule()
            self.assertFalse(api.state['board']['rulePending'])
            resumed=Bridge(d)
            resumed.loadSlot(0)
            self.assertFalse(resumed.state['board']['rulePending'])
            self.assertTrue(resumed.state['board']['mulligan'])
            resumed.selectCard(uid)
            self.assertEqual(resumed.state['board']['exchangeCount'],1)


if __name__ == '__main__': unittest.main()
