"""Audit uses real hidden information, legal actions, and reproducible witnesses."""
import random
import unittest
from scripts.audit_campaign import play, replay, player_plan, invariants
from tabota.engine import Match


class StoryAuditTests(unittest.TestCase):
    def test_winning_witness_replays_without_simulator_policy(self):
        trace, _ = play(5, 500000)
        m = replay(trace)
        self.assertEqual(m.s['winner'], 0)
        self.assertFalse(m.s['hard'])
        self.assertEqual(len(trace['turns']), 6)

    def test_policy_cannot_read_enemy_hand_or_either_deck_order(self):
        m = Match(12, seed=1200000)
        hidden = m.clone(False)
        hidden.s['hand'][1] = []
        hidden.s['deck'] = [list(reversed(d)) for d in hidden.s['deck']]
        for seed in range(10):
            self.assertEqual(player_plan(m, random.Random(seed)),
                             player_plan(hidden, random.Random(seed)))

    def test_imperfect_plans_are_legal_and_really_differ(self):
        m = Match(5, seed=500001)
        alternatives = 0
        for seed in range(30):
            plan, different = player_plan(m, random.Random(seed))
            m.project(0, plan)
            alternatives += different
        self.assertGreater(alternatives, 0)

    def test_conservation_check_detects_missing_card(self):
        m = Match(1)
        m.s['hand'][0].pop()
        with self.assertRaises(AssertionError):
            invariants(m)

    def test_macko_self_protection_blocks_exactly_one_hostile_effect(self):
        m = Match(5, seed=500000)
        m.s['turn'] = 2
        m.s['energy'][1] = 2
        m.s['hand'][1] = [m.new_unit('18', 1)]
        uid = m.s['hand'][1][0]['uid']
        action = next(a for a in m.candidates(1, uid, 1) if a['targets'] == [uid])
        m.apply(1, action)
        unit = m.find(uid)
        self.assertTrue(unit['protected'])
        before = m.power(unit)
        m.buff(unit, -1, hostile=True)
        self.assertEqual(m.power(unit), before)
        self.assertFalse(unit['protected'])
        m.buff(unit, -1, hostile=True)
        self.assertEqual(m.power(unit), before-1)


if __name__ == '__main__':
    unittest.main()
