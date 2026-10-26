"""Public naming and backward-compatible project packaging conventions."""
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1]

class PublicNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.menu = (BASE/'tabota/ui/Menu.qml').read_text(encoding='utf-8')
        cls.main = (BASE/'tabota/ui/Main.qml').read_text(encoding='utf-8')
        cls.readme = (BASE/'README.md').read_text(encoding='utf-8')
        cls.spec = (BASE/'tabota.spec').read_text(encoding='utf-8')

    def test_window_and_menu_use_contextual_name(self):
        self.assertIn('title: "Karty TABOta: WSZYSCY DO BANA! · Puchar PROPLAYERA"', self.main)
        self.assertIn('Text { text: "Karty TABOta";', self.menu)
        self.assertIn('Text { text: "Karty TABOta";', self.main)
        self.assertNotIn('text: "TABOta";', self.menu)
        self.assertNotIn('text: "TABOta";', self.main)

    def test_visual_targets_keep_full_card_height(self):
        self.assertIn('height: Math.max(192, optionContent.implicitHeight + 28)', self.main)
        self.assertIn('id: optionContent', self.main)

    def test_executable_is_standalone_tabot_saves_remain_compatible(self):
        self.assertIn('name="TABOt"', self.spec)
        self.assertIn('name="TABOt.app"', self.spec)
        self.assertIn('`dist/TABOt/TABOt`', self.readme)
        storage=(BASE/'tabota/storage.py').read_text(encoding='utf-8')
        self.assertIn('"TABOta"', storage)  # Do not orphan older saves.

if __name__ == '__main__':
    unittest.main()
