#!/usr/bin/env python3
"""Golden Fall town material bindings (authoring time, offline).

Reads the downloaded Poly Haven / ambientCG keys from assets/textures/manifest.json, derives the
few maps that need it (painted siding: source hue neutralised so each house can be tinted without
a blue cast) and writes game/data/town_materials.json, which town_zone.gd applies to the blockout
material names. The town UVs are authored in metres (build_town.py), so uv1_scale = 1 / tile_m.

Run: python scripts/textures/prepare_town_materials.py
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageStat

from integration import prepare_texture_import

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((ROOT/'assets/textures/manifest.json').read_text(encoding='utf-8'))
DERIVED = ROOT/'game/assets/textures/town'

# Blockout material -> source key, tint (multiplies albedo), surface response.
# Tints come from the moodboard palette (docs/golden_fall/12_ART_DIRECTION_MOODBOARD.md).
BINDINGS = {
	'asphalt':      {'key': 'polyhaven/asphalt_04/town_psx_128_4ea6ba35', 'tint': [.42, .40, .37], 'wet': True},
	'sidewalk':     {'key': 'polyhaven/concrete_tiles_02/town_psx_128_4ed5a937', 'tint': [.92, .88, .80]},
	'curb':         {'key': 'polyhaven/rough_concrete/town_psx_128_f91d557a', 'tint': [.62, .60, .55]},
	'lawn':         {'key': 'polyhaven/forrest_ground_01/town_psx_128_58b98ccd', 'tint': [.78, .66, .46]},
	'brick':        {'key': 'ambientcg/Bricks094/town_psx_128_6d0e0e96', 'tint': [.82, .72, .64]},
	'brick_dark':   {'key': 'polyhaven/brick_wall_10/town_psx_128_3340d924', 'tint': [.95, .85, .78]},
	'cinder':       {'key': 'polyhaven/concrete_block_wall/town_psx_128_ae8fa7d9', 'tint': [1.0, .96, .88]},
	'roof':         {'key': 'polyhaven/roof_slates_02/town_psx_128_394248f4', 'tint': [.34, .31, .29]},
	'siding_cream': {'derived': 'siding', 'tint': [.86, .79, .62]},
	'siding_sage':  {'derived': 'siding', 'tint': [.47, .52, .40]},
	'siding_rust':  {'derived': 'siding', 'tint': [.60, .30, .19]},
	'trim':         {'derived': 'siding', 'tint': [.80, .76, .66]},
	'trunk':        {'key': 'polyhaven/bark_brown_02/town_psx_64_45035809', 'tint': [.62, .55, .48]},
	'foundation':   {'key': 'polyhaven/rough_concrete/town_psx_128_f91d557a', 'tint': [.55, .53, .49]},
	'coping':       {'key': 'polyhaven/rough_concrete/town_psx_128_f91d557a', 'tint': [.70, .68, .63]},
}
# Original alpha-cutout foliage (scripts/assets/prepare_town_foliage.py); UVs authored per card.
FOLIAGE = {name: 'res://assets/town/foliage/%s.png' % name for name in
	('maple_orange', 'maple_amber', 'maple_copper', 'fir_tier', 'leaf_litter')}
DERIVATIONS = {
	'siding': {'key': 'polyhaven/blue_painted_planks/town_psx_128_6b50a0a6',
		'albedo': 'luminance only (blue hue removed), stretched to mean 0.72 so the per-house tint sets the paint colour; 64 px'},
}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def res(path): return 'res://' + path.relative_to(ROOT/'game').as_posix()

def derive(name, spec):
	entry = MANIFEST['assets'][spec['key']]
	maps = {role: ROOT/item['path'] for role, item in entry['godot']['maps'].items()}
	out = DERIVED/name; out.mkdir(parents=True, exist_ok=True)
	grey = ImageOps.grayscale(Image.open(maps['albedo']).convert('RGB'))
	mean = ImageStat.Stat(grey).mean[0]/255
	grey = grey.point(lambda v: max(0, min(255, round(v*.72/mean))))
	# 1 m source tile: 64 px keeps the boards near the street's ~64 texels/m (guide V0.17 density rule).
	grey = grey.resize((64, 64), Image.LANCZOS)
	albedo = out/'albedo.png'; grey.convert('RGB').save(albedo)
	prepare_texture_import(albedo, res(albedo), 'albedo')
	refs = {'albedo': albedo, **{r: p for r, p in maps.items() if r != 'albedo'}}
	lines = [f'[ext_resource type="Texture2D" path="{res(p)}" id="{r}"]' for r, p in refs.items()]
	props = [f'resource_name = "town/{name}"', 'texture_filter = 2', 'texture_repeat = true',
		'albedo_texture = ExtResource("albedo")', 'metallic_specular = 0.25', 'roughness = 1.0',
		'roughness_texture = ExtResource("roughness")', 'roughness_texture_channel = 0',
		'normal_enabled = true', 'normal_scale = 0.3', 'normal_texture = ExtResource("normal")']
	if 'ao' in refs: props += ['ao_enabled = true', 'ao_texture = ExtResource("ao")', 'ao_light_affect = 0.15']
	material = out/'material.tres'
	material.write_text(f'[gd_resource type="StandardMaterial3D" load_steps={len(lines)+1} format=3]\n\n'
		+ '\n'.join(lines) + '\n\n[resource]\n' + '\n'.join(props) + '\n', encoding='utf-8')
	return {'source_key': spec['key'], 'source_page': entry['source_page'], 'tile_m': entry['tile_m'],
		'albedo': spec['albedo'], 'maps': {r: {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)} for r, p in refs.items()},
		'material': res(material)}

derived = {name: derive(name, spec) for name, spec in DERIVATIONS.items()}
bindings = {}
for material, b in BINDINGS.items():
	if 'derived' in b:
		d = derived[b['derived']]; path, tile, source = d['material'], d['tile_m'], d['source_key']
		albedo_path = ROOT/d['maps']['albedo']['path']
	else:
		entry = MANIFEST['assets'][b['key']]
		path, tile, source = 'res://' + entry['godot']['material'].removeprefix('game/'), entry['tile_m'], b['key']
		albedo_path = ROOT/entry['godot']['maps']['albedo']['path']
	side = Image.open(albedo_path).size
	bindings[material] = {'material': path, 'source_key': source, 'tile_m': tile, 'tint': b['tint'],
		'wet': b.get('wet', False), 'texels_per_m': round(side[0]/tile[0], 1)}
(ROOT/'game/data/town_materials.json').write_text(json.dumps({'uv_period_m': [1, 1], 'bindings': bindings, 'foliage': FOLIAGE}, indent=1), encoding='utf-8')
(ROOT/'assets/textures/town_derived_manifest.json').write_text(json.dumps({'schema_version': 1,
	'purpose': 'Golden Fall town: hue-neutral siding so one real plank texture serves every house', 'derivations': derived}, indent=1), encoding='utf-8')
for m, b in bindings.items(): print(f'{m:13s} {b["texels_per_m"]:6.1f} texels/m  {b["source_key"]}')
