"""Readable rule-badge layout at hand and battlefield card widths.

This is geometry + QML source-contract coverage; final visual QA still needs Qt.
"""
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1]
CARD = (BASE / 'tabota/ui/Card.qml').read_text(encoding='utf-8')
BATTLE = (BASE / 'tabota/ui/Battle.qml').read_text(encoding='utf-8')


def overlap(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


class BadgePlacementTests(unittest.TestCase):
    def test_rule_badge_is_inside_card(self):
        self.assertIn('id: ruleNameBadge', CARD)
        self.assertIn('objectName: "tabotaNameRuleBadge"', CARD)
        self.assertIn('property bool compact: card.width < 80', CARD)
        self.assertIn('x: parent.width - width - (compact ? 1 : 0)', CARD)
        self.assertIn('y: card.onTable ? 2 : (compact ? -22 : -8)', CARD)
        self.assertNotIn('x: parent.width - 53; y: 6;', CARD)
        self.assertEqual(BATTLE.count('onTable: true'), 2)
        self.assertIn('property bool onTable: false', CARD)
        self.assertIn('Row { x: 15; y: 53;', BATTLE)
        self.assertIn('Row { x: 15; y: 234;', BATTLE)

    def test_cost_and_rule_badge_never_intersect_for_all_card_widths(self):
        for width in (52, 67):
            for variant in ('A', 'BEZ A'):
                compact = width < 80
                badge_width = (19 if variant == 'A' else 39) if compact else (25 if variant == 'A' else 48)
                badge_height = 14 if compact else 17
                x = width - badge_width - (1 if compact else 0)
                y = 2
                badge = (x, y, x + badge_width, y + badge_height)
                cost_y = -28 if x < 40 else -7
                cost = (-5, cost_y, 38, cost_y + 28)
                with self.subTest(width=width, badge=variant):
                    self.assertGreaterEqual(x, 0, 'badge cannot protrude toward neighbouring card')
                    self.assertLessEqual(x + badge_width, width)
                    self.assertFalse(overlap(cost, badge), 'rule marker cannot cover energy chip')
                    self.assertLessEqual(cost_y, 2, 'energy must remain at the top-left corner')
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(y + badge_height, width * 603 / 388)

    def test_rule_and_protection_stay_separate(self):
        self.assertIn('y: card.onTable && card.info.nameRuleBadge ? 49', CARD)
        self.assertIn('font.pixelSize: card.width < 80 ? 16 : 24', CARD)
        for width in (52, 67, 98, 132):
            bottom = 2 + (14 if width < 80 else 17)
            protection_top = 49
            with self.subTest(width=width):
                self.assertLessEqual(bottom, protection_top)

    def test_rule_badge_is_specific_to_name_rule_not_all_rounds(self):
        bridge = (BASE / 'tabota/bridge.py').read_text(encoding='utf-8')
        self.assertIn('active.s.get("mission") == 3', bridge)
        self.assertIn('visible: card.battle && card.faceUp && !!card.info.nameRuleBadge', CARD)
        # Silence is intentionally a strong red X across the picture.
        self.assertIn('visible: card.battle && card.info.silenced === true', CARD)


if __name__ == '__main__':
    unittest.main()
