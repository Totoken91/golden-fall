"""No Blender dependency: test new integrity checks with synthetic files."""
from pathlib import Path
import json
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "assets"))
from inspect_glb import inspect, GlbError
from validate_manifest import validate


class PipelineContractTests(unittest.TestCase):
    def test_project_manifest_planned(self):
        self.assertEqual(validate(ROOT / "assets" / "asset_manifest.json"), [])

    def test_tiny_valid_glb_header(self):
        doc = {"asset": {"version": "2.0"}, "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
               "accessors": [{"count": 3}], "nodes": [{"mesh": 0}], "scenes": [{"nodes": [0]}], "scene": 0}
        payload = json.dumps(doc, separators=(",", ":")).encode("utf8")
        payload += b" " * (-len(payload) % 4)
        chunk = struct.pack("<II", len(payload), 0x4E4F534A) + payload
        glb = struct.pack("<4sII", b"glTF", 2, 12 + len(chunk)) + chunk
        with tempfile.TemporaryDirectory() as p:
            path = Path(p) / "tiny.glb"
            path.write_bytes(glb)
            self.assertEqual(inspect(path)["meshes"], 1)

    def test_bad_glb_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            path = Path(p) / "bad.glb"
            path.write_bytes(b"invalid")
            with self.assertRaises(GlbError):
                inspect(path)

    def test_missing_generated_files_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            path = Path(p) / "asset_manifest.json"
            path.write_text(json.dumps({"schema_version": 1, "assets": [{
                "id": "x", "category": "prop", "status": "generated", "source": "missing.blend",
                "export": "missing.glb", "license": "original-project", "generation_method": "blender-python"}]}))
            self.assertTrue(any("absent" in x for x in validate(path)))

    def test_approved_without_visual_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            root = Path(p)
            (root / "source.blend").touch()
            (root / "export.glb").touch()
            path = root / "asset_manifest.json"
            path.write_text(json.dumps({"schema_version": 1, "assets": [{
                "id": "x", "category": "prop", "status": "approved", "source": "source.blend",
                "export": "export.glb", "license": "original-project", "generation_method": "blender-python",
                "qa": {"technical": False, "visual_in_godot": False}}]}))
            errors = validate(path)
            self.assertTrue(any("QA technique" in e for e in errors))
            self.assertTrue(any("capture Godot" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
