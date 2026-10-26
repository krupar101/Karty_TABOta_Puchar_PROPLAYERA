"""Regression checks for responsive details and off-thread frame generation."""
from copy import deepcopy
from pathlib import Path
import unittest

from tabota.engine import Match, ai_plan, prepare_turn
from tabota.content import CARDS

ROOT = Path(__file__).resolve().parents[1]


class TurnPerformanceTests(unittest.TestCase):
    def test_background_resolution_matches_original_sealed_rules(self):
        # Compare every animation snapshot and final match for normal, hard,
        # tutorial, rituals, all campaign encounters and different turn orders.
        for mission in range(1, 21):
            for hard in [False, True]:
                m = Match(mission, hard=hard, seed=mission * 73 + int(hard))
                m.mulligan(0, [])
                m.mulligan(1, [])
                for _ in range(3):
                    old = m.clone(False)
                    # Simple, legal player plan from the same public AI planner.
                    player = ai_plan(m, 0, "easy")
                    expected_enemy = ai_plan(old, 1, "easy")
                    expected_frames = old.commit([deepcopy(player), expected_enemy])
                    while old.s["choices"] and old.s["choices"][0]["owner"] == 1:
                        uid = min(old.s["hand"][1], key=lambda u: CARDS[u["card"]]["power"])["uid"]
                        old.discard_choice(uid)
                    expected_frames[-1] = deepcopy(old.s)
                    actual_state, actual_frames = prepare_turn(m, player, "easy")
                    self.assertEqual(actual_state, old.s, (mission, hard))
                    self.assertEqual(actual_frames, expected_frames, (mission, hard))
                    self.assertEqual(m.s["turn"], len(m.s["actions"]) + 1)
                    m = Match.restore(actual_state)
                    while m.s["choices"]:
                        p = m.s["choices"][0]["owner"]
                        m.discard_choice(m.s["hand"][p][0]["uid"])
                    if m.s["finished"]:
                        break

    def test_tutorial_remains_deterministic(self):
        m = Match(tutorial=True)
        lesson = m.tutorial_move()
        player = m.candidates(0, lesson["uid"], lesson["lane"])[:1]
        final, frames = prepare_turn(m, player, "easy")
        self.assertEqual(final["turn"], 2)
        self.assertGreaterEqual(len(frames), 2)
        self.assertEqual(m.s["turn"], 1)  # untouched input

    def test_playback_uses_independent_board_notifications(self):
        bridge = (ROOT / "tabota/bridge.py").read_text(encoding="utf-8")
        battle = (ROOT / "tabota/ui/Battle.qml").read_text(encoding="utf-8")
        main = (ROOT / "tabota/ui/Main.qml").read_text(encoding="utf-8")
        self.assertIn('boardChanged = Signal()', bridge)
        self.assertIn('def battleBoard(self): return self._battle_board', bridge)
        self.assertIn('self.refresh_frame()', bridge)
        self.assertIn('self.worker.signals.done.connect(self.resolve)', bridge)
        self.assertIn('outcome = prepare_turn(', bridge)
        self.assertIn('self.signals.done.emit((*outcome,', bridge)
        self.assertIn('property var liveBoard: api.battleBoard', battle)
        self.assertNotIn('property var b: s.board', battle)
        self.assertIn('def closeDetail(self):', bridge)
        self.assertIn('self._state["detail"] = {}', bridge)
        self.assertIn('fadeDuration: window.s.settings.reduced ? 35 : 150', main)

    def test_skip_while_ai_still_thinking_does_not_finish_match(self):
        bridge = (ROOT / "tabota/bridge.py").read_text(encoding="utf-8")
        start = bridge.index('    def skipAnimation(self):')
        end = bridge.index('    @Slot()', start)
        self.assertIn('if self.frames:', bridge[start:end])
        self.assertNotIn('self.advance()\n        else:', bridge[start:end])


if __name__ == "__main__":
    unittest.main()
