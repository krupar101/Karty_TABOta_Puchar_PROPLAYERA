"""Static contracts for complete screen/modal fades and card interaction roles.

Runtime rendering is checked by scripts/check_fades.py on computers with Qt.
"""
import unittest
from pathlib import Path

UI = Path(__file__).resolve().parents[1] / "tabota" / "ui"


class FadeAndCardRoleContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = (UI / "Card.qml").read_text(encoding="utf-8")
        cls.battle = (UI / "Battle.qml").read_text(encoding="utf-8")
        cls.main = (UI / "Main.qml").read_text(encoding="utf-8")
        cls.fade = (UI / "FadeBox.qml").read_text(encoding="utf-8")
        cls.help = (UI / "Help.qml").read_text(encoding="utf-8")
        cls.fortune = (UI / "Fortune.qml").read_text(encoding="utf-8")

    def test_details_affordance_in_same_animated_item_as_art(self):
        motion_start = self.card.index("id: motion")
        overlay_start = self.card.index("id: inspectAffordance")
        mouse_start = self.card.index("id: mouse")
        # The inspect overlay is not a sibling of the animated card: it follows
        # the same parent with lift/rotation/scale and flip entrance transform.
        self.assertLess(motion_start, overlay_start)
        self.assertLess(overlay_start, mouse_start)
        self.assertIn('objectName: "tabotaCardMotion"', self.card)
        self.assertIn('objectName: "tabotaInspectAffordance"', self.card)
        self.assertIn('opacity: card.lowerHalfHovered && !card.moving ? 1 : 0', self.card)
        self.assertIn('card.splitClickDetails && event.y >= card.height/2', self.card)
        self.assertIn('splitClickDetails: !b.choice', self.battle)

    def test_placed_cards_have_no_split_or_inspection_overlay(self):
        lines = self.battle.splitlines()
        played = next(line for line in lines if 'playerUnits[index]' in line)
        self.assertIn('playerUnits[index]', played)
        played_card = next(line for line in lines if 'splitClickDetails: false;' in line)
        self.assertIn('onClicked: api.inspect(info.id)', played_card)
        self.assertNotIn('api.chooseLane(', played_card)
        self.assertIn('enabled: !parent.unit', self.battle)  # Empty slots still accept lane clicks.

    def test_screen_router_fades_out_before_switch_and_fades_in_after(self):
        self.assertIn('id: pageFadeOut', self.main)
        self.assertIn('id: pageFadeIn', self.main)
        self.assertIn('stage.displayedScreen = stage.requestedScreen', self.main)
        self.assertIn('pageFadeIn.start()', self.main)
        self.assertIn('enabled: !pageFadeOut.running && !pageFadeIn.running', self.main)
        self.assertLess(self.main.index('stage.displayedScreen = stage.requestedScreen'), self.main.index('id: pageFadeIn'))

    def test_modal_fades_draw_exits_without_intercepting_input(self):
        self.assertIn('visible: open || opacity > 0.001', self.fade)
        self.assertIn('enabled: open', self.fade)
        self.assertIn('opacity: open ? 1 : 0', self.fade)
        self.assertIn('api.state.settings.reduced ? 35 : 190', self.fade)
        for name in ['tabotaNotice', 'tabotaDetailDialog', 'tabotaTargetDialog', 'tabotaConfirmationDialog']:
            self.assertIn(f'objectName: "{name}"', self.main)
        for name in ['tabotaRuleWindow', 'tabotaExchangePanel', 'tabotaTutorialPanel']:
            self.assertIn(f'objectName: "{name}"', self.battle)

    def test_rule_and_exchange_do_not_overlap_even_during_exit(self):
        self.assertIn('open: b.mulligan && !b.rulePending && !ruleWindow.visible', self.battle)
        self.assertIn('open: !!b.rulePending;', self.battle)
        self.assertIn('!exchangePanel.visible && !ruleWindow.visible', self.battle)

    def test_other_dynamic_content_has_fades(self):
        self.assertIn('onShowLogChanged: logFade.restart()', self.battle)
        self.assertIn('onShowExtraChanged: rulesFade.restart()', self.help)
        self.assertIn('guide.displayedExtra = guide.showExtra', self.help)
        self.assertIn('opacity: fortune.phase === 2 ? 1 : 0', self.fortune)


if __name__ == "__main__":
    unittest.main()
