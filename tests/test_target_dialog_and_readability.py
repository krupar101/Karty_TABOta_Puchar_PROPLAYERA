"""Regression checks for visual target selection and player-facing wording."""
from pathlib import Path
import unittest

from tabota.content import ENCOUNTERS

BASE = Path(__file__).resolve().parents[1]
UI = BASE / "tabota" / "ui"


class TargetDialogReadabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = (UI / "Main.qml").read_text(encoding="utf-8")
        cls.card = (UI / "Card.qml").read_text(encoding="utf-8")
        cls.engine = (BASE / "tabota" / "engine.py").read_text(encoding="utf-8")

    def test_target_dialog_uses_visual_cards_and_effect_copy(self):
        self.assertIn('objectName: "tabotaTargetDialog"', self.main)
        self.assertIn('"Wybierz cel efektu"', self.main)
        self.assertIn('window.displayOptions[0].effect', self.main)
        self.assertIn('id: targetHeader', self.main)
        self.assertIn('id: targetSourceCard', self.main)
        self.assertIn('id: targetOptionList', self.main)
        self.assertIn('targetHeader.y + targetHeader.implicitHeight + 16', self.main)
        self.assertIn('targetSourceCard.y + targetSourceCard.height + 16', self.main)
        self.assertIn('Math.max(192, optionContent.implicitHeight + 28)', self.main)
        self.assertIn('delegate: Card {', self.main)
        self.assertIn('text: "Wybierz opcję, a następnie', self.main)
        self.assertIn('chosen: true', self.main)

    def test_silenced_cards_have_stronger_overlay_and_name_rule_badge(self):
        self.assertIn('card.info.nameRuleBadge', self.card)
        self.assertIn('text: card.info.nameRuleBadge', self.card)
        self.assertGreaterEqual(self.card.count('card.info.silenced === true'), 3)
        self.assertIn('⛔ Wyciszona: Aura i Finał tej karty są wyłączone.', self.card)

    def test_player_facing_text_has_no_namekey_in_encounter_rule(self):
        self.assertNotIn('nameKey', ENCOUNTERS[2]['rule'])
        self.assertIn('bez litery „A” w nazwie', ENCOUNTERS[2]['rule'])
        self.assertNotIn('[uid]', self.engine)


if __name__ == "__main__":
    unittest.main()
