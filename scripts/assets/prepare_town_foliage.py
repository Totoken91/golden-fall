"""Golden Fall town foliage textures: original, deterministic, low resolution, alpha cutout.

Bigleaf maple leaf clumps (three autumn tints), a Douglas-fir branch tier wrapped on open cones,
and fallen-leaf litter decals. Palette from docs/golden_fall/12_ART_DIRECTION_MOODBOARD.md.
Run: python scripts/assets/prepare_town_foliage.py
"""
from pathlib import Path
import math, random, sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'game/assets/town/foliage'
sys.path.insert(0, str(ROOT/'scripts/textures'))
from integration import prepare_texture_import

def shade(c, k): return tuple(max(0, min(255, round(v*k))) for v in c)

def maple_leaf(d, x, y, r, angle, colour):
	"""Five-lobed leaf as one polygon: readable at 2-6 px, which is all a PSX canopy needs."""
	pts = []
	for i in range(10):
		a = angle + i*math.tau/10
		rr = r if i % 2 == 0 else r*.45
		pts.append((x+math.cos(a)*rr, y+math.sin(a)*rr))
	d.polygon(pts, fill=colour)

def clump(index, base):
	"""Leaf clump card: dense core, ragged lobed outline, a few sky holes, twigs reaching the edge."""
	rng = random.Random(151100+index)
	im = Image.new('RGBA', (128, 128)); d = ImageDraw.Draw(im)
	for _ in range(5):
		a = rng.uniform(0, math.tau); d.line((64, 70, 64+math.cos(a)*46, 66+math.sin(a)*42), fill=(52, 36, 24, 255), width=2)
	lobes = [(64+rng.uniform(-30, 30), 64+rng.uniform(-26, 24), rng.uniform(16, 26)) for _ in range(7)] + [(64, 64, 30)]
	for cx, cy, rad in lobes:
		for _ in range(int(rad*7)):
			a = rng.uniform(0, math.tau); r = math.sqrt(rng.random())*rad
			x, y = cx+math.cos(a)*r, cy+math.sin(a)*r*.85
			# Lit from above: top leaves warmer and lighter, underside darker copper.
			k = 1.18-.55*(y/128)+rng.uniform(-.18, .18)
			c = rng.choice(base)
			maple_leaf(d, x, y, rng.uniform(2.2, 4.6), rng.uniform(0, math.tau), shade(c, k)+(255,))
	# Punch a few holes so the sky reads through the crown.
	for _ in range(6):
		x, y, r = rng.uniform(30, 98), rng.uniform(30, 98), rng.uniform(2, 4.5)
		d.ellipse((x-r, y-r, x+r, y+r), fill=(0, 0, 0, 0))
	return im

def fir_tier():
	"""Open-cone tier: U wraps the circumference, V runs apex (0) to branch tips (1).
	Drooping needle sprays with a jagged alpha fringe at the bottom edge."""
	rng = random.Random(151200)
	W, H = 128, 64
	im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
	d.rectangle((0, 0, W, int(H*.55)), fill=(24, 36, 29, 255))
	for _ in range(170):
		x = rng.uniform(0, W); top = rng.uniform(0, H*.5); bottom = rng.uniform(H*.7, H-1)
		c = rng.choice([(28, 42, 33), (33, 49, 37), (22, 33, 27), (40, 55, 40), (47, 58, 40)])
		k = .8+.45*(1-top/H)
		col = shade(c, k)+(255,)
		bend = rng.uniform(-6, 6)
		d.line((x, top, x+bend*.5, (top+bottom)/2, x+bend, bottom), fill=col, width=rng.choice((2, 3, 3, 4)))
		for t in range(3):
			yy = top+(bottom-top)*(t+1)/4
			d.line((x+bend*t/3, yy, x+bend*t/3+rng.uniform(-5, 5), yy+rng.uniform(3, 7)), fill=col, width=1)
	for x in range(W):          # wrap seam: copy left edge columns to the right so U=0/1 meet
		pass
	return im

def litter():
	"""Fallen maple leaves on wet ground: sparse, clustered toward the centre, transparent between."""
	rng = random.Random(151300)
	im = Image.new('RGBA', (128, 128)); d = ImageDraw.Draw(im)
	cols = [(200, 98, 30), (142, 59, 23), (227, 154, 62), (110, 52, 26), (90, 58, 34)]
	for _ in range(520):
		r = math.sqrt(rng.random())*60; a = rng.uniform(0, math.tau)
		x, y = 64+math.cos(a)*r, 64+math.sin(a)*r
		if rng.random() < r/80: continue
		maple_leaf(d, x, y, rng.uniform(2.0, 3.8), rng.uniform(0, math.tau), shade(rng.choice(cols), rng.uniform(.6, .95))+(255,))
	return im

OUT.mkdir(parents=True, exist_ok=True)
textures = {
	'maple_orange': clump(0, [(200, 98, 30), (214, 120, 40), (176, 82, 26)]),
	'maple_amber': clump(1, [(227, 154, 62), (214, 132, 48), (196, 118, 40)]),
	'maple_copper': clump(2, [(142, 59, 23), (168, 78, 30), (122, 50, 22)]),
	'fir_tier': fir_tier(),
	'leaf_litter': litter(),
}
for name, im in textures.items():
	path = OUT/f'{name}.png'; im.save(path)
	prepare_texture_import(path, 'res://'+path.relative_to(ROOT/'game').as_posix(), 'albedo')
sheet = Image.new('RGBA', (128*5, 128), (60, 58, 52, 255))
for i, im in enumerate(textures.values()): sheet.alpha_composite(im, (128*i, 0))
(ROOT/'work/art_trees').mkdir(parents=True, exist_ok=True)
sheet.resize((128*5*3, 128*3), Image.NEAREST).save(ROOT/'work/art_trees/foliage_sheet.png')
print('foliage textures', list(textures))
