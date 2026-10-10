class_name RoomScene
extends Node

# The bedroom shared by the playable campaign (campaign.gd) and the independent
# visual review/QA scene (room_review.gd): 640x360 dithered world, lights, materials,
# rain, first-person body, physical PC, native overlay and audio. No game rules here.
var db := ContentDB.new()
var state := GoldenState.new(db)
var web := WebArchive.new(state)
var ui: AutumnUI
var walker: RoomWalker
var view: SubViewport
var scene: Node3D
var is_modal := false
var sound_enabled := false
var qa_mode := false
var reticle: Label
var help: Label
var ambience: AudioStreamPlayer
# Outdoor rain (procedural loop) on its own bus with a low-pass: clear on the street, muffled in the
# diner. The user's indoor recording (ambience) only plays in the bedroom.
var outdoor: AudioStreamPlayer
var outdoor_filter: AudioEffectLowPassFilter
const AUDIO_AREAS := {"bedroom":[-2.0,-80.0,9000.0],"street":[-80.0,-5.0,9000.0],"alley":[-80.0,-7.0,6500.0],"diner":[-80.0,-13.0,650.0]}
var closing := false
var weather: RoomWeather
var room_triangle_count := 0
var floor_material_surfaces := 0
var material_pass = preload("res://scripts/world/room_material_pass.gd").new()
var computer: RoomComputer
var env: Environment
var daylight: DirectionalLight3D
var town: TownZone
var zone := "bedroom"
var fade: ColorRect
# Atmosphere per zone: bedroom keeps the validated V0.17 values; town is amber overcast dusk.
const ATMOSPHERE := {
	"bedroom": {"bg":"5e6969","ambient":"b2aaa0","ambient_energy":.18,"fog":"626b6b","fog_density":.004,"sun":"a6bac1","sun_energy":.24,"sun_rot":Vector3(-40,-25,0)},
	"town": {"bg":"6f6658","ambient":"b39f86","ambient_energy":.42,"fog":"7a6e5e","fog_density":.028,"sun":"e7b57a","sun_energy":.55,"sun_rot":Vector3(-18,-118,0)},
}

func _ready() -> void:
	qa_mode = detect_qa_mode()
	if qa_mode: Input.use_accumulated_input = false
	get_tree().auto_accept_quit = false
	build_view()
	if not qa_mode: add_child(FrameWatch.new(self))
	ui = AutumnUI.new(self)
	add_child(ui)
	reticle = ui.label("·",21,Color("d5c9ae"))
	reticle.position = Vector2(631,345)
	reticle.size = Vector2(18,30)
	reticle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	reticle.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.root.add_child(reticle)
	help = ui.label(help_text(),15,Color("c0b29a"))
	help.position = Vector2(32,690)
	help.mouse_filter = Control.MOUSE_FILTER_IGNORE
	help.add_theme_color_override("font_shadow_color",Color(0,0,0,.85))
	help.add_theme_constant_override("shadow_offset_x",1)
	help.add_theme_constant_override("shadow_offset_y",1)
	ui.root.add_child(help)
	fade = ColorRect.new()
	fade.color = Color(0,0,0,0)
	fade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.root.add_child(fade)
	set_modal(false)
	if wants_audio(): start_audio()

# Overridden by each scene.
func detect_qa_mode() -> bool: return false
func wants_audio() -> bool: return not qa_mode
func help_text() -> String: return "WASD / ZQSD · mouse · E interact · Esc pause"
func prompt_captions() -> Dictionary: return {}
func interact(_id: String) -> void: pass
func show_menu() -> void: pass
func build_town() -> void:
	town = TownZone.new(self)
	scene.add_child(town)
	town.build()

func apply_atmosphere(name: String) -> void:
	var a: Dictionary = ATMOSPHERE[name]
	env.background_color = Color(a.bg)
	env.ambient_light_color = Color(a.ambient)
	env.ambient_light_energy = a.ambient_energy
	env.fog_light_color = Color(a.fog)
	env.fog_density = a.fog_density
	daylight.light_color = Color(a.sun)
	daylight.light_energy = a.sun_energy
	daylight.rotation_degrees = a.sun_rot
	daylight.directional_shadow_max_distance = 70 if name == "bedroom" else 35

# Places the player in a zone at a position, looking at a target. Instant (used by loading too).
func place(zone_name: String, at: Vector3, look: Vector3) -> void:
	zone = zone_name
	walker.steps_enabled = zone_name != "bedroom"
	apply_atmosphere("bedroom" if zone_name == "bedroom" else "town")
	walker.position = at
	walker.velocity = Vector3.ZERO
	walker.aim(look)

# Door transition with a short fade; the walk itself is never interrupted elsewhere.
func travel(zone_name: String, at: Vector3, look: Vector3) -> void:
	set_modal(true)
	var tween := create_tween()
	tween.tween_property(fade,"color:a",1.0,.35)
	tween.tween_callback(place.bind(zone_name,at,look))
	tween.tween_interval(.15)
	tween.tween_property(fade,"color:a",0.0,.45)
	tween.tween_callback(func(): set_modal(false))

# Called by RoomComputer once the camera is back from the screen.
func computer_closed() -> void: pass


func build_view() -> void:
	view = SubViewport.new()
	view.size = Vector2i(640,360)
	view.own_world_3d = true
	view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	view.msaa_3d = Viewport.MSAA_DISABLED
	view.screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
	add_child(view)
	var image := TextureRect.new()
	image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	image.texture = view.get_texture()
	image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	image.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shader := ShaderMaterial.new()
	shader.shader = load("res://shaders/room_pixels.gdshader")
	image.material = shader
	add_child(image)
	scene = Node3D.new()
	view.add_child(scene)
	weather = RoomWeather.new()
	scene.add_child(weather)
	computer = RoomComputer.new(self)
	add_child(computer)
	var model: Node3D = load("res://assets/room/bedroom.glb").instantiate()
	scene.add_child(model)
	room_triangle_count = count_mesh_triangles(model)
	prepare_meshes(model)
	floor_material_surfaces = apply_room_materials(model)
	var room_bindings: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/room_materials.json"))
	material_pass.apply(model,room_bindings.get("surfaces",[]))
	weather.create_rain(scene)
	var environment := WorldEnvironment.new()
	env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("5e6969")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("b2aaa0")
	env.ambient_light_energy = 0.18
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.fog_enabled = true
	env.fog_light_color = Color("626b6b")
	env.fog_light_energy = 0.65
	env.fog_density = 0.004
	env.fog_sky_affect = 0
	environment.environment = env
	scene.add_child(environment)
	daylight = DirectionalLight3D.new()
	daylight.light_color = Color("a6bac1")
	daylight.light_energy = .24
	daylight.rotation_degrees = Vector3(-40,-25,0)
	daylight.shadow_enabled = true
	daylight.directional_shadow_max_distance = 70
	scene.add_child(daylight)
	var lamp := OmniLight3D.new()
	lamp.position = Vector3(.84,.992,-2.505)
	lamp.light_color = Color("ffca80")
	lamp.light_energy = .76
	lamp.omni_range = 3.2
	lamp.omni_attenuation = 1.65
	lamp.shadow_enabled = true
	lamp.shadow_bias = .03
	scene.add_child(lamp)
	# Broad cool window spill and a low reflected pool keep the far corners readable.
	var window := SpotLight3D.new()
	window.position = Vector3(-.8,2.35,-3.25)
	window.light_color = Color("b4c6c5")
	window.light_energy = 1.0
	window.spot_range = 7.0
	window.spot_angle = 43
	window.spot_attenuation = 1.1
	window.shadow_enabled = true
	scene.add_child(window)
	window.look_at(Vector3(-.15,.35,.9))
	var spill := OmniLight3D.new()
	spill.position = Vector3(-.8,1.9,-2.2)
	spill.light_color = Color("abbab7")
	spill.light_energy = .2
	spill.omni_range = 3.4
	spill.omni_attenuation = 1.5
	scene.add_child(spill)
	var bounce := OmniLight3D.new()
	bounce.position = Vector3(.35,1.65,-.55)
	bounce.light_color = Color("c4aa80")
	bounce.light_energy = .065
	bounce.omni_range = 3.2
	bounce.omni_attenuation = 1.0
	scene.add_child(bounce)
	var crt := OmniLight3D.new()
	crt.position = Vector3(-.85,1.19,-1.85)
	crt.light_color = Color("82998c")
	crt.light_energy = .20
	crt.omni_range = 1.1
	scene.add_child(crt)
	walker = RoomWalker.new()
	scene.add_child(walker)
	walker.position = Vector3(-1.68,.025,2.30)
	walker.aim(Vector3(-.05,.95,-1.45))

func count_mesh_triangles(node: Node) -> int:
	var total := 0
	if node is MeshInstance3D:
		total += int(node.mesh.get_faces().size()/3.0)
	for child in node.get_children(): total += count_mesh_triangles(child)
	return total

func prepare_meshes(node: Node) -> void:
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		for i in mi.mesh.get_surface_count():
			var mat := mi.get_active_material(i) as StandardMaterial3D
			if mat:
				mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
				var material_name := str(mat.resource_name)
				if material_name == "screen": computer.attach_screen(mi,i)
				mat.roughness = .96
				mat.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
				if material_name in ["brass","metal"]:
					mat.roughness = .55 if material_name == "brass" else .72
					mat.metallic = .55 if material_name == "brass" else .35
					mat.specular_mode = BaseMaterial3D.SPECULAR_SCHLICK_GGX
				elif material_name in ["ivory","crt_side","paint","keycaps","ceramic"]:
					mat.roughness = .73
					mat.metallic = 0
					mat.specular_mode = BaseMaterial3D.SPECULAR_SCHLICK_GGX
				if str(mi.name).begins_with("Sky_"):
					mi.set_surface_override_material(i,weather.sky_material())
				if "Glass_" in mi.name:
					mi.set_surface_override_material(i,weather.glass_material(mat))
				if "curtain" in mi.name or "Shade_" in mi.name or "Cloth_" in mi.name: mat.cull_mode = BaseMaterial3D.CULL_DISABLED
				if str(mi.name).begins_with("Foliage_") or str(mi.name).begins_with("Outside_"):
					mi.set_surface_override_material(i,weather.outdoor_material(mat,str(mi.name).begins_with("Foliage_")))
		if str(mi.name).begins_with("Shade_"): mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		if str(mi.name).begins_with("Sky_"): mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		if str(mi.name).begins_with("Glass_"): mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		if str(mi.name).begins_with("C_") or str(mi.name).begins_with("I_"):
			mi.create_trimesh_collision()
			if str(mi.name).begins_with("I_"):
				mi.set_meta("interaction",str(mi.name).split("_")[1])
	for child in node.get_children(): prepare_meshes(child)

func apply_room_materials(model: Node3D) -> int:
	# Material-only override: preserve model UVs, geometry and room placement.
	var config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/room_materials.json"))
	var binding: Dictionary = config.floor
	var library = load("res://scripts/world/texture_library.gd").new()
	var count := 0
	for node in model.find_children("*", "MeshInstance3D", true, false):
		for surface in node.mesh.get_surface_count():
			var original = node.get_active_material(surface)
			if original is StandardMaterial3D and original.resource_name == "floor":
				if library.apply_surface(node,surface,str(binding.key),Vector2(float(binding.uv_period_m[0]),float(binding.uv_period_m[1]))) == OK:
					# Keep the semantic material label for QA and future targeted passes.
					node.get_active_material(surface).resource_name = "floor"
					count += 1
	return count

func set_modal(value: bool) -> void:
	is_modal = value
	if is_instance_valid(walker): walker.enabled = not value
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE if value or qa_mode else Input.MOUSE_MODE_CAPTURED
	if is_instance_valid(reticle): reticle.visible = not value
	if is_instance_valid(help): help.visible = not value
	if is_instance_valid(ui): ui.prompt.visible = not value

# Browsers only grant pointer lock inside a real click, so a capture requested after a menu
# button is refused; on the web every click retries it while the mouse should be captured.
static func recapture_on_click(event: InputEvent) -> void:
	if OS.has_feature("web") and event is InputEventMouseButton and event.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

# Chrome's pointer lock on Windows occasionally reports a single huge movement (hundreds of
# pixels) that makes the camera jump. Real flicks stay well below this per event.
const WEB_MOUSE_SPIKE := 300.0

static func mouse_delta(event: InputEventMouseMotion) -> Vector2:
	if OS.has_feature("web") and event.relative.length() > WEB_MOUSE_SPIKE: return Vector2.ZERO
	return event.relative

func _input(event: InputEvent) -> void:
	if not is_modal and not qa_mode: recapture_on_click(event)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and not is_modal and (qa_mode or Input.mouse_mode == Input.MOUSE_MODE_CAPTURED): walker.look(mouse_delta(event))
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_E:
		if not is_modal: interact(walker.target())

func _process(delta: float) -> void:
	update_audio(delta)
	if not is_instance_valid(ui) or is_modal: return
	if OS.has_feature("web") and not qa_mode and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		ui.prompt.text = "Click to look around"
		return
	var captions := prompt_captions()
	var id := walker.target()
	ui.prompt.text = "E · " + captions[id] if captions.has(id) else ""

# Eases the two rain layers toward the player's current area (bedroom / street / alley / diner).
func update_audio(delta: float) -> void:
	if not is_instance_valid(outdoor) or not is_instance_valid(walker): return
	var area := "bedroom" if zone == "bedroom" or not is_instance_valid(town) else town.area_of(walker.global_position)
	var target: Array = AUDIO_AREAS[area]
	var k := clampf(delta*3.0,0.0,1.0)
	ambience.volume_db = lerpf(ambience.volume_db,target[0],k)
	outdoor.volume_db = lerpf(outdoor.volume_db,target[1],k)
	outdoor_filter.cutoff_hz = lerpf(outdoor_filter.cutoff_hz,target[2],k)

func start_audio() -> void:
	var bus := AudioServer.bus_count
	AudioServer.add_bus(bus)
	AudioServer.set_bus_name(bus,"Outdoor")
	outdoor_filter = AudioEffectLowPassFilter.new()
	outdoor_filter.cutoff_hz = 9000.0
	AudioServer.add_bus_effect(bus,outdoor_filter)
	outdoor = AudioStreamPlayer.new()
	var rain: AudioStreamWAV = load("res://assets/audio/rain_outdoor.wav")
	rain.loop_mode = AudioStreamWAV.LOOP_FORWARD
	rain.loop_end = int(rain.get_length()*rain.mix_rate)
	outdoor.stream = rain
	outdoor.bus = "Outdoor"
	outdoor.volume_db = -80.0
	add_child(outdoor)
	outdoor.play()
	ambience = AudioStreamPlayer.new()
	var stream: AudioStreamWAV = load("res://assets/audio/rain.wav")
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	stream.loop_end = int(stream.get_length()*stream.mix_rate)
	ambience.stream = stream
	ambience.volume_db = -2
	add_child(ambience)
	sound_enabled = true
	ambience.play()

func toggle_sound() -> void:
	sound_enabled = not sound_enabled
	if is_instance_valid(ambience):
		if sound_enabled: ambience.play()
		else: ambience.stop()
	if is_instance_valid(outdoor):
		if sound_enabled: outdoor.play()
		else: outdoor.stop()

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST: close_game.call_deferred()

func close_game() -> void:
	if closing: return
	closing = true
	if is_instance_valid(ambience):
		ambience.stop()
		ambience.stream = null
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	await get_tree().process_frame
	await get_tree().process_frame
	get_tree().quit()

# Camera placement and scripted PC input, shared by QA checks, captures and films.
func pose(pos: Vector3, look_at: Vector3) -> void:
	walker.position = pos
	walker.velocity = Vector3.ZERO
	walker.aim(look_at)
	await get_tree().physics_frame
	await get_tree().physics_frame

func pc_move(point: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.set_meta("computer_qa",true)
	event.relative = point-computer.cursor
	Input.parse_input_event(event)
	await get_tree().process_frame
	await get_tree().process_frame

func pc_click(point: Vector2) -> void:
	await pc_move(point)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.set_meta("computer_qa",true)
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		Input.parse_input_event(event)
		await get_tree().process_frame
		await get_tree().process_frame

func pc_key(code: Key, unicode := 0) -> void:
	for pressed in [true,false]:
		var event := InputEventKey.new()
		event.set_meta("computer_qa",true)
		var resolved: Key = code if code != KEY_NONE else String.chr(unicode).to_upper().unicode_at(0) as Key
		event.physical_keycode = resolved
		event.keycode = resolved
		event.unicode = unicode
		event.pressed = pressed
		Input.parse_input_event(event)
		await get_tree().process_frame

# Center of a named control on the PC desktop, in desktop pixels (for scripted clicks).
func pc_target(node_name: String) -> Vector2:
	var node := computer.desktop.find_child(node_name,true,false) as Control
	return node.get_global_rect().get_center() if node else Vector2(-1,-1)
