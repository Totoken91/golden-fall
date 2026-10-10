class_name RoomComputer
extends Node

var game: Node
var display: SubViewport
var desktop: CedarDesktop
var screen_mesh: MeshInstance3D
var screen_material: ShaderMaterial
var active := false
var transitioning := false
var cursor := Vector2(320,240)
var saved_camera := Transform3D.IDENTITY
var saved_fov := 62.0
var camera_tween: Tween
# V0.20: once zoomed in, the desktop is shown at native resolution over the physical
# screen (outside the 640x360 dithered world) so text stays readable.
var overlay_layer: CanvasLayer
var overlay: TextureRect
var overlay_tween: Tween
var screen_corners: Array[Vector3] = []
var audio: PcAudio

func _init(controller: Node) -> void:
	game = controller

func _ready() -> void:
	display = SubViewport.new()
	display.name = "PhysicalComputerDisplay"
	display.size = Vector2i(640,480)
	display.disable_3d = true
	display.handle_input_locally = true
	display.render_target_update_mode = SubViewport.UPDATE_ONCE
	add_child(display)
	desktop = CedarDesktop.new(game)
	display.add_child(desktop)
	desktop.leave_requested.connect(request_leave)
	screen_material = ShaderMaterial.new()
	screen_material.shader = load("res://shaders/physical_crt.gdshader")
	screen_material.set_shader_parameter("desktop_tex",display.get_texture())
	overlay_layer = CanvasLayer.new()
	overlay_layer.name = "CrtOverlay"
	overlay_layer.layer = 3
	add_child(overlay_layer)
	overlay = TextureRect.new()
	overlay.name = "NativeScreen"
	overlay.texture = display.get_texture()
	overlay.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	overlay.stretch_mode = TextureRect.STRETCH_SCALE
	overlay.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var crt := ShaderMaterial.new()
	crt.shader = load("res://shaders/crt_overlay.gdshader")
	overlay.material = crt
	overlay.modulate.a = 0.0
	overlay.hide()
	overlay_layer.add_child(overlay)
	audio = PcAudio.new()
	add_child(audio)
	desktop.chime.connect(audio.play_chime)

func attach_screen(mesh: MeshInstance3D, surface: int) -> void:
	screen_mesh = mesh
	mesh.set_surface_override_material(surface,screen_material)
	mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	screen_corners.clear()
	var arrays := mesh.mesh.surface_get_arrays(surface)
	var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	# Bounding box of the whole tube surface, so the native view fully covers the in-world one.
	var bounds := AABB(vertices[0],Vector3.ZERO)
	for vertex in vertices: bounds = bounds.expand(vertex)
	for i in 8: screen_corners.append(bounds.get_endpoint(i))

func screen_rect() -> Rect2:
	var camera: Camera3D = game.walker.camera
	var scale := get_viewport().get_visible_rect().size/Vector2(game.view.size)
	var rect := Rect2()
	for i in screen_corners.size():
		var point := camera.unproject_position(screen_mesh.global_transform*screen_corners[i])*scale
		if i == 0: rect = Rect2(point,Vector2.ZERO)
		else: rect = rect.expand(point)
	return rect

func fade_overlay(target: float, delay: float, duration: float) -> void:
	if is_instance_valid(overlay_tween): overlay_tween.kill()
	overlay.show()
	overlay_tween = create_tween()
	overlay_tween.tween_interval(delay)
	if target <= 0.0: screen_material.set_shader_parameter("covered",0.0)
	overlay_tween.tween_property(overlay,"modulate:a",target,duration)
	if target <= 0.0: overlay_tween.tween_callback(overlay.hide)
	else: overlay_tween.tween_callback(func(): screen_material.set_shader_parameter("covered",1.0))

func _process(_delta: float) -> void:
	if overlay.visible and not screen_corners.is_empty():
		var rect := screen_rect()
		# A few pixels of margin: the world is upscaled from 640x360 with nearest filtering.
		overlay.position = rect.position-Vector2(4,4)
		overlay.size = rect.size+Vector2(8,8)

func enter() -> void:
	if active:return
	desktop.refresh_metadata()
	game.ui.close()
	game.set_modal(true)
	game.ui.root.hide()
	game.walker.set_physics_process(false)
	active = true
	transitioning = true
	saved_camera = game.walker.camera.global_transform
	saved_fov = game.walker.camera.fov
	display.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	display.notify_mouse_entered()
	desktop.set_pointer(cursor,true)
	if not game.qa_mode:Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	var destination := Transform3D(Basis.IDENTITY,Vector3(-.85,1.19,-1.40))
	camera_tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	camera_tween.tween_property(game.walker.camera,"global_transform",destination,.7)
	camera_tween.tween_property(game.walker.camera,"fov",40.0,.7)
	camera_tween.finished.connect(func(): transitioning = false)
	fade_overlay(1.0,.42,.28)
	audio.power(true)

# V0.20: leaving ends a paid research evening, so the campaign asks first; a misclick or a
# stutter must not silently spend the evening. Review mode and scripted exits stay direct.
func request_leave() -> void:
	if not active or transitioning: return
	leave()

func leave() -> void:
	if not active:return
	if is_instance_valid(camera_tween):camera_tween.kill()
	transitioning = true
	desktop.set_pointer(cursor,false)
	desktop.start_menu.hide()
	display.gui_release_focus()
	display.notify_mouse_exited()
	fade_overlay(0.0,0.0,.18)
	audio.power(false)
	camera_tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	camera_tween.tween_property(game.walker.camera,"global_transform",saved_camera,.7)
	camera_tween.tween_property(game.walker.camera,"fov",saved_fov,.7)
	camera_tween.finished.connect(func():
		active = false
		transitioning = false
		display.render_target_update_mode = SubViewport.UPDATE_ONCE
		game.walker.set_physics_process(true)
		game.ui.root.show()
		game.set_modal(false)
		game.computer_closed())

func _input(event: InputEvent) -> void:
	if not active:return
	get_viewport().set_input_as_handled()
	# Only scripted input drives hidden QA captures; normal play accepts all input.
	if game.qa_mode and not event.has_meta("computer_qa"):return
	if event is InputEventKey and event.pressed and not event.echo: audio.play_key()
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_F5:
		desktop.manual_save()
		return
	if event is InputEventKey and event.pressed and event.physical_keycode == KEY_ESCAPE:
		if transitioning: return
		request_leave()
		return
	if transitioning:return
	forward_event(event)

func forward_event(event: InputEvent) -> void:
	var local := event.duplicate() as InputEvent
	if local is InputEventMouseMotion:
		cursor = (cursor+local.relative).clamp(Vector2(0,0),Vector2(639,479))
		local.position = cursor
		local.global_position = cursor
	elif local is InputEventMouseButton:
		if local.button_index == MOUSE_BUTTON_LEFT or local.button_index == MOUSE_BUTTON_RIGHT: audio.play_click()
		local.position = cursor
		local.global_position = cursor
	display.push_input(local,true)
	if local is InputEventMouseMotion: desktop.set_pointer(cursor,true)
