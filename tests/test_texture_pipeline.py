"""Offline regressions for metadata parsing, cache failure and PBR conversion."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts/textures'))
from net import Client, PipelineError, digest
from providers import ph_files, acg_archive, acg_info, ph_info, rank, safe_id, resolution_choice
from processing import extract_maps, normalize_normal, convert_maps
from integration import publish


class FakeJSON:
    def __init__(self, data): self.data = data
    def json(self, url): return self.data


class Response(io.BytesIO):
    def __init__(self, body, content_type='image/png'):
        super().__init__(body)
        self.headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
    def geturl(self): return 'https://example.test/final.png'


class TexturePipelineTests(unittest.TestCase):
    def setUp(self):
        self.scratch = Path(__file__).resolve().parents[1] / 'work/texture_pipeline_tests'
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=self.scratch)
        self.root = Path(self.temp.name)
    def tearDown(self):
        assert self.root.resolve().is_relative_to(self.scratch.resolve())
        self.temp.cleanup()

    def test_ph_uses_metadata_url_and_gl_normal(self):
        body = {k: {'1k': {'png': {'url': f'https://official.test/{k}.png', 'size': 123, 'md5': 'abc'}}}
                for k in ('Diffuse', 'nor_gl', 'Rough', 'AO')}
        result = ph_files(FakeJSON(body), 'actual_id')
        self.assertEqual(result['maps']['albedo']['url'], 'https://official.test/Diffuse.png')
        self.assertEqual(result['maps']['normal']['normal_convention'], 'OpenGL')
        self.assertNotIn('nor_dx', str(result))

    def test_missing_required_map_fails(self):
        with self.assertRaises(PipelineError): ph_files(FakeJSON({}), 'actual_id')

    def test_ambient_download_never_uses_preview(self):
        candidate = {'id': 'Plaster007', 'raw_metadata': {'previewImage': {'url': 'https://bad.test/preview.png'},
            'downloadFolders': {'default': {'downloadFiletypeCategories': {'zip': {'downloads': [
                {'attribute': '4K-PNG', 'filetype': 'zip', 'downloadLink': 'https://official.test/large.zip', 'size': 99},
                {'attribute': '1K-JPG', 'filetype': 'zip', 'downloadLink': 'https://official.test/small.zip', 'size': 12}]}}}}}}
        self.assertEqual(acg_archive(candidate)['url'], 'https://official.test/small.zip')

    def test_units_and_unknown_size(self):
        acg = acg_info({'assetId': 'Wood001', 'dataType': 'Material', 'dimensionX': 100, 'dimensionY': 50})
        self.assertEqual(acg['tile_m'], [1, .5])
        ph = ph_info(FakeJSON({'type': 1, 'dimensions': [1500, 2000]}), 'wood')
        self.assertEqual(ph['tile_m'], [1.5, 2])
        self.assertIsNone(acg_info({'assetId': 'Wood001', 'dataType': 'Material'})['tile_m'])

    def test_ranking_rejects_wrong_family_and_penalizes_modern(self):
        brief = {'query': 'old wood', 'require_any': ['wood'], 'prefer': ['old'], 'avoid': ['modern', 'clean']}
        base = {'id': 'a', 'name': 'Wood', 'tags': ['wood', 'old'], 'api_rank': 0}
        modern = {**base, 'tags': ['wood', 'modern', 'clean']}
        self.assertGreater(rank(base, brief)['score'], rank(modern, brief)['score'])
        self.assertIsNone(rank({**base, 'name': 'Stone', 'tags': ['stone']}, brief))

    def test_safe_ids_and_resolution(self):
        for value in ('../x', 'https://x', 'bad id', 'a/b'):
            with self.assertRaises(PipelineError): safe_id(value)
        self.assertEqual(resolution_choice(['4k', '2k', '1k'], 1), '1k')

    def test_offline_corrupt_download_not_reused(self):
        client = Client(self.root / 'cache')
        body = b'actual binary bytes'
        client._open = lambda url: Response(body)
        target = self.root / 'file.bin'
        client.file('https://example.test/a', target, len(body), hashlib.md5(body).hexdigest())
        client.offline = True
        del client._open
        self.assertEqual(client.file('https://example.test/a', target)['sha256'], digest(target))
        target.write_bytes(b'corrupt')
        with self.assertRaises(PipelineError): client.file('https://example.test/a', target)
        self.assertFalse(target.with_name('file.bin.part').exists())

    def test_bad_size_md5_and_html_leave_no_success_receipt(self):
        for size, md5, kind in [(999, None, 'image/png'), (3, 'bad', 'image/png'), (3, None, 'text/html')]:
            client = Client(self.root / 'cache')
            client._open = lambda url: Response(b'abc', kind)
            target = self.root / 'bad.bin'
            with self.assertRaises(PipelineError): client.file('https://example.test/a', target, size, md5)
            self.assertFalse(target.exists())
            self.assertFalse(target.with_name('bad.bin.receipt.json').exists())

    def test_total_transfer_budget_is_enforced(self):
        client = Client(self.root / 'cache')
        client.transfer_budget = 5
        client._open = lambda url: Response(b'abc')
        client.file('https://example.test/first', self.root / 'first')
        with self.assertRaises(PipelineError): client.file('https://example.test/second', self.root / 'second')
        self.assertFalse((self.root / 'second').exists())

    def test_metadata_cache_works_without_network(self):
        client = Client(self.root / 'cache')
        client._open = lambda url: Response(b'{"id":"actual"}', 'application/json')
        self.assertEqual(client.json('https://example.test/api'), {'id': 'actual'})
        client.offline = True
        del client._open
        self.assertEqual(client.json('https://example.test/api'), {'id': 'actual'})
        with self.assertRaises(PipelineError): client.json('https://example.test/missing')

    def test_zip_traversal_rejected(self):
        archive = self.root / 'bad.zip'
        with zipfile.ZipFile(archive, 'w') as z: z.writestr('../Color.png', b'bad')
        with self.assertRaises(PipelineError): extract_maps(archive, self.root / 'maps')

    def test_archive_extracts_only_useful_maps_and_prefers_gl(self):
        image = io.BytesIO()
        Image.new('RGB', (64, 64), (128, 128, 255)).save(image, format='PNG')
        archive = self.root / 'real.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for role in ('Color', 'NormalGL', 'NormalDX', 'Roughness', 'Displacement'):
                z.writestr('Asset_1K_' + role + '.png', image.getvalue())
            z.writestr('ignore.txt', 'not a texture')
        maps = extract_maps(archive, self.root / 'maps')
        self.assertEqual(set(maps), {'albedo', 'normal', 'roughness'})
        self.assertIn('NormalGL', maps['normal']['archive_member'])
        self.assertEqual(len(list((self.root / 'maps').iterdir())), 3)

    def test_dx_normals_are_flipped_and_renormalized(self):
        converted = normalize_normal(Image.new('RGB', (1, 1), (128, 200, 220)), directx=True)
        r, g, b = converted.getpixel((0, 0))
        self.assertLess(g, 128)
        length = sum((v / 127.5 - 1) ** 2 for v in (r, g, b)) ** .5
        self.assertAlmostEqual(length, 1, places=2)

    def test_maps_transform_independently_and_uv_scale_is_physical(self):
        sources = {}
        for role, color in [('albedo', (120, 100, 80)), ('normal', (128, 128, 255)), ('roughness', (90, 90, 90))]:
            path = self.root / (role + '.png')
            Image.new('RGB', (128, 64), color).save(path)
            sources[role] = {'path': path, 'normal_convention': 'OpenGL'}
        profile = {'saturation': .88, 'rgb_gain': [1.02, 1, .94], 'normal_scale': .35, 'filter_enum': 3}
        maps, seam = convert_maps(sources, self.root / 'optimized', profile, 64)
        self.assertEqual(maps['roughness']['output_dimensions'], [64, 32])
        with Image.open(maps['roughness']['path']) as im: self.assertEqual(im.getpixel((0, 0)), 90)
        result = publish(self.root, 'provider/asset/profile', maps, [1.5, .5], [3, 2], profile)
        self.assertEqual(result['uv_scale'], [2, 4])
        self.assertFalse(result['applied_to_game_scene'])
        import_text = (self.root / result['maps']['albedo']['path']).with_suffix('.png.import').read_text(encoding='utf-8')
        self.assertIn('mipmaps/generate=true', import_text)
        self.assertIn('compress/normal_map=2', import_text)
        text = (self.root / result['material']).read_text(encoding='utf-8')
        self.assertIn('roughness_texture_channel = 0', text)
        self.assertNotIn('ao_enabled', text)
        self.assertTrue(seam['visual_review_required'])


if __name__ == '__main__': unittest.main()
