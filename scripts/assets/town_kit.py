"""Golden Fall town kit: materials, primitives and modelled assemblies (bpy, low poly).

Imported by build_town.py, which only lays the town out. Blender coordinates: X east, Y north,
Z up, metres. Every solid is built closed with outward normals (Godot culls back faces); faces
that would sit against another surface are skipped to save triangles.
"""
import bpy, math, random
from mathutils import Vector

rng = random.Random(151003)

# ---------- materials: blockout palette, golden autumn, no blue cast ----------
mats = {}
def mat(name, color, emission=0.0, rough=.92):
	m = bpy.data.materials.new(name); m.use_nodes = True
	bs = m.node_tree.nodes['Principled BSDF']
	bs.inputs['Base Color'].default_value = (*color, 1); bs.inputs['Roughness'].default_value = rough
	if emission:
		bs.inputs['Emission Color'].default_value = (*color, 1); bs.inputs['Emission Strength'].default_value = emission
	m.diffuse_color = (*color, 1); mats[name] = m
for name, c, e in [
	('asphalt', (.075,.07,.065), 0), ('road_line', (.55,.45,.18), 0), ('sidewalk', (.36,.34,.30), 0), ('curb', (.42,.40,.36), 0),
	('lawn', (.17,.14,.07), 0), ('dirt', (.16,.11,.07), 0), ('leaves_ground', (.36,.18,.06), 0),
	('siding_cream', (.62,.57,.46), 0), ('siding_sage', (.33,.37,.29), 0), ('siding_rust', (.42,.20,.12), 0),
	('roof', (.12,.10,.09), 0), ('trim', (.70,.66,.56), 0), ('trim_paint', (.52,.49,.41), 0), ('door_wood', (.25,.14,.07), 0),
	('brick', (.36,.17,.11), 0), ('brick_dark', (.24,.12,.08), 0), ('cinder', (.40,.38,.34), 0),
	('diner_enamel', (.62,.55,.40), 0), ('diner_red', (.48,.12,.08), 0), ('chrome', (.55,.53,.50), 0),
	('window_dark', (.05,.06,.06), 0), ('glow_warm', (.95,.62,.30), 2.2), ('neon', (.95,.30,.12), 5.0),
	('diner_floor', (.55,.50,.42), 0), ('counter_top', (.66,.62,.55), 0), ('booth_red', (.42,.10,.07), 0),
	('wood_table', (.38,.24,.13), 0), ('metal_dark', (.17,.17,.16), 0), ('dumpster', (.16,.22,.15), 0),
	('fence_wood', (.27,.18,.11), 0), ('pole_wood', (.20,.14,.09), 0), ('wire', (.04,.04,.04), 0),
	('lamp_head', (1.0,.62,.25), 3.0), ('car_rust', (.38,.16,.10), 0), ('car_cream', (.60,.55,.45), 0), ('car_green', (.18,.26,.20), 0),
	('tyre', (.05,.05,.05), 0), ('trunk', (.16,.11,.07), 0), ('leaf_orange', (.62,.26,.06), 0), ('leaf_amber', (.70,.40,.09), 0),
	('leaf_copper', (.45,.17,.07), 0), ('spruce', (.07,.11,.08), 0), ('guardrail', (.45,.43,.40), 0), ('sign_board', (.20,.15,.10), 0),
	('service_light', (1.0,.80,.50), 2.5)]:
	mat(name, c, e)

# Materials that receive a real texture in Godot (game/data/town_materials.json): their UVs are
# authored in metres so the binding can scale by the source tile size.
TEXTURED = {'asphalt', 'sidewalk', 'curb', 'lawn', 'brick', 'brick_dark', 'cinder', 'roof',
	'siding_cream', 'siding_sage', 'siding_rust', 'trim'}

def finish(o, material, tile=1.0):
	"""World-space planar UVs (metres / tile), like build_room.py."""
	if material in TEXTURED: tile = 1.0
	o.data.materials.append(mats[material])
	uv = o.data.uv_layers.new(name='UVMap') if not o.data.uv_layers else o.data.uv_layers.active
	mw = o.matrix_world
	for poly in o.data.polygons:
		n = poly.normal; axis = max(range(3), key=lambda i: abs(n[i])); axes = [i for i in range(3) if i != axis]
		for li in poly.loop_indices:
			v = mw @ o.data.vertices[o.data.loops[li].vertex_index].co
			uv.data[li].uv = (v[axes[0]]/tile, v[axes[1]]/tile)
	return o

def box(name, x0, x1, y0, y1, z0, z1, material, tile=1.0):
	bpy.ops.mesh.primitive_cube_add(size=1, location=((x0+x1)/2, (y0+y1)/2, (z0+z1)/2))
	o = bpy.context.object; o.name = name; o.dimensions = (abs(x1-x0), abs(y1-y0), abs(z1-z0))
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(o, material, tile)

def cyl(name, x, y, z0, z1, r, material, verts=8, r2=None):
	bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r if r2 is None else r2, depth=z1-z0, location=(x, y, (z0+z1)/2))
	o = bpy.context.object; o.name = name
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
	return finish(o, material)

def gable(name, x0, x1, y0, y1, z0, ridge, material, along='y'):
	"""Pitched roof as a single prism; ridge runs along Y (or X)."""
	xm, ym = (x0+x1)/2, (y0+y1)/2
	if along == 'y':
		v = [(x0,y0,z0),(x1,y0,z0),(xm,y0,ridge),(x0,y1,z0),(x1,y1,z0),(xm,y1,ridge)]
	else:
		v = [(x0,y0,z0),(x0,y1,z0),(x0,ym,ridge),(x1,y0,z0),(x1,y1,z0),(x1,ym,ridge)]
	f = [(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)]
	me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	return finish(o, material, 2.0)

def ramp(name, x0, x1, y0, y1, z0, z1):
	"""Invisible walkable wedge rising from z0 at x0 to z1 at x1 (collision only, never rendered).
	A 15 cm curb is a wall for a capsule; a 20-degree ramp over it is not."""
	v = [(x0,y0,z0),(x1,y0,z1),(x1,y0,z0),(x0,y1,z0),(x1,y1,z1),(x1,y1,z0)]
	f = [(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(0,3,5,2)]
	me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update()
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	return finish(o, 'asphalt')

def empty(name, loc, yaw_deg):
	o = bpy.data.objects.new(name, None); o.location = loc; o.rotation_euler = (0, 0, math.radians(yaw_deg))
	bpy.context.collection.objects.link(o); return o

for name, c in [('foundation', (.40,.38,.34)), ('glass', (.05,.055,.055)), ('lattice', (.10,.08,.06)),
		('coping', (.45,.43,.39)), ('storefront_wood', (.22,.12,.07)), ('collision', (1,0,1))]:
	mat(name, c)
TEXTURED |= {'foundation', 'coping'}

# ---------- closed solids with guaranteed outward normals ----------
def solid(name, pts, material, skip=()):
	"""Convex hexahedron from 8 corners indexed c[i+2j+4k] (i,j,k in 0/1 along three edges).
	Faces are oriented outward from the centroid, so tapered or sloped corners stay correct.
	skip: face keys 'i0','i1','j0','j1','k0','k1' that sit against something and are never seen."""
	P = [Vector(p) for p in pts]
	quads = {'k0': (0,1,3,2), 'k1': (4,6,7,5), 'i0': (0,2,6,4), 'i1': (1,5,7,3), 'j0': (0,4,5,1), 'j1': (2,3,7,6)}
	centre = sum(P, Vector()) / 8
	faces = []
	for key, q in quads.items():
		if key in skip: continue
		f = list(q)
		a, b, c = P[f[0]], P[f[1]], P[f[2]]
		n = (b-a).cross(c-a)
		mid = sum((P[i] for i in f), Vector())/4
		if n.dot(mid-centre) < 0: f.reverse()
		faces.append(f)
	me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in P], [], faces); me.update()
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	return finish(o, material)

def wbox(name, x0, x1, y0, y1, z0, z1, material, skip=()):
	"""World-aligned box; skip uses '-x','+x','-y','+y','-z','+z'."""
	keys = {'-x': 'i0', '+x': 'i1', '-y': 'j0', '+y': 'j1', '-z': 'k0', '+z': 'k1'}
	pts = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
	return solid(name, pts, material, tuple(keys[s] for s in skip))

def prism(name, pts, material, outward):
	"""Single flat polygon facing `outward` (gable triangles and other plates)."""
	me = bpy.data.meshes.new(name); P = [Vector(p) for p in pts]
	f = list(range(len(P)))
	if (P[1]-P[0]).cross(P[2]-P[0]).dot(Vector(outward)) < 0: f.reverse()
	me.from_pydata([tuple(p) for p in P], [], [f]); me.update()
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	return finish(o, material)

def collider(name, x0, x1, y0, y1, z0, z1):
	"""Invisible collision box (Col_ contract): detailed visuals never collide themselves."""
	return wbox('Col_'+name, x0, x1, y0, y1, z0, z1, 'collision')

# ---------- wall-plane helper ----------
class Wall:
	"""A facade plane: origin on the wall surface, u along the wall, z up, n outward."""
	def __init__(self, origin, u, n):
		self.o, self.u, self.n = Vector(origin), Vector(u).normalized(), Vector(n).normalized()
	def p(self, u, z, n=0.0): return self.o + self.u*u + Vector((0, 0, z)) + self.n*n
	def block(self, name, u0, u1, z0, z1, n0, n1, material, back=True):
		pts = [self.p(u, z, n) for n in (n0, n1) for z in (z0, z1) for u in (u0, u1)]
		return solid(name, pts, material, ('k0',) if back and n0 <= 0.001 else ())

def window(w, name, u, z0, width, height, lit=False, muntins=True, frame='trim_paint'):
	"""Double-hung window: glass in a casing proud of the wall, sill, head, meeting rail and mullion."""
	h = width/2; c = .09
	w.block(('Glow_' if lit else '')+name+'_Glass', u-h, u+h, z0, z0+height, 0, .01, 'glow_warm' if lit else 'glass')
	w.block(name+'_CasL', u-h-c, u-h, z0, z0+height, 0, .05, frame)
	w.block(name+'_CasR', u+h, u+h+c, z0, z0+height, 0, .05, frame)
	w.block(name+'_Head', u-h-c-.04, u+h+c+.04, z0+height, z0+height+.14, 0, .07, frame)
	w.block(name+'_Sill', u-h-c-.05, u+h+c+.05, z0-.07, z0, 0, .09, frame)
	if muntins:
		w.block(name+'_Rail', u-h, u+h, z0+height*.5-.025, z0+height*.5+.025, .01, .035, frame, back=False)
		w.block(name+'_Mull', u-.02, u+.02, z0, z0+height, .01, .03, frame, back=False)

def door(w, name, u, z0, width=1.0, height=2.05, material='door_wood', interactive=False):
	"""Casing around a door; the leaf itself is omitted when an interactive I_ door is placed there."""
	h = width/2; c = .09
	w.block(name+'_CasL', u-h-c, u-h, z0, z0+height, 0, .05, 'trim_paint')
	w.block(name+'_CasR', u+h, u+h+c, z0, z0+height, 0, .05, 'trim_paint')
	w.block(name+'_Head', u-h-c-.04, u+h+c+.04, z0+height, z0+height+.16, 0, .07, 'trim_paint')
	if not interactive:
		w.block(name+'_Leaf', u-h, u+h, z0, z0+height, 0, .02, material)
		w.block(name+'_Lite', u-h+.15, u+h-.15, z0+height*.62, z0+height*.9, .02, .025, 'glass', back=False)

# ---------- roofs ----------
def gable_roof(name, x0, x1, y0, y1, eave, ridge, ridge_along, over=.45, rake=.35, t=.14, siding=None, vents=True):
	"""Two roof slabs with eave and rake overhangs, fascia boards, closed gable walls and rake boards."""
	if ridge_along == 'y':
		half = (x1-x0)/2; xm = (x0+x1)/2; slope = (ridge-eave)/half
		for side, sgn in (('W', -1), ('E', 1)):
			xe = xm+sgn*(half+over); ze = eave-over*slope
			bottom = [(xe, y0-rake, ze), (xm, y0-rake, ridge), (xe, y1+rake, ze), (xm, y1+rake, ridge)]
			solid(f'{name}_Slab{side}', bottom+[(x, y, z+t) for (x, y, z) in bottom], 'roof')
			solid(f'{name}_Fascia{side}', [(xe+sgn*e, y, z) for z in (ze-.16, ze+t) for y in (y0-rake, y1+rake) for e in (0, .04)], 'trim_paint')
		for end, y, sgn in (('S', y0, -1), ('N', y1, 1)):
			if siding: prism(f'{name}_Gable{end}', [(x0, y, eave), (x1, y, eave), (xm, y, ridge)], siding, (0, sgn, 0))
			for side, s in (('W', -1), ('E', 1)):
				a = Vector((xm+s*(half+over), y+sgn*rake, eave-over*slope)); b = Vector((xm, y+sgn*rake, ridge))
				solid(f'{name}_Rake{end}{side}', [(a if i == 0 else b)+Vector((0, sgn*dy, dz)) for dz in (-.18, t) for dy in (0, .04) for i in (0, 1)], 'trim_paint')
			if siding and vents:
				Wall((xm, y, 0), (1, 0, 0), (0, sgn, 0)).block(f'{name}_Vent{end}', -.35, .35, eave+(ridge-eave)*.4, eave+(ridge-eave)*.4+.45, 0, .04, 'lattice')
	else:
		half = (y1-y0)/2; ym = (y0+y1)/2; slope = (ridge-eave)/half
		for side, sgn in (('S', -1), ('N', 1)):
			ye = ym+sgn*(half+over); ze = eave-over*slope
			bottom = [(x0-rake, ye, ze), (x0-rake, ym, ridge), (x1+rake, ye, ze), (x1+rake, ym, ridge)]
			solid(f'{name}_Slab{side}', bottom+[(x, y, z+t) for (x, y, z) in bottom], 'roof')
			solid(f'{name}_Fascia{side}', [(x, ye+sgn*e, z) for z in (ze-.16, ze+t) for e in (0, .04) for x in (x0-rake, x1+rake)], 'trim_paint')
		for end, x, sgn in (('W', x0, -1), ('E', x1, 1)):
			if siding: prism(f'{name}_Gable{end}', [(x, y0, eave), (x, y1, eave), (x, ym, ridge)], siding, (sgn, 0, 0))
			for side, s in (('S', -1), ('N', 1)):
				a = Vector((x+sgn*rake, ym+s*(half+over), eave-over*slope)); b = Vector((x+sgn*rake, ym, ridge))
				solid(f'{name}_Rake{end}{side}', [(a if i == 0 else b)+Vector((sgn*dx, 0, dz)) for dz in (-.18, t) for dx in (0, .04) for i in (0, 1)], 'trim_paint')
			if siding and vents:
				Wall((x, ym, 0), (0, 1, 0), (sgn, 0, 0)).block(f'{name}_Vent{end}', -.35, .35, eave+(ridge-eave)*.4, eave+(ridge-eave)*.4+.45, 0, .04, 'lattice')

# ---------- houses (east side, street facade at x=front facing -X) ----------
def house(name, front, y0, y1, depth, eave, siding, roof='side', ridge=None, windows=(), door_u=0.0,
		door_id=False, porch=None, chimney=None):
	"""windows: (u = world y, sill z, width, height, lit). porch: (y0, y1, depth, deck_z), front gable.
	chimney: (world y of the side wall it hugs, top z)."""
	x0, x1 = front, front+depth
	foot = porch[3] if porch else .55   # the door sill sits at porch-deck height
	wbox(f'{name}_Foundation', x0-.04, x1+.04, y0-.04, y1+.04, 0, foot, 'foundation', skip=('-z',))
	wbox(f'{name}_Body', x0, x1, y0, y1, foot, eave, siding, skip=('-z', '+z'))
	collider(name, x0-.04, x1+.04, y0-.04, y1+.04, 0, eave)
	# Corner boards: two flat boards per corner, proud of the siding.
	for cx, sx in ((x0, -1), (x1, 1)):
		for cy, sy in ((y0, -1), (y1, 1)):
			wbox(f'{name}_CornerX_{cx}_{cy}', min(cx, cx+sx*.035), max(cx, cx+sx*.035), min(cy, cy-sy*.16), max(cy, cy-sy*.16), foot, eave, 'trim_paint', skip=('-z', '+z'))
			wbox(f'{name}_CornerY_{cx}_{cy}', min(cx, cx-sx*.16), max(cx, cx-sx*.16), min(cy, cy+sy*.035), max(cy, cy+sy*.035), foot, eave, 'trim_paint', skip=('-z', '+z'))
	wbox(f'{name}_Frieze', x0-.04, x1+.04, y0-.04, y1+.04, eave-.24, eave, 'trim_paint', skip=('-z', '+z'))
	wbox(f'{name}_Skirt', x0-.03, x1+.03, y0-.03, y1+.03, foot, foot+.14, 'trim_paint', skip=('-z', '+z'))
	if roof == 'side': gable_roof(f'{name}_Roof', x0, x1, y0, y1, eave, ridge, 'y', siding=siding)
	else: gable_roof(f'{name}_Roof', x0, x1, y0, y1, eave, ridge, 'x', siding=siding)
	w = Wall((x0, 0, 0), (0, 1, 0), (-1, 0, 0))
	for i, (u, z, wd, ht, lit) in enumerate(windows): window(w, f'{name}_Win{i}', u, z, wd, ht, lit)
	for side, y, sgn in (('S', y0, -1), ('N', y1, 1)):
		sw = Wall((0, y, 0), (1, 0, 0), (0, sgn, 0))
		for k, frac in enumerate((.3, .72)):
			window(sw, f'{name}_Side{side}{k}', x0+depth*frac, foot+.9, .8, 1.25, False)
			if eave > 5: window(sw, f'{name}_SideUp{side}{k}', x0+depth*frac, eave-1.95, .8, 1.15, False)
	deck = foot
	if porch:
		py0, py1, pd, deck = porch
		px = x0-pd
		wbox(f'{name}_PorchDeck', px, x0, py0, py1, deck-.12, deck, 'trim', skip=('+x',))
		wbox(f'{name}_PorchSkirt', px+.05, x0, py0+.05, py1-.05, 0, deck-.12, 'lattice', skip=('+x', '+z', '-z'))
		collider(f'{name}_Porch', px, x0, py0, py1, 0, deck)
		steps = max(1, round(deck/.19)); rise = deck/steps
		for s in range(1, steps):
			wbox(f'{name}_Step{s}', px-.3*(steps-s), px-.3*(steps-s-1), door_u-.8, door_u+.8, 0, rise*s, 'trim', skip=('-z',))
		ph = deck+2.4
		for k, py in enumerate((py0+.25, py1-.25)):
			wbox(f'{name}_Pier{k}', px+.05, px+.5, py-.22, py+.22, deck, deck+.85, 'brick', skip=('-z',))
			c = Vector((px+.275, py, 0))
			# Craftsman tapered column: wide at the pier, narrow under the beam.
			pts = [c+Vector(((i-.5)*(.28 if k2 == 0 else .17), (j-.5)*(.28 if k2 == 0 else .17), deck+.85 if k2 == 0 else ph))
				for k2 in (0, 1) for j in (0, 1) for i in (0, 1)]
			solid(f'{name}_Post{k}', pts, 'trim_paint', skip=('k0', 'k1'))
			collider(f'{name}_Post{k}', px+.05, px+.5, py-.22, py+.22, deck, ph)
		# Craftsman knee walls clad like the house, with a painted cap, front and sides.
		knee = deck+.82
		walls = [('S', px+.2, px+.34, py0+.47, door_u-.75), ('N', px+.2, px+.34, door_u+.75, py1-.47),
			('SS', px+.5, x0, py0+.05, py0+.19), ('NS', px+.5, x0, py1-.19, py1-.05)]
		for side, xa, xb, ya, yb in walls:
			if max(xb-xa, yb-ya) < .3: continue
			wbox(f'{name}_Knee{side}', xa, xb, ya, yb, deck, knee, siding, skip=('-z', '+z'))
			wbox(f'{name}_KneeCap{side}', xa-.03, xb+.03, ya-.03, yb+.03, knee, knee+.07, 'trim_paint', skip=('-z',))
			collider(f'{name}_Knee{side}', xa, xb, ya, yb, deck, knee+.07)
		wbox(f'{name}_Beam', px+.1, px+.45, py0, py1, ph, ph+.25, 'trim_paint')
		wbox(f'{name}_PorchCeil', px+.1, x0, py0, py1, ph+.25, ph+.3, 'trim', skip=('+x',))
		pr = ph+.3+(py1-py0)/2*.62
		gable_roof(f'{name}_PorchRoof', px-.1, x0+.3, py0, py1, ph+.3, pr, 'x', over=.3, rake=0, siding=None)
		prism(f'{name}_PorchGable', [(px-.1, py0, ph+.3), (px-.1, py1, ph+.3), (px-.1, (py0+py1)/2, pr)], 'trim', (-1, 0, 0))
		wbox(f'{name}_PorchGableBeam', px-.14, px-.1, py0, py1, ph+.12, ph+.3, 'trim_paint', skip=('+x',))
	door(w, f'{name}_Door', door_u, deck, interactive=door_id)
	if chimney:
		cy, top = chimney
		sgn = -1 if abs(cy-y0) < abs(cy-y1) else 1
		cx = x0+depth*.55
		ya, yb = (cy-.6, cy) if sgn < 0 else (cy, cy+.6)
		wbox(f'{name}_Chimney', cx, cx+.75, ya, yb, 0, top, 'brick', skip=('-z',))
		wbox(f'{name}_ChimCap', cx-.06, cx+.81, ya-.06, yb+.06, top, top+.12, 'coping')
		collider(f'{name}_Chimney', cx, cx+.75, ya, yb, 0, 2)

# ---------- storefronts (west side, facade at x=front facing +X) ----------
def storefront(name, front, back, y0, y1, height, wall, display=(), door_y=None, parapet=.5):
	"""display: (y0, y1, lit) bays, each with a kick panel, plate glass, mullions and a transom row."""
	wbox(f'{name}_Body', back, front, y0, y1, .05, height, wall, skip=('-z',))
	collider(name, back, front, y0, y1, 0, height+parapet)
	wbox(f'{name}_Parapet', back-.05, front+.05, y0-.05, y1+.05, height, height+parapet, wall, skip=('-z',))
	wbox(f'{name}_Coping', back-.1, front+.12, y0-.1, y1+.1, height+parapet, height+parapet+.1, 'coping')
	wbox(f'{name}_Cornice', front, front+.24, y0-.05, y1+.05, height-.35, height-.12, 'storefront_wood', skip=('-x',))
	w = Wall((front, 0, 0), (0, 1, 0), (1, 0, 0))
	w.block(f'{name}_SignBand', y0+.4, y1-.4, 2.98, height-.45, 0, .06, 'sign_board')
	w.block(f'{name}_Lintel', y0+.2, y1-.2, 2.75, 2.95, 0, .12, 'storefront_wood')
	for i, (a, b, lit) in enumerate(display):
		w.block(f'{name}_Kick{i}', a, b, .05, .6, 0, .1, 'storefront_wood')
		w.block(('Glow_' if lit else '')+f'{name}_Display{i}', a, b, .6, 2.35, 0, .01, 'glow_warm' if lit else 'glass')
		w.block(f'{name}_Transom{i}', a, b, 2.42, 2.75, 0, .01, 'glass')
		w.block(f'{name}_TransomBar{i}', a, b, 2.35, 2.42, 0, .08, 'storefront_wood')
		w.block(f'{name}_FrameL{i}', a-.08, a, .05, 2.75, 0, .1, 'storefront_wood')
		w.block(f'{name}_FrameR{i}', b, b+.08, .05, 2.75, 0, .1, 'storefront_wood')
		n = max(1, round((b-a)/1.6))
		for k in range(1, n):
			m = a+(b-a)*k/n
			w.block(f'{name}_Mull{i}_{k}', m-.04, m+.04, .6, 2.75, 0, .08, 'storefront_wood')
	if door_y is not None:
		door(w, f'{name}_Door', door_y, .05, 1.05, 2.25)
		w.block(f'{name}_DoorTransom', door_y-.52, door_y+.52, 2.42, 2.75, 0, .01, 'glass')

# ---------- trees: low-poly wood, alpha-cutout foliage (guide 22 §7/§14: no stacked opaque cones) ----------
for name, c in [('maple_orange', (.78,.38,.12)), ('maple_amber', (.89,.60,.24)), ('maple_copper', (.56,.23,.09)),
		('fir_tier', (.12,.18,.14)), ('leaf_litter', (.6,.3,.1))]:
	mat(name, c)
TEXTURED |= {'trunk'}

def raw_mesh(name, verts, faces, uvs, material, normals=None):
	"""Mesh with authored UVs (cards, cones) instead of the planar metric projection.
	normals: optional per-vertex custom normals (foliage lit as a volume, not as flat cards)."""
	me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
	uv = me.uv_layers.new(name='UVMap')
	for poly in me.polygons:
		for li in poly.loop_indices: uv.data[li].uv = uvs[me.loops[li].vertex_index]
	if normals: me.normals_split_custom_set_from_vertices([Vector(n).normalized() for n in normals])
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	o.data.materials.append(mats[material])
	return o

def beam(name, a, b, r0, r1, material, sides=5):
	"""Tapered tube from a to b (trunks and limbs), faces oriented away from the axis, capped at b."""
	a, b = Vector(a), Vector(b); axis = (b-a).normalized()
	side = axis.cross(Vector((0, 0, 1)) if abs(axis.z) < .95 else Vector((1, 0, 0))).normalized(); up = axis.cross(side)
	verts = []
	for p, r in ((a, r0), (b, r1)):
		for k in range(sides):
			t = k*math.tau/sides; verts.append(tuple(p + (side*math.cos(t) + up*math.sin(t))*r))
	faces = []
	for k in range(sides):
		f = [k, (k+1) % sides, sides+(k+1) % sides, sides+k]
		mid = sum((Vector(verts[i]) for i in f), Vector())/4
		axis_pt = a + axis*((mid-a).dot(axis))
		n = (Vector(verts[f[1]])-Vector(verts[f[0]])).cross(Vector(verts[f[2]])-Vector(verts[f[0]]))
		if n.dot(mid-axis_pt) < 0: f.reverse()
		faces.append(f)
	cap = list(range(sides, 2*sides))
	if (Vector(verts[cap[1]])-Vector(verts[cap[0]])).cross(Vector(verts[cap[2]])-Vector(verts[cap[0]])).dot(axis) < 0: cap.reverse()
	faces.append(cap)
	me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
	o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
	return finish(o, material)

def card(name, centre, width, height, yaw, material, volume_centre, pitch=0.0):
	"""Upright cutout card; normals bend away from the crown centre so the crown shades as a mass."""
	c = Vector(centre); u = Vector((math.cos(yaw), math.sin(yaw), 0)); v = Vector((0, 0, 1))
	if pitch: v = (v*math.cos(pitch) + Vector((-math.sin(yaw), math.cos(yaw), 0))*math.sin(pitch)).normalized()
	pts = [c-u*width/2-v*height/2, c+u*width/2-v*height/2, c+u*width/2+v*height/2, c-u*width/2+v*height/2]
	vc = Vector(volume_centre)
	normals = [((p-vc).normalized()*.65 + Vector((0, 0, .35))) for p in pts]
	return raw_mesh(name, [tuple(p) for p in pts], [(0, 1, 2, 3)], [(0, 0), (1, 0), (1, 1), (0, 1)], material, normals)

def maple(name, x, y, h, tint):
	"""Bigleaf maple: flared trunk, four to five limbs, a crown of crossed leaf-clump cards at the limb ends."""
	fork = h*rng.uniform(.34, .42)
	beam(f'C_{name}_Trunk', (x, y, -.05), (x+rng.uniform(-.15, .15), y+rng.uniform(-.15, .15), fork), .24, .15, 'trunk', 6)
	top = Vector((x, y, fork))
	crown = Vector((x, y, h*.66)); R = h*.34
	limbs = rng.randint(4, 5)
	ends = []
	for k in range(limbs):
		a = k*math.tau/limbs + rng.uniform(-.4, .4); reach = R*rng.uniform(.45, .75)
		end = Vector((x+math.cos(a)*reach, y+math.sin(a)*reach, h*rng.uniform(.6, .82)))
		beam(f'{name}_Limb{k}', top, end, .11, .04, 'trunk', 4)
		ends.append(end)
	ends.append(Vector((x, y, h*.9)))
	clumps = []
	for e in ends:
		clumps.append(e)
		for _ in range(3):
			clumps.append(e + Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-.5, .7)))*R*.38)
	for k, p in enumerate(clumps):
		s = h*rng.uniform(.33, .43)
		yaw = rng.uniform(0, math.pi)
		material = tint if rng.random() < .7 else rng.choice(('maple_orange', 'maple_amber', 'maple_copper'))
		card(f'{name}_Clump{k}a', p, s, s*.9, yaw, material, crown, rng.uniform(-.2, .2))
		card(f'{name}_Clump{k}b', p, s, s*.9, yaw+math.pi/2, material, crown, rng.uniform(-.2, .2))
	# Fallen leaves gathered under the crown.
	for k in range(3):
		a = rng.uniform(0, math.tau); r = rng.uniform(.3, R*.6)
		litter(f'{name}_Litter{k}', x+math.cos(a)*r, y+math.sin(a)*r, .145, rng.uniform(1.6, 2.6))

def fir(name, x, y, h):
	"""Douglas fir: thin trunk and ten to twelve drooping tiers, each an open cone wrapped with a
	needle texture whose alpha fringe makes the ragged branch tips."""
	beam(f'{name}_Trunk', (x, y, -.1), (x, y, h*.92), max(.12, h*.018), .04, 'trunk', 5)
	tiers = rng.randint(10, 12)
	base_r = h*rng.uniform(.2, .25)
	sides = 8
	verts, faces, uvs, normals = [], [], [], []
	for k in range(tiers):
		t = k/(tiers-1)                        # 0 top .. 1 bottom
		r = base_r*(.18 + .82*t**.85)*rng.uniform(.9, 1.1)
		apex_z = h*(1.0 - .8*t) + (.25 if k == 0 else 0)
		# Each tier droops past the next apex, so no trunk shows between tiers (no pagoda look).
		spacing = h*.8/(tiers-1)
		drop = max(r*rng.uniform(.8, 1.0), spacing*rng.uniform(1.7, 2.0))
		apex = Vector((x+rng.uniform(-.08, .08), y+rng.uniform(-.08, .08), apex_z))
		phase = rng.uniform(0, math.tau)
		for s in range(sides):
			a0, a1 = phase+s*math.tau/sides, phase+(s+1)*math.tau/sides
			ra, rb = r*rng.uniform(.88, 1.08), r*rng.uniform(.88, 1.08)
			p0 = Vector((x+math.cos(a0)*ra, y+math.sin(a0)*ra, apex_z-drop))
			p1 = Vector((x+math.cos(a1)*rb, y+math.sin(a1)*rb, apex_z-drop))
			i = len(verts)
			verts += [tuple(apex), tuple(p1), tuple(p0)]
			u0 = (s % 4)/4; u1 = u0+.25
			uvs += [((u0+u1)/2, 1), (u1, 0), (u0, 0)]
			faces.append((i, i+1, i+2))
			for p in (apex, p1, p0):
				out = Vector((p.x-x, p.y-y, 0))
				normals.append((out.normalized() if out.length > .01 else Vector()) * .7 + Vector((0, 0, .5)))
	raw_mesh(f'{name}_Tiers', verts, faces, uvs, 'fir_tier', normals)

def litter(name, x, y, z, size):
	"""Flat decal of fallen leaves, 1 cm above the surface it lies on."""
	a = rng.uniform(0, math.tau); c, s = math.cos(a)*size/2, math.sin(a)*size/2
	pts = [(x-c+s, y-s-c, z+.01), (x+c+s, y+s-c, z+.01), (x+c-s, y+s+c, z+.01), (x-c-s, y-s+c, z+.01)]
	return raw_mesh(name, pts, [(0, 1, 2, 3)], [(0, 0), (1, 0), (1, 1), (0, 1)], 'leaf_litter', [(0, 0, 1)]*4)
