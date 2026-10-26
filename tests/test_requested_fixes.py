import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tabota.engine import Match, campaign_difficulty
from tabota.storage import data_directory, validate_match


class RequestedFixesTests(unittest.TestCase):
    def test_hymn_scores_empty_lane_and_records_source(self):
        m = Match(4)
        m.s['turn'] = 4
        m.apply(0, dict(special='hymn', lane=2, targets=[]))
        self.assertEqual(m.units(0, 2), [])
        self.assertEqual(m.scores()[0][2], 3)
        self.assertEqual(m.s['flags']['pointSources']['0:2'], ['Rytuał Hymn: +3'])
        restored = Match.restore(m.s)
        self.assertEqual(restored.scores(), m.scores())
        validate_match(restored.s)

    def test_campaign_curve_does_not_override_free_or_hard(self):
        self.assertEqual([campaign_difficulty(n) for n in (1, 5, 6, 10, 11, 15, 16, 20)],
                         ['beginner', 'beginner', 'casual', 'casual', 'easy', 'easy', 'normal', 'normal'])
        self.assertEqual(campaign_difficulty(1, hard=True), 'hard')
        self.assertEqual(campaign_difficulty(1, free=True), 'normal')
        self.assertEqual(campaign_difficulty(1, selected='easy'), 'easy')

    def test_migrate_legacy_data_once_without_destroying_it(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'XDG_DATA_HOME': directory}, clear=True), patch('tabota.storage.sys.platform', 'linux'):
            old = Path(directory) / 'tabota'
            old.mkdir()
            (old / 'campaign.json').write_text('legacy')
            new = data_directory()
            self.assertEqual(new.name, 'Tabot')
            self.assertEqual((new / 'campaign.json').read_text(), 'legacy')
            (new / 'campaign.json').write_text('new')
            self.assertEqual(data_directory(), new)
            self.assertEqual((new / 'campaign.json').read_text(), 'new')
            self.assertEqual((old / 'campaign.json').read_text(), 'legacy')

    def test_initial_decks_survive_roundtrip_and_are_validated(self):
        m = Match(6)
        original = m.s['initialDecks']
        m.s['deck'][0].pop()
        self.assertEqual(Match.restore(m.s).s['initialDecks'], original)
        m.s['initialDecks'] = [['not a card'], []]
        with self.assertRaises(ValueError): validate_match(m.s)
