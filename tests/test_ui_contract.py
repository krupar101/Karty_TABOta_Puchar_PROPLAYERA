"""Regression checks for player-visible UI contract, no Qt runtime required."""
from pathlib import Path
import unittest

UI = Path(__file__).resolve().parents[1] / "tabota" / "ui"


class UiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.battle = (UI / "Battle.qml").read_text(encoding="utf-8")
        cls.card = (UI / "Card.qml").read_text(encoding="utf-8")
        cls.help = (UI / "Help.qml").read_text(encoding="utf-8")
        cls.main = (UI / "Main.qml").read_text(encoding="utf-8")

    def test_card_cost_and_power_have_icons(self):
        self.assertIn('EnergyIcon { width: 10; height: 15;', self.card)
        self.assertIn('text: "✦ " + (card.info.currentPower', self.card)
        self.assertIn('text: "⚡ KOSZT "', self.main)
        self.assertIn('text: "✦ " + lane.laneInfo.player', self.battle)

    def test_energy_is_placed_by_player_hand(self):
        self.assertIn('text: "TWOJA ENERGIA"', self.battle)
        self.assertIn("x: 0; y: 481; width: 1020;", self.battle)
        self.assertIn("x: 0; y: 555; width: 1020;", self.battle)
        self.assertNotIn('Row { x: 215; y: 4; spacing:', self.battle)

    def test_mulligan_is_explained_and_counted(self):
        self.assertIn('text: "DO WYMIANY"', self.card)
        self.assertIn('text: "Zaznaczone do wymiany: " + b.exchangeCount', self.battle)
        self.assertIn("api.exchange()", self.battle)
        self.assertIn('text: b.mulligan ? "TWOJE KARTY', self.battle)

    def test_end_turn_and_simple_rules(self):
        self.assertIn('"Zakończ turę  →"', self.battle)
        self.assertNotIn('"Ujawnij plan  →"', self.battle)
        self.assertIn('title: journal ? "Kronika Turnieju" : "Jak grać? To proste."', self.help)
        self.assertIn('guide.basics.concat(guide.displayedExtra ? guide.extras : [])', self.help)
        self.assertIn("Karty TABOta: WSZYSCY DO BANA!", self.main)


if __name__ == "__main__":
    unittest.main()
