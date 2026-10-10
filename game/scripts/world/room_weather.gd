class_name RoomWeather
extends Node

var elapsed := 0.0
var frozen := false
var materials: Array[ShaderMaterial] = []
var exterior_materials: Array[ShaderMaterial] = []
var rain_layers: Array[MultiMeshInstance3D] = []
var drops: Array[Dictionary] = []
const DROP_COUNTS := [100,120,140]
const VOLUMES := [Vector3(5.6,4.2,1.8),Vector3(11,6.4,4),Vector3(19,9,12)]

func _process(delta: float) -> void:
	if not frozen: set_time(elapsed+delta)

func set_time(value: float) -> void:
	elapsed = value
	for mat in materials: mat.set_shader_parameter("weather_time",elapsed)
	update_drops()

func outdoor_material(source: StandardMaterial3D, is_foliage: bool) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/outdoor_depth.gdshader")
	mat.set_shader_parameter("albedo_tex",source.albedo_texture)
	mat.set_shader_parameter("base_color",source.albedo_color)
	mat.set_shader_parameter("foliage",is_foliage)
	mat.set_shader_parameter("wet_ground",source.resource_name == "wetsoil")
	materials.append(mat)
	exterior_materials.append(mat)
	return mat

func sky_material() -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/overcast_sky.gdshader")
	materials.append(mat)
	return mat

func glass_material(source: StandardMaterial3D) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = load("res://shaders/window_water.gdshader")
	mat.set_shader_parameter("grime_tex",source.albedo_texture)
	mat.render_priority = 2
	materials.append(mat)
	return mat

func create_rain(parent: Node3D) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 140103
	for i in range(3):
		var layer := MultiMeshInstance3D.new()
		layer.name = "RainVolume_%s" % i
		var quad := QuadMesh.new()
		quad.size = Vector2.ONE
		var multimesh := MultiMesh.new()
		multimesh.transform_format = MultiMesh.TRANSFORM_3D
		multimesh.use_custom_data = true
		multimesh.mesh = quad
		multimesh.instance_count = DROP_COUNTS[i]
		multimesh.custom_aabb = AABB(-VOLUMES[i]*.5-Vector3.ONE*.4,VOLUMES[i]+Vector3.ONE*.8)
		layer.multimesh = multimesh
		layer.position = Vector3(-.8,[1.5,2.4,3.7][i],-[4.0,6.9,14.9][i])
		layer.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var mat := ShaderMaterial.new()
		mat.shader = load("res://shaders/rain_outside.gdshader")
		mat.set_shader_parameter("opacity",[.65,.50,.35][i])
		layer.material_override = mat
		parent.add_child(layer)
		rain_layers.append(layer)
		for j in range(DROP_COUNTS[i]):
			var width: float = rng.randf_range(.007,.017)*(1.0+float(i)*.32)
			var length: float = rng.randf_range(.09,.26)*(1.0+float(i)*.38)
			var lean: float = rng.randf_range(-.105,.025)
			var basis := Basis(Vector3.BACK,lean).scaled(Vector3(width,length,1))
			drops.append({"layer":i,"index":j,"seed":rng.randf_range(1,9000),"phase":rng.randf_range(0,VOLUMES[i].y),"speed":rng.randf_range(4.8,8.7),"wind":rng.randf_range(.06,.32),"basis":basis})
			multimesh.set_instance_custom_data(j,Color(rng.randf_range(.45,1.0),rng.randf_range(.65,1.0),0,1))
	update_drops()

func drop_hash(value: float) -> float:
	return fposmod(sin(value*12.9898)*43758.5453,1.0)

func drop_position(drop: Dictionary, time: float) -> Vector3:
	var volume: Vector3 = VOLUMES[drop.layer]
	var fall: float = drop.phase+time*drop.speed
	var cycle := floorf(fall/volume.y)
	var progress := fposmod(fall,volume.y)
	# Uniform coordinates; each drop respawns independently, no rows or cells.
	var x := (drop_hash(drop.seed+cycle*31.7)-.5)*volume.x
	x += drop.wind*(progress/drop.speed)+.025*sin(time*1.3+drop.seed)
	var z := (drop_hash(drop.seed+91.3+cycle*7.9)-.5)*volume.z
	return Vector3(x,volume.y*.5-progress,z)

func update_drops() -> void:
	for drop in drops:
		rain_layers[drop.layer].multimesh.set_instance_transform(drop.index,Transform3D(drop.basis,drop_position(drop,elapsed)))

func triangle_count() -> int:
	return drops.size()*2

func distribution_report() -> Dictionary:
	var layers: Array = []
	for i in range(3):
		var positions: Array = []
		var speeds: Array = []
		for drop in drops:
			if drop.layer != i:continue
			var p := drop_position(drop,2.0)+rain_layers[i].position
			positions.append([p.x,p.y,p.z]);speeds.append(drop.speed)
		layers.append({"count":DROP_COUNTS[i],"volume_m":[VOLUMES[i].x,VOLUMES[i].y,VOLUMES[i].z],"positions_at_2s":positions,"speeds_m_s":speeds})
	return {"method":"Independent continuous positions in 3 volumes; per-drop phase, speed, wind and respawn seed; no spatial lattice", "seed":140103,"drops":drops.size(),"triangles":triangle_count(),"layers":layers}

func set_wind(enabled: bool) -> void:
	for mat in exterior_materials: mat.set_shader_parameter("wind_amount",.04 if enabled else 0.0)
