import tempfile
import unittest
from tabota.bridge import Bridge
from tabota.content import CARDS, ENCOUNTERS, encounter_rule
from tabota.engine import Match


class EncounterAuditTests(unittest.TestCase):
    def test_every_variant_is_used_in_bridge(self):
        with tempfile.TemporaryDirectory() as directory:
            api = Bridge(directory)
            for mission in range(1, 21):
                for hard in (False, True):
                    api.mission, api.hard = mission, hard
                    api.match = Match(mission, hard)
                    api.refresh()
                    text = api.state["encounter"]["activeRule"]
                    self.assertEqual(text, encounter_rule(mission, hard))
                    self.assertTrue(text.startswith(ENCOUNTERS[mission-1]["ruleName"] + ":"))
            api.mission, api.hard = 10, True
            api.match = Match(10, True)
            api.refresh()
            rule = api.state["encounter"]["activeRule"]
            self.assertIn("ZAPLECZU", rule)
            self.assertNotIn("STREAM", rule)

    def test_name_badges_follow_public_gumbox_without_leaking_enemy_hand(self):
        with tempfile.TemporaryDirectory() as directory:
            api = Bridge(directory)
            for mission in range(1, 21):
                api.match = m = Match(mission)
                m.s["hand"] = [[], []]
                self.assertEqual(bool(api.card("10")["nameRuleBadge"]), mission == 3)
                m.s["hand"][1].append(m.new_unit("30", 1))
                self.assertEqual(bool(api.card("10")["nameRuleBadge"]), mission == 3)
                m.units(1, 0).append(m.new_unit("30", 1, 0))
                self.assertEqual(api.card("10")["nameRuleBadge"], "BEZ A")
                self.assertEqual(api.card("02")["nameRuleBadge"], "A")
                self.assertEqual(api.card("T3")["nameRuleBadge"], "A")
                self.assertEqual(api.card("E04")["nameRuleBadge"], "")
                m.units(1, 0)[0]["silenced"] = True
                self.assertEqual(bool(api.card("10")["nameRuleBadge"]), mission == 3)

    def test_banned_or_targetless_ritual_is_disabled_in_ui(self):
        with tempfile.TemporaryDirectory() as directory:
            api = Bridge(directory)
            api.match = Match(17, True)
            api.match.s["turn"] = 4
            api.match.units(1, 0).append(api.match.new_unit("04", 1, 0))
            api.refresh()
            self.assertEqual(api.battleBoard["ritualKinds"], ["hymn", "clip"])
            api.match.s["hard"] = False
            api.refresh()
            self.assertIn("ban", api.battleBoard["ritualKinds"])
            api.match.units(1, 0).clear()
            api.refresh()
            self.assertNotIn("ban", api.battleBoard["ritualKinds"])


if __name__ == "__main__": unittest.main()
