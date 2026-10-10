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
		material.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
		material.resource_name = name
		textured[name] = material
		if float(binding.wet) > 0:
			# Soaked ground: same real maps, water darkening, puddles, ripples, lamp glints.
			var wet := ShaderMaterial.new()
			wet.shader = preload("res://shaders/wet_ground.gdshader")
			wet.set_shader_parameter("albedo_tex",material.albedo_texture)
			wet.set_shader_parameter("normal_tex",material.normal_texture)
			wet.set_shader_parameter("tint",material.albedo_color)
			wet.set_shader_parameter("uv_scale",Vector2(material.uv1_scale.x,material.uv1_scale.y))
			wet.set_shader_parameter("puddles",float(binding.wet))
			wet.resource_name = name
			textured[name] = wet
	# Cutout foliage: alpha scissor, both faces, no specular; card normals are authored in Blender.
	for name in config.get("foliage",{}):
		var leaves := StandardMaterial3D.new()
		leaves.albedo_texture = load(config.foliage[name])
		leaves.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		leaves.alpha_scissor_threshold = .5
		leaves.cull_mode = BaseMaterial3D.CULL_DISABLED
		leaves.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
		leaves.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
		leaves.roughness = 1.0
		leaves.resource_name = name
		textured[name] = leaves

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
		if id.begins_with("Col_"):
			# Simple invisible boxes standing in for the detailed facades, porches and posts.
			mi.create_trimesh_collision()
			mi.visible = false
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
		if id.begins_with("Vis_leaf_litter"): mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for child in node.get_children(): prepare(child)

func add_lamp(mi: MeshInstance3D) -> void:
	var light := OmniLight3D.new()
	var center := mi.get_aabb().get_center()
	light.position = center+Vector3(0,-.25,0)
	var id := str(mi.name)
	if id.begins_with("Lamp_Street"):
		light.light_color = Color("ffa04a")
		light.light_energy = 3.4
		light.omni_range = 13.0
		add_lamp_shaft(mi,light.position)
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

# Wet-air bloom around each streetlamp head. No light-shaft mesh: the real rain streaks catch the
# lamp light themselves (rain_follow.gdshader light()), so every drop keeps the same fall and size.
func add_lamp_shaft(mi: MeshInstance3D, head: Vector3) -> void:
	var halo := MeshInstance3D.new()
	var quad := QuadMesh.new()
	quad.size = Vector2(2.6,2.6)
	halo.mesh = quad
	halo.position = head+Vector3(0,.1,0)
	halo.material_override = halo_material
	halo.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.add_child(halo)

var halo_material := ShaderMaterial.new()
var splashes: MultiMeshInstance3D
var curtains: Array[MeshInstance3D] = []

# Rain around the player: 1,400 lit streaks in a 28 m box, splash crowns on the ground, and two
# open cylinders of distant rain sheets. All animated in shaders; the nodes only follow the player.
func build_rain() -> void:
	halo_material.shader = preload("res://shaders/lamp_halo.gdshader")
	var rng := RandomNumberGenerator.new()
	rng.seed = 151003
	rain = MultiMeshInstance3D.new()
	rain.name = "TownRain"
	var quad := QuadMesh.new()
	quad.size = Vector2(.014,.38)
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_custom_data = true
	multimesh.mesh = quad
	multimesh.instance_count = 1400
	for i in multimesh.instance_count:
		multimesh.set_instance_transform(i,Transform3D(Basis.IDENTITY,Vector3(rng.randf_range(-14,14),0,rng.randf_range(-14,14))))
		multimesh.set_instance_custom_data(i,Color(rng.randf(),rng.randf_range(.8,1.25),rng.randf_range(.25,1.0),0))
	multimesh.custom_aabb = AABB(Vector3(-16,-1,-16),Vector3(32,14,32))
	rain.multimesh = multimesh
	var material := ShaderMaterial.new()
	material.shader = preload("res://shaders/rain_follow.gdshader")
	rain.material_override = material
	rain.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(rain)
	splashes = MultiMeshInstance3D.new()
	splashes.name = "TownSplashes"
	var splash_mm := MultiMesh.new()
	splash_mm.transform_format = MultiMesh.TRANSFORM_3D
	splash_mm.use_custom_data = true
	splash_mm.mesh = QuadMesh.new()
	splash_mm.instance_count = 360
	for i in splash_mm.instance_count:
		splash_mm.set_instance_custom_data(i,Color(rng.randf(),rng.randf(),rng.randf(),0))
	splash_mm.custom_aabb = AABB(Vector3(-12,-2,-12),Vector3(24,4,24))
	splashes.multimesh = splash_mm
	var splash_material := ShaderMaterial.new()
	splash_material.shader = preload("res://shaders/rain_splash.gdshader")
	splash_material.set_shader_parameter("town_origin",ORIGIN)
	splashes.material_override = splash_material
	splashes.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(splashes)
	for radius in [16.0,32.0]:
		var curtain := MeshInstance3D.new()
		var tube := CylinderMesh.new()
		tube.top_radius = radius
		tube.bottom_radius = radius
		tube.height = 26.0
		tube.radial_segments = 32
		tube.rings = 1
		tube.cap_top = false
		tube.cap_bottom = false
		curtain.mesh = tube
		var sheet := ShaderMaterial.new()
		sheet.shader = preload("res://shaders/rain_curtain.gdshader")
		sheet.set_shader_parameter("strength",.2 if radius < 20 else .26)
		sheet.set_shader_parameter("columns",420.0 if radius < 20 else 760.0)
		curtain.material_override = sheet
		curtain.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		curtain.extra_cull_margin = 40.0
		add_child(curtain)
		curtains.append(curtain)

func area_of(world_position: Vector3) -> String:
	var p := world_position-ORIGIN
	if DINER.has_point(Vector2(p.x,p.z)): return "diner"
	if ALLEY.has_point(Vector2(p.x,p.z)): return "alley"
	return "street"

func _process(_delta: float) -> void:
	if not visible or not is_instance_valid(game.walker): return
	var p: Vector3 = game.walker.global_position-ORIGIN
	rain.position = Vector3(snappedf(p.x,2.0),p.y,snappedf(p.z,2.0))
	splashes.position = Vector3(snappedf(p.x,1.0),0,snappedf(p.z,1.0))
	var outside := area_of(game.walker.global_position) != "diner"
	rain.visible = outside
	splashes.visible = outside
	for curtain in curtains:
		curtain.position = Vector3(p.x,11.0,p.z)
		curtain.visible = outside
	var density: float = game.env.fog_density
	halo_material.set_shader_parameter("fog_density",density)

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
