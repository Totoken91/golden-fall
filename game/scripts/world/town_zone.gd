class_name TownZone
extends Node3D

# Morrow Creek main street, Morrow Diner and its service alley (Stage 1 blockout).
# Lives in the same 3D world as the bedroom, 200 m away, so walking between the street and the
# diner never loads anything; only the house door fades (bedroom <-> porch).
# Name contracts come from scripts/assets/build_town.py.
const ORIGIN := Vector3(200,0,0)
# Areas in town-local Godot coordinates (Blender X, Z, -Y): x range, z range.
const DINER := Rect2(-14.5,-62,8,12)      # x -14.5..-6.5, z -62..-50 (door at z -51.8..-50.6)
const ALLEY := Rect2(-22.5,-65.5,16,3.5)  # x -22.5..-6.5, z -65.5..-62
const GLOW := {"glow_warm":.55,"neon":1.1,"lamp_head":1.0,"service_light":.9}

var game: Node
var model: Node3D
var doors := {}
var door_open := {}
var rain: MultiMeshInstance3D
var textured := {}   # blockout material name -> real textured material (game/data/town_materials.json)

func _init(controller: Node) -> void:
	game = controller
	name = "Town"
	position = ORIGIN

func build() -> void:
	model = load("res://assets/town/town.glb").instantiate()
	add_child(model)
	load_materials()
	prepare(model)
	build_rain()

# Real Poly Haven / ambientCG materials bound by blockout material name. Town UVs are authored in
# metres, so one UV unit = 1 m and the scale is 1 / source tile. Tints come from the moodboard.
func load_materials() -> void:
	var config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/town_materials.json"))
	var period: Array = config.uv_period_m
	for name in config.bindings:
		var binding: Dictionary = config.bindings[name]
		var material := (load(binding.material) as StandardMaterial3D).duplicate() as StandardMaterial3D
		var tile: Array = binding.tile_m
		material.uv1_scale = Vector3(float(period[0])/float(tile[0]),float(period[1])/float(tile[1]),1)
		var tint: Array = binding.tint
		material.albedo_color = Color(tint[0],tint[1],tint[2])
		material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
		if binding.wet:
			# Rain-soaked asphalt: a soft sheen that catches the sodium lamps.
			material.roughness = .8
			material.metallic_specular = .35
		else:
			material.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
		material.resource_name = name
		textured[name] = material

func prepare(node: Node) -> void:
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		var id := str(mi.name)
		for i in mi.mesh.get_surface_count():
			var source := mi.get_active_material(i) as StandardMaterial3D
			if source == null: continue
			if textured.has(str(source.resource_name)):
				mi.set_surface_override_material(i,textured[str(source.resource_name)])
				continue
			var material := source.duplicate() as StandardMaterial3D
			material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
			material.roughness = .95
			material.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
			# Blender's emission strengths blow out to white under the linear tonemap: keep glows warm.
			if material.emission_enabled:
				material.emission_energy_multiplier = GLOW.get(str(source.resource_name),.8)
			mi.set_surface_override_material(i,material)
		if id.begins_with("C_") or id.begins_with("I_"): mi.create_trimesh_collision()
		if id.begins_with("Ramp_"):
			# Collision-only wedges over curbs and the porch step; both faces collide (mirrored sides).
			mi.create_trimesh_collision()
			for shape in mi.find_children("*","CollisionShape3D",true,false):
				(shape.shape as ConcavePolygonShape3D).backface_collision = true
			mi.visible = false
		if id.begins_with("I_"):
			var interaction := id.split("_")[1]
			mi.set_meta("interaction",interaction)
			if interaction in ["dinerdoor","homedoor"]: doors[interaction] = mi
		if id.begins_with("Lamp_"): add_lamp(mi)
		if id.begins_with("Vis_spruce") or id.begins_with("Vis_leaf"): mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for child in node.get_children(): prepare(child)

func add_lamp(mi: MeshInstance3D) -> void:
	var light := OmniLight3D.new()
	var center := mi.get_aabb().get_center()
	light.position = center+Vector3(0,-.25,0)
	var id := str(mi.name)
	if id.begins_with("Lamp_Street"):
		light.light_color = Color("ffae55")
		light.light_energy = 1.7
		light.omni_range = 10.0
	elif id.begins_with("Lamp_Diner"):
		light.light_color = Color("ffd39a")
		light.light_energy = 1.3
		light.omni_range = 7.0
	else:
		light.light_color = Color("ffcf8f")
		light.light_energy = 1.1
		light.omni_range = 5.5
	light.omni_attenuation = 1.4
	light.shadow_enabled = false
	mi.add_child(light)

# Rain that follows the player outdoors: 420 streaks in a 26 x 12 x 26 m box, animated in the shader.
func build_rain() -> void:
	rain = MultiMeshInstance3D.new()
	rain.name = "TownRain"
	var quad := QuadMesh.new()
	quad.size = Vector2(.012,.32)
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_custom_data = true
	multimesh.mesh = quad
	multimesh.instance_count = 420
	var rng := RandomNumberGenerator.new()
	rng.seed = 151003
	for i in multimesh.instance_count:
		multimesh.set_instance_transform(i,Transform3D(Basis(Vector3.BACK,rng.randf_range(-.12,.02)),Vector3(rng.randf_range(-13,13),0,rng.randf_range(-13,13))))
		multimesh.set_instance_custom_data(i,Color(rng.randf(),rng.randf_range(.75,1.25),rng.randf_range(.35,.8),0))
	multimesh.custom_aabb = AABB(Vector3(-14,-1,-14),Vector3(28,14,28))
	rain.multimesh = multimesh
	var material := ShaderMaterial.new()
	material.shader = load("res://shaders/rain_follow.gdshader")
	rain.material_override = material
	rain.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(rain)

func area_of(world_position: Vector3) -> String:
	var p := world_position-ORIGIN
	if DINER.has_point(Vector2(p.x,p.z)): return "diner"
	if ALLEY.has_point(Vector2(p.x,p.z)): return "alley"
	return "street"

func _process(_delta: float) -> void:
	if not visible or not is_instance_valid(game.walker): return
	var p: Vector3 = game.walker.global_position-ORIGIN
	rain.position = Vector3(snappedf(p.x,2.0),p.y,snappedf(p.z,2.0))
	rain.visible = area_of(game.walker.global_position) != "diner"

func toggle_door(id: String) -> void:
	var mesh: MeshInstance3D = doors.get(id)
	if mesh == null: return
	# The pivot is the door's hinge edge: rotate the mesh about it.
	if not mesh.has_meta("hinge"):
		var box := mesh.get_aabb()
		mesh.set_meta("hinge",Vector3(box.position.x+box.size.x*.5,0,box.position.z))
		mesh.set_meta("closed",mesh.transform)
	var opening: bool = not door_open.get(id,false)
	door_open[id] = opening
	var hinge: Vector3 = mesh.get_meta("hinge")
	var closed: Transform3D = mesh.get_meta("closed")
	var target := closed
	if opening:
		var swing := Transform3D(Basis(Vector3.UP,deg_to_rad(-100)),Vector3.ZERO)
		target = closed*Transform3D.IDENTITY.translated(hinge)*swing*Transform3D.IDENTITY.translated(-hinge)
	create_tween().tween_property(mesh,"transform",target,.45).set_trans(Tween.TRANS_SINE)

func is_open(id: String) -> bool: return door_open.get(id,false)

# Spawn points in world coordinates with a look target.
func porch_spawn() -> Array: return [ORIGIN+Vector3(6.9,.4,0),ORIGIN+Vector3(-4,1.4,0)]
