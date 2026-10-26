"""Opening-playability, collection secrecy and guided-to-independent tutorial."""
from pathlib import Path
import unittest
from collections import Counter

from tabota.content import CARDS, ENCOUNTERS, STARTER, validate_deck
from tabota.engine import Match, IllegalMove, ai_plan, auto_deck, draft_offer
from tabota.storage import new_profile, validate_profile


def opening_options(match, player=0):
    return [(u["uid"], lane) for u in match.s["hand"][player]
            for lane in range(3) if match.candidates(player, u["uid"], lane)]


class OpeningTests(unittest.TestCase):
    def test_all_story_and_enemy_hands_can_play_on_first_turn(self):
        for mission in range(1, 21):
            for seed in range(60):
                m = Match(mission=mission, seed=seed)
                for side in (0, 1):
                    self.assertTrue(opening_options(m, side), (mission, seed, side))
                    self.assertTrue(any(CARDS[u["card"]]["cost"] == 1 and
                                        CARDS[u["card"]]["kind"] == "unit"
                                        for u in m.s["hand"][side]), (mission, seed, side))

    def test_exchange_never_removes_all_first_turn_plays(self):
        for mission in (1, 5, 11, 20):
            for seed in range(36):
                for picks in [(0,), (1,), (0, 1), (2, 4)]:
                    m = Match(mission=mission, seed=seed)
                    ids = [m.s["hand"][0][index]["uid"] for index in picks]
                    m.mulligan(0, ids)
                    self.assertTrue(opening_options(m), (mission, seed, picks))
                    self.assertEqual(len(m.s["hand"][0]), 5)

    def test_one_cost_unit_required_in_custom_deck_and_draft(self):
        expensive = [cid for cid, d in CARDS.items() if d["kind"] == "unit" and d["cost"] > 1][:18]
        self.assertEqual(len(expensive), 18)
        self.assertTrue(any("⚡ 1" in error for error in validate_deck(expensive)))
        for seed in range(100):
            offer = draft_offer(STARTER, seed)
            self.assertTrue(any(CARDS[c]["kind"] == "unit" and CARDS[c]["cost"] == 1 for c in offer))
            deck = auto_deck(offer)
            self.assertFalse(validate_deck(deck, STARTER, offer))
            m = Match(seed=seed, decks=[deck, ENCOUNTERS[0]["enemyDeck"]])
            self.assertTrue(opening_options(m))

    def test_old_saved_presets_can_load_but_cannot_launch_until_fixed(self):
        legacy = [cid for cid, d in CARDS.items() if d["kind"] == "unit" and d["cost"] > 1][:18]
        p = new_profile("Stary zapis")
        p["unlocked"] = [cid for cid, d in CARDS.items() if d["kind"] != "token"]
        p["presets"] = [{"name": "Stary legalny preset", "cards": legacy}]
        validate_profile(p)  # Old save must remain readable, not discarded.
        self.assertTrue(validate_deck(p["presets"][0]["cards"], p["unlocked"]))
        with self.assertRaises(ValueError):
            Match(decks=[legacy, ENCOUNTERS[0]["enemyDeck"]])

    def test_seed_replays_same_guaranteed_opening(self):
        for seed in range(30):
            a, b = Match(mission=11, seed=seed), Match(mission=11, seed=seed)
            self.assertEqual(a.s, b.s)
            chosen = [u["uid"] for u in a.s["hand"][0]][:2]
            a.mulligan(0, chosen)
            b.mulligan(0, chosen)
            self.assertEqual(a.s, b.s)


class TutorialTests(unittest.TestCase):
    def test_exact_moves_only_in_first_three_turns(self):
        m = Match(tutorial=True)
        required = [("06", 0), ("04", 1), ("10", 2)]
        for cid, lane in required:
            lesson = m.tutorial_move()
            self.assertEqual((lesson["card"], lesson["lane"]), (cid, lane))
            correct = next(u for u in m.s["hand"][0] if u["card"] == cid)
            wrong = next(u for u in m.s["hand"][0] if u["uid"] != correct["uid"])
            self.assertEqual(m.candidates(0, wrong["uid"], lane), [])
            self.assertEqual(m.candidates(0, correct["uid"], (lane+1)%3), [])
            actions = m.candidates(0, correct["uid"], lane)
            self.assertEqual(len(actions), 1)
            self.assertEqual(len(opening_options(m)), 1)
            with self.assertRaises(IllegalMove):
                m.commit([[], ai_plan(m)])
            with self.assertRaises(IllegalMove):
                m.commit([[dict(actions[0], lane=(lane+1)%3)], ai_plan(m)])
            m.commit([[actions[0]], ai_plan(m)])
        self.assertEqual(m.s["turn"], 4)
        self.assertIsNone(m.tutorial_move())
        # The student is on their own: skipping a turn or choosing another
        # affordable action is now legal; the enemy continues its scripted play.
        m.commit([[], ai_plan(m)])
        self.assertEqual(m.s["turn"], 5)

    def test_tutorial_saved_snapshot_preserves_guided_step(self):
        m = Match(tutorial=True)
        lesson = m.tutorial_move()
        restored = Match.restore(m.s)
        self.assertEqual(lesson, restored.tutorial_move())
        self.assertEqual(opening_options(m), opening_options(restored))


class UiContracts(unittest.TestCase):
    def test_dragged_original_card_renders_outside_clipped_hand(self):
        ui = Path(__file__).resolve().parents[1] / "tabota" / "ui"
        battle = (ui / "Battle.qml").read_text(encoding="utf-8")
        card = (ui / "Card.qml").read_text(encoding="utf-8")
        self.assertIn("clip: true", battle)
        self.assertIn("property bool dragActive: false", battle)
        self.assertIn("ParentChange { target: handCard; parent: table }", battle)
        self.assertIn("table.dragX - table.dragOffsetX", battle)
        self.assertIn("z: 210", battle)
        self.assertNotIn("visible: table.dragActive", battle)
        self.assertIn("onDragStarted:", battle)
        self.assertIn("signal dragStarted(", card)
        self.assertIn("preventStealing: card.dragEnabled", card)
        self.assertNotIn("drag.target: card.dragEnabled", card)

    def test_locked_collection_is_not_inspectable_and_shows_unlock_goal(self):
        root = Path(__file__).resolve().parents[1]
        collection = (root / "tabota/ui/Collection.qml").read_text(encoding="utf-8")
        bridge = (root / "tabota/bridge.py").read_text(encoding="utf-8")
        self.assertIn('interactive: modelData.unlocked', collection)
        self.assertIn('faceUp: modelData.unlocked', collection)
        self.assertIn('modelData.unlockHint', collection)
        self.assertIn('c = self.catalog_card(cid)', bridge)
        self.assertIn('return dict(id=cid, unlocked=False, image="", name="Nieodkryta karta"', bridge)
        self.assertIn('if self.screen in ("collection", "builder") and cid not in', bridge)

    def test_tutorial_popup_guides_then_yields_control(self):
        battle = (Path(__file__).resolve().parents[1] / "tabota/ui/Battle.qml").read_text(encoding="utf-8")
        self.assertIn('open: (b.tutorialGuided || b.tutorialPractice)', battle)
        self.assertIn('b.tutorialPhase === "card"', battle)
        self.assertIn('OD TERAZ GRASZ SAMODZIELNIE', battle)
        self.assertIn('(!b.tutorialGuided || b.tutorialPhase === "submit")', battle)


if __name__ == "__main__":
    unittest.main()
