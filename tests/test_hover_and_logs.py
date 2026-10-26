"""Contracts for a single animated hover card and clean QML shutdown."""
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


class HoverAndLogTests(unittest.TestCase):
    def setUp(self):
        self.battle = (BASE / "tabota/ui/Battle.qml").read_text(encoding="utf-8")
        self.card = (BASE / "tabota/ui/Card.qml").read_text(encoding="utf-8")
        self.main = (BASE / "main.py").read_text(encoding="utf-8")

    def test_hover_reparents_the_original_card_without_double_animation(self):
        self.assertEqual(self.battle.count('ParentChange { target: handCard; parent: table }'), 1)
        self.assertNotIn('table.hoverInfo', self.battle)
        self.assertNotIn('table.hoverUid', self.battle)
        self.assertIn('id: handSlot', self.battle)
        self.assertIn('id: handCard', self.battle)
        self.assertIn(': handArea.x + 10 + handSlot.index * 110 - handArea.contentX', self.battle)
        self.assertIn('table.dragActive && table.dragUid === handSlot.handInfo.uid', self.battle)
        self.assertIn('table.dragX - table.dragOffsetX', self.battle)
        self.assertNotIn('dragInfo:', self.battle)
        self.assertNotIn('visible: table.dragActive', self.battle)

    def test_inspection_overlay_fades_on_details_hover(self):
        self.assertIn('id: inspectAffordance', self.card)
        self.assertIn('opacity: card.lowerHalfHovered && !card.moving ? 1 : 0', self.card)
        self.assertIn('Behavior on opacity', self.card)
        self.assertNotIn('visible: (card.lowerHalfHovered', self.card)
        self.assertIn('card.splitClickDetails && event.y >= card.height/2', self.card)
        self.assertIn('event.button === Qt.RightButton', self.card)

    def test_no_undefined_bool_binding_or_shutdown_context_leak(self):
        self.assertNotIn('table.hoverInfo.selected || table.hoverInfo.exchange', self.battle)
        self.assertIn('root_window.deleteLater()', self.main)
        self.assertIn('QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)', self.main)


if __name__ == "__main__":
    unittest.main()
