"""The target modal's header must not collide with its source card or target list."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'tabota/ui/Main.qml'

class TargetModalTypography(unittest.TestCase):
    def test_texts_and_layout_do_not_have_em_dash(self):
        # Inspect project sources, not installed dependencies or bundled Qt.
        # Local builds create .venv/build/dist trees containing third-party text.
        paths = list(ROOT.glob('*'))
        for directory in ('tabota', 'tests', 'scripts', 'docs', '.github'):
            paths.extend((ROOT / directory).rglob('*'))
        for path in paths:
            if path.is_file() and path.suffix in {'.py','.qml','.md','.txt','.spec','.yml','.yaml','.json','.toml'} and '__pycache__' not in str(path):
                self.assertNotIn(chr(0x2014), path.read_text(encoding='utf-8'), f'Long dash in {path}')

    def test_source_card_beside_not_over_heading(self):
        text=MAIN.read_text(encoding='utf-8')
        self.assertIn('x: 30; y: 23; width: 865;', text)
        self.assertIn('x: 950; y: 27; width: 88', text)
        self.assertLess(30+865, 950)
        self.assertIn('targetHeader.y + targetHeader.implicitHeight + 16', text)
        self.assertIn('targetSourceCard.y + targetSourceCard.height + 16', text)
        self.assertIn('height: Math.max(80, cancelTarget.y - y - 12)', text)
        self.assertIn('Math.max(192, optionContent.implicitHeight + 28)', text)

    def test_effect_description_always_visible_above_list(self):
        text=MAIN.read_text(encoding='utf-8')
        self.assertIn('window.displayOptions[0].effect ||', text)
        self.assertIn('id: targetHeader', text)
        self.assertIn('id: targetOptionList', text)
        self.assertIn('clip: true; spacing: 12', text)

if __name__ == '__main__':
    unittest.main()
