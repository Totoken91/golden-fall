from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class SourceEncodingTests(unittest.TestCase):
    def test_godot_sources_are_utf8_without_mojibake(self):
        for path in (ROOT/'game').rglob('*.gd'):
            if '.godot' in path.parts:continue
            text=path.read_bytes().decode('utf-8')
            for marker in ['\u00c3','\u00c2','\u00e2\u20ac','\ufffd']:
                self.assertNotIn(marker,text,str(path))
        text=(ROOT/'game/scripts/room_scene.gd').read_text(encoding='utf-8')
        self.assertIn('ui.label("·",21',text)
        self.assertIn('Esc pause',text)
