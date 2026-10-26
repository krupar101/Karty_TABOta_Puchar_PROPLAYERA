"""Protect gameplay data while the story and tournament presentation evolve."""
import hashlib
import json
import unittest
from pathlib import Path

from tabota.content import CARDS, ENCOUNTERS, ACTS

ROOT = Path(__file__).resolve().parents[1]

class TournamentLoreTests(unittest.TestCase):
    def test_all_twenty_use_approved_decks_and_rewards(self):
        self.assertEqual(len(ENCOUNTERS), 20)
        self.assertEqual(len(CARDS), 79) # 52 units + 24 events + 3 tokens
        payload = [[e['storyDeck'], e['enemyDeck'], e['unlocks']] for e in ENCOUNTERS]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        # Four deliberate balance corrections, documented in docs/PLAYTEST.md.
        # IDs, rewards and card stats remain unchanged.
        self.assertEqual(digest, 'a9b9091bf80f4461af27549d86a5b15cc9ef2f41928f4e2d38fa4bfaf44e55a7')
        card_values = [[k,d['kind'],d['cost'],d['power'],d['tag'],d['description']] for k,d in sorted(CARDS.items())]
        digest = hashlib.sha256(json.dumps(card_values, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        # Description punctuation was normalized from the long dash to '-'; gameplay data is unchanged.
        self.assertEqual(digest, 'ea494646052ad7289617874ecaab8ef7fcd9bacdadd7b6ab94703e5b2c758e50')

    def test_tournament_story_dialogue_and_final_rule(self):
        self.assertIn('Puchar', (ROOT / 'Game_Design.md').read_text(encoding='utf-8'))
        self.assertEqual(len(ACTS), 4)
        self.assertEqual(len([e for e in ENCOUNTERS if len(e['dialogue']) == 6]), 20)
        self.assertIn('poczekalni', ENCOUNTERS[0]['story'])
        self.assertIn('Studio Finałowe', ENCOUNTERS[-1]['scene'])
        self.assertIn('NIC TU KURŁA NIE DZIAŁA', ENCOUNTERS[-1]['ruleName'])
        self.assertIn('t2 STREAM, t4 CZAT, t6 ZAPLECZE', ENCOUNTERS[-1]['rule'])
        self.assertIn('HARD', ENCOUNTERS[-1]['hardRule'])
        self.assertFalse(any('zombie Nysmo' in e['story'] for e in ENCOUNTERS))
        self.assertFalse(any('archiwum' in e['story'].lower() for e in ENCOUNTERS))

    def test_story_screen_and_campaign_have_new_labels(self):
        ui = ROOT / 'tabota' / 'ui'
        story = (ui / 'Story.qml').read_text(encoding='utf-8')
        menu = (ui / 'Menu.qml').read_text(encoding='utf-8')
        campaign = (ui / 'Campaign.qml').read_text(encoding='utf-8')
        self.assertIn('Złoty Taboret', story)
        self.assertIn('P U C H A R  P R O P L A Y E R A', menu)
        self.assertIn('pieczątek zwycięstwa', campaign)
        self.assertNotIn('0 potwierdzonych widzów', story)
        self.assertIn('text: ending ? (s.hard ?', story)

if __name__ == '__main__':
    unittest.main()
