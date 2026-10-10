"""Golden Fall Stage 1 blockout: Morrow Creek main street, Morrow Diner and its service alley.

Run: blender -b --python-exit-code 1 -P scripts/assets/build_town.py
Blender coordinates (metres): X east, Y north, Z up. The street runs along +Y.
Godot receives X, Z->Y, -Y->Z. Volumes, scale and route first: flat colours here, real
textures come in the art pass (docs/legacy_heures_creuses/22_GUIDE_CREATION_ZONES.md).

Name contracts used by game/scripts/world/town_zone.gd:
  C_*  static collision          I_<id>_*  interactive (id = second token)
  Lamp_*  sodium light position  Glow_*   warm emissive window/sign
  Spawn_* empties: player spawn points
"""
from pathlib import Path
import bpy, math, random, json
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'game/assets/town'
SOURCE = ROOT/'assets/blender'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
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
	('roof', (.12,.10,.09), 0), ('trim', (.70,.66,.56), 0), ('door_wood', (.25,.14,.07), 0),
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

def finish(o, material, tile=1.0):
	"""World-space planar UVs (metres / tile), like build_room.py."""
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

# ---------- ground ----------
box('C_Road', -4, 4, -22, 98, -.2, 0, 'asphalt', 4)
for y in range(-20, 96, 6): box(f'RoadLine_{y}', -.06, .06, y, y+3, 0, .005, 'road_line')
for side in (-1, 1):
	x0, x1 = (4, 6.5) if side > 0 else (-6.5, -4)
	box(f'C_Sidewalk_{side}', x0, x1, -22, 98, -.2, .15, 'sidewalk', 1.5)
	box(f'C_Curb_{side}', (4 if side > 0 else -4.15), (4.15 if side > 0 else -4), -22, 98, -.2, .16, 'curb')
	box(f'C_Lawn_{side}', (6.5 if side > 0 else -40), (40 if side > 0 else -6.5), -30, 105, -.2, .14, 'lawn', 3)
	ramp(f'Ramp_Curb_{side}', 3.55*side, 4.0*side, -22, 98, 0, .16)
# Fallen-leaf drifts in the gutters and on lawns (flat, no collision).
for i in range(40):
	side = rng.choice((-1, 1)); x = side*rng.uniform(3.6, 4.0) if i < 24 else side*rng.uniform(7, 14)
	y = rng.uniform(-18, 94); s = rng.uniform(.6, 1.8)
	box(f'Leaves_{i}', x-s/2, x+s/2, y-s, y+s, .0, .02 if i < 24 else .07, 'leaves_ground')

# ---------- player's house (east, porch faces the street) ----------
box('C_HomeBody', 8, 17, -7, 7, .05, 6.0, 'siding_cream', 2)
gable('Roof_Home', 7.6, 17.4, -7.4, 7.4, 6.0, 8.6, 'roof')
box('C_HomePorch', 6.5, 8.0, -2.4, 2.4, .05, .38, 'trim')
box('C_HomeStep', 6.0, 6.5, -1.0, 1.0, .05, .26, 'trim')
ramp('Ramp_Porch', 5.5, 6.5, -1.0, 1.0, .15, .38)
box('HomePorchRoof', 6.4, 8.0, -2.6, 2.6, 2.75, 2.9, 'roof')
for y in (-2.3, 2.3): cyl(f'C_HomePost_{y}', 6.6, y, .38, 2.75, .07, 'trim', 6)
box('I_homedoor_Door', 7.94, 8.0, -.5, .5, .38, 2.45, 'door_wood')
for y, z, lit in [(-4.2, 1.4, False), (4.2, 1.4, True), (-4.2, 4.0, True), (0, 4.0, False), (4.2, 4.0, False)]:
	box(('Glow_' if lit else '')+f'HomeWin_{y}_{z}', 7.97, 8.0, y-.6, y+.6, z, z+1.25, 'glow_warm' if lit else 'window_dark')
	box(f'HomeTrim_{y}_{z}', 7.95, 7.99, y-.7, y+.7, z-.1, z+1.35, 'trim')
empty('Spawn_porch', (6.9, 0, .38), 90)          # looking west at the street
empty('Spawn_bedroom_door', (0, 0, 0), 0)          # marker only; bedroom spawn lives in Godot

# ---------- neighbours (east) ----------
for i, (y0, y1, siding) in enumerate([(15, 27, 'siding_sage'), (34, 46, 'siding_rust'), (72, 84, 'siding_cream')]):
	box(f'C_House_{i}', 10, 18, y0, y1, .05, 5.4, siding, 2)
	gable(f'Roof_House_{i}', 9.6, 18.4, y0-.4, y1+.4, 5.4, 7.6, 'roof')
	box(f'C_HousePorch_{i}', 8.6, 10, (y0+y1)/2-2, (y0+y1)/2+2, .05, .35, 'trim')
	box(f'HouseDoor_{i}', 9.95, 10.0, (y0+y1)/2-.5, (y0+y1)/2+.5, .35, 2.4, 'door_wood')
	for dy in (-3.5, 3.5):
		lit = rng.random() < .5
		box(('Glow_' if lit else '')+f'HouseWin_{i}_{dy}', 9.97, 10.0, (y0+y1)/2+dy-.6, (y0+y1)/2+dy+.6, 1.3, 2.5, 'glow_warm' if lit else 'window_dark')

# ---------- Morrow Records (west) ----------
box('C_Records', -16, -6.5, 22, 34, .05, 4.6, 'brick', 1.2)
box('RecordsParapet', -16.1, -6.4, 21.9, 34.1, 4.6, 5.0, 'brick_dark')
box('Glow_RecordsWindow', -6.53, -6.48, 23.5, 30.5, .8, 2.7, 'glow_warm')
box('RecordsDoor', -6.53, -6.47, 31.2, 32.4, .15, 2.3, 'door_wood')
box('RecordsSign', -6.45, -6.3, 23, 33, 3.2, 4.1, 'sign_board')

# ---------- Morrow Diner (west): 8 x 12 m, entrance on the street side ----------
DX0, DX1, DY0, DY1, DH, T = -14.5, -6.5, 50, 62, 3.4, .25
box('C_DinerFloor', DX0, DX1, DY0, DY1, -.1, .15, 'diner_floor', .6)
box('C_DinerWall_W', DX0, DX0+T, DY0, DY1, .15, DH, 'brick', 1.2)
box('C_DinerWall_S', DX0, DX1, DY0, DY0+T, .15, DH, 'diner_enamel', 1)
box('C_DinerWall_N', DX0, DX1, DY1-T, DY1, .15, DH, 'brick', 1.2)
# East (street) facade: low wall, window band, header. The door sits at the south end so it
# opens onto a clear entry, not onto a booth (caught by the traversal test).
DOOR0, DOOR1 = 50.6, 51.8
for a, b in [(DY0, DOOR0), (DOOR1, DY1)]:
	box(f'C_DinerWall_E_low_{a}', DX1-T, DX1, a, b, .15, 1.0, 'diner_red')
	box(f'Glow_DinerWindow_{a}', DX1-T*.6, DX1-T*.4, a+.15, b-.15, 1.0, 2.5, 'glow_warm')
	box(f'C_DinerWindowPane_{a}', DX1-T*.55, DX1-T*.45, a, b, 1.0, 2.5, 'window_dark')
	for y in range(int(a)+1, int(b), 2): box(f'DinerMullion_{a}_{y}', DX1-T, DX1, y-.05, y+.05, 1.0, 2.5, 'chrome')
box('C_DinerWall_E_head', DX1-T, DX1, DY0, DY1, 2.5, DH, 'diner_enamel')
box('DinerChromeBand', DX1-.02, DX1+.02, DY0, DY1, 2.55, 2.7, 'chrome')
box('C_DinerRoof', DX0-.1, DX1+.1, DY0-.1, DY1+.1, DH, DH+.25, 'roof')
box('DinerParapet', DX1-.1, DX1+.12, DY0-.1, DY1+.1, DH+.25, DH+.7, 'diner_enamel')
box('DinerAwning', DX1, DX1+1.3, DY0+.3, DY1-.3, 2.75, 2.85, 'diner_red')
box('Glow_DinerSign', DX1+.12, DX1+.22, 53.5, 60.5, DH+.8, DH+1.6, 'neon')
box('DinerSignBack', DX1, DX1+.12, 53.3, 60.7, DH+.7, DH+1.7, 'metal_dark')
# Interactive front door, hinged on its north edge (town_zone.gd swings it).
box('I_dinerdoor_Door', DX1-.12, DX1-.06, DOOR0, DOOR1, .15, 2.35, 'chrome')
# Interior: counter along the west side, stools, back bar, three window booths, kitchen partition.
box('C_Counter', -12.1, -11.3, 51.0, 57.6, .15, 1.05, 'diner_red')
box('CounterTop', -12.2, -11.2, 50.9, 57.7, 1.05, 1.12, 'counter_top')
for i, y in enumerate((51.6, 52.7, 53.8, 54.9, 56.0, 57.1)):
	cyl(f'StoolPost_{i}', -10.75, y, .15, .72, .05, 'chrome', 6)
	cyl(f'StoolSeat_{i}', -10.75, y, .72, .8, .2, 'booth_red', 8)
box('C_BackBar', -14.25, -13.6, 50.5, 58.0, .15, 1.0, 'wood_table')
box('BackBarTop', -14.3, -13.5, 50.4, 58.1, 1.0, 1.05, 'counter_top')
box('CoffeeMachine', -14.2, -13.7, 51.2, 52.0, 1.05, 1.6, 'chrome')
box('Glow_SpecialsBoard', -14.24, -14.2, 53.5, 56.0, 1.6, 2.6, 'glow_warm')
box('C_KitchenPartition', DX0+T, -9.0, 59.5, 59.7, .15, DH, 'diner_enamel')
box('KitchenSwingDoor', -10.9, -10.0, 59.45, 59.75, .3, 2.1, 'chrome')
for i, y in enumerate((53.3, 55.6, 57.9)):
	box(f'C_BoothSeatS_{i}', -8.4, -6.85, y-1.0, y-.45, .15, .62, 'booth_red')
	box(f'BoothBackS_{i}', -8.4, -6.85, y-1.05, y-.9, .62, 1.25, 'booth_red')
	box(f'C_BoothSeatN_{i}', -8.4, -6.85, y+.45, y+1.0, .15, .62, 'booth_red')
	box(f'BoothBackN_{i}', -8.4, -6.85, y+.9, y+1.05, .62, 1.25, 'booth_red')
	box(f'C_BoothTable_{i}', -8.2, -6.85, y-.35, y+.35, .72, .78, 'wood_table')
	cyl(f'BoothTableLeg_{i}', -7.5, y, .15, .72, .05, 'chrome', 6)
for i, y in enumerate((52.5, 56.0)):
	box(f'Lamp_DinerCeiling_{i}', -11.0, -10.4, y-.3, y+.3, DH-.25, DH-.15, 'glow_warm')
empty('Spawn_diner_inside', (-7.6, 51.2, .15), 90)  # just inside the door, facing west
empty('Seat_hannah', (-7.6, 57.9, .15), 0)        # Hannah's window booth (stage 2)
empty('Spot_june', (-12.8, 54.5, .15), -90)        # June behind the counter (stage 2)

# ---------- service alley: north of the diner, 15.5 m to a fence ----------
AY0, AY1 = DY1, 65.5
box('C_AlleyGround', -22.5, -6.5, AY0, AY1, -.2, .14, 'asphalt', 3)
box('C_Hardware', -16, -6.5, AY1, 80, .05, 4.2, 'cinder', 1.5)
box('HardwareParapet', -16.1, -6.4, AY1-.1, 80.1, 4.2, 4.6, 'cinder')
box('HardwareWindow', -6.53, -6.48, 68, 77, .8, 2.6, 'window_dark')
box('HardwareSign', -6.45, -6.3, 68.5, 76.5, 3.0, 3.8, 'sign_board')
box('C_AlleyFence', -22.6, -22.4, AY0-1.5, AY1+1.5, .03, 2.2, 'fence_wood', .5)
for y in (AY0-1.2, AY0+1.0, AY0+3.0, AY1+1.2): cyl(f'FencePost_{y}', -22.5, y, .03, 2.3, .07, 'pole_wood', 6)
box('C_AlleyBackWall', -22.4, -16, AY0-6, AY0-5.8, .03, 2.0, 'fence_wood', .5)  # closes behind the diner
box('C_Dumpster', -18.4, -16.6, AY0+.25, AY0+1.45, .03, 1.25, 'dumpster')
box('DumpsterLid', -18.5, -16.5, AY0+.2, AY0+1.5, 1.25, 1.32, 'metal_dark')
box('I_servicedoor_Door', -12.6, -11.6, DY1-.02, DY1+.04, .03, 2.15, 'metal_dark')
box('Lamp_ServiceLight', -12.35, -11.85, DY1, DY1+.25, 2.45, 2.6, 'service_light')
box('ExhaustFan', -9.6, -8.6, DY1, DY1+.45, 2.4, 3.1, 'metal_dark')
cyl('DrainPipe', -14.2, DY1+.1, .03, DH+.2, .06, 'metal_dark', 6)
box('Puddle', -15.5, -13.0, AY0+1.6, AY0+3.0, .03, .035, 'window_dark')

# ---------- streetlamps, poles and wires ----------
for i, (x, y) in enumerate([(5.8, 4), (5.8, 26), (5.8, 48), (5.8, 70), (5.8, 90), (-5.8, 15), (-5.8, 37), (-5.8, 48), (-5.8, 82)]):
	s = 1 if x > 0 else -1
	cyl(f'C_LampPost_{i}', x, y, .15, 5.6, .08, 'metal_dark', 6)
	box(f'LampArm_{i}', min(x, x-s*1.4), max(x, x-s*1.4), y-.04, y+.04, 5.5, 5.6, 'metal_dark')
	box(f'Lamp_Street_{i}', x-s*1.55, x-s*1.15, y-.18, y+.18, 5.38, 5.5, 'lamp_head')
poles = [(7.2, y) for y in range(-15, 100, 24)]
for i, (x, y) in enumerate(poles):
	cyl(f'C_TelePole_{i}', x, y, .05, 8.5, .13, 'pole_wood', 6)
	box(f'TeleCross_{i}', x-1.2, x+1.2, y-.06, y+.06, 7.9, 8.05, 'pole_wood')
for i in range(len(poles)-1):
	(x, y), (_, y2) = poles[i], poles[i+1]
	for dx in (-1.0, 1.0):
		box(f'Wire_{i}_{dx}', x+dx-.012, x+dx+.012, y, y2, 7.75, 7.77, 'wire')

# ---------- parked cars (1990s sedans / wagon), low poly ----------
def car(name, x, y, colour, wagon=False):
	box(f'C_{name}_Body', x-.9, x+.9, y-2.3, y+2.3, .32, .95, colour)
	cy0, cy1 = (y-1.2, y+2.0) if wagon else (y-1.0, y+1.1)
	box(f'{name}_Cabin', x-.82, x+.82, cy0, cy1, .95, 1.42, colour)
	box(f'{name}_Glass', x-.84, x+.84, cy0+.12, cy1-.12, 1.0, 1.36, 'window_dark')
	for wx in (x-.88, x+.88):
		for wy in (y-1.45, y+1.45):
			bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=.33, depth=.22, location=(wx, wy, .33), rotation=(0, math.pi/2, 0))
			w = bpy.context.object; w.name = f'{name}_Wheel'; bpy.ops.object.transform_apply(rotation=True); finish(w, 'tyre')
car('CarRust', 3.0, 20, 'car_rust')
car('CarCream', -3.0, 44, 'car_cream', wagon=True)
car('CarGreen', -3.0, 64.5, 'car_green')

# ---------- trees: orange deciduous along lawns, dark spruce walls ----------
def deciduous(name, x, y, h):
	cyl(f'C_{name}_Trunk', x, y, 0, h*.55, .16, 'trunk', 6, .1)
	for k in range(3):
		ox, oy, oz = rng.uniform(-.8, .8), rng.uniform(-.8, .8), h*(.55+.13*k)
		bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=h*rng.uniform(.22, .3), location=(x+ox, y+oy, oz))
		c = bpy.context.object; c.name = f'{name}_Crown_{k}'; c.scale = (1, 1, .8); bpy.ops.object.transform_apply(scale=True)
		finish(c, rng.choice(('leaf_orange', 'leaf_amber', 'leaf_copper')))
def spruce(name, x, y, h):
	cyl(f'{name}_Trunk', x, y, 0, h*.25, .14, 'trunk', 5)
	for k, (z0, r) in enumerate([(.18, .30), (.42, .22), (.65, .14)]):
		cyl(f'{name}_Tier_{k}', x, y, h*z0, h*(z0+.42), h*r, 'spruce', 6, 0)
for i, (x, y) in enumerate([(7.6, 11), (7.6, 31), (8.2, 52), (7.6, 60), (8.0, 88), (-7.4, 19), (-7.6, 42), (-7.2, 86)]):
	deciduous(f'Maple_{i}', x, y, rng.uniform(5.5, 7.5))
i = 0
for x0, x1, y0, y1 in [(22, 40, -30, 105), (-40, -24, -30, 105), (-20, 20, 100, 115), (-20, 20, -38, -26)]:
	for _ in range(int(abs(x1-x0)*abs(y1-y0)/38)):
		spruce(f'Spruce_{i}', rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(9, 16)); i += 1
for x, y in [(-20, 40), (-19, 47), (-25, 58), (-26, 66), (20, 30), (21, 60), (19, -5)]:
	spruce(f'Spruce_{i}', x, y, rng.uniform(10, 14)); i += 1

# ---------- bounds: guardrails at both road ends, rail fences at lawn edges ----------
for y in (-21.5, 97.5):
	box(f'C_Guardrail_{y}', -6.5, 6.5, y-.1, y+.1, .45, .8, 'guardrail')
	for x in range(-6, 7, 2): box(f'GuardPost_{y}_{x}', x-.06, x+.06, y-.06, y+.06, 0, .8, 'metal_dark')
for x in (22, -24):
	box(f'C_LawnFence_{x}', x-.06, x+.06, -21.5, 97.5, .05, 1.1, 'fence_wood', .5)
box('C_LawnFence_S_E', 6.5, 22, -21.6, -21.4, .05, 1.1, 'fence_wood', .5)
box('C_LawnFence_S_W', -24, -6.5, -21.6, -21.4, .05, 1.1, 'fence_wood', .5)
box('C_LawnFence_N_E', 6.5, 22, 97.4, 97.6, .05, 1.1, 'fence_wood', .5)
box('C_LawnFence_N_W', -24, -16, 97.4, 97.6, .05, 1.1, 'fence_wood', .5)
box('C_BehindStores_W', -16.2, -16.0, 22, 50, .05, 2.0, 'fence_wood', .5)
box('C_BehindStores_W2', -16.2, -16.0, 80, 97.5, .05, 2.0, 'fence_wood', .5)

# ---------- save source, export GLB, report ----------
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'town_blockout.blend'))

# Runtime export: join static meshes per material (collision and visual-only separately) so the
# street costs a few dozen draw calls instead of ~900. Interactive objects and lamps stay single.
groups = {}
for o in [o for o in bpy.data.objects if o.type == 'MESH']:
	if o.name.startswith(('I_', 'Lamp_', 'Ramp_')): continue
	kind = 'C' if o.name.startswith('C_') else 'Vis'
	groups.setdefault((kind, o.data.materials[0].name), []).append(o)
for (kind, material), objs in groups.items():
	bpy.ops.object.select_all(action='DESELECT')
	for o in objs: o.select_set(True)
	bpy.context.view_layer.objects.active = objs[0]
	if len(objs) > 1: bpy.ops.object.join()
	objs[0].name = f'{kind}_{material}'
bpy.ops.export_scene.gltf(filepath=str(OUT/'town.glb'), export_format='GLB', export_apply=True, export_yup=True)
tris = sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
report = {'objects': len([o for o in bpy.data.objects if o.type == 'MESH']), 'triangles': tris,
	'collisions': len([o for o in bpy.data.objects if o.name.startswith('C_')]),
	'interactive': sorted({o.name.split('_')[1] for o in bpy.data.objects if o.name.startswith('I_')}),
	'lamps': len([o for o in bpy.data.objects if o.name.startswith('Lamp_')])}
(ROOT/'assets/exported').mkdir(parents=True, exist_ok=True)
(ROOT/'assets/exported/town_report.json').write_text(json.dumps(report, indent=2))
print('TOWN', json.dumps(report))
