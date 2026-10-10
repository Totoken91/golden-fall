extends RoomScene

# Independent visual review of the bedroom with its QA suite and films.
# Not part of the playable campaign (campaign.gd); kept as the regression harness.
var checks := 0
var failures: Array[String] = []
var movie_mode := false

func detect_qa_mode() -> bool:
	var args := OS.get_cmdline_user_args()
	movie_mode = "--assets-film" in args or "--room-film" in args or "--computer-film" in args or "--exterior-film" in args
	return movie_mode or "--room-capture" in args or "--room-check" in args

func wants_audio() -> bool: return not qa_mode or movie_mode
func prompt_captions() -> Dictionary:
	return {"pc":"use the computer", "desk":"look at the desk", "bed":"sit for a moment", "door":"look at the door"}

func _ready() -> void:
	# Review session: the bedroom on its own, no campaign save.
	super._ready()
	if not qa_mode: ui.toast("Bedroom · visual review")
	var args := OS.get_cmdline_user_args()
	if "--computer-film" in args: add_child(RoomComputerFilm.new(self))
	elif "--assets-film" in args: add_child(AssetContactFilm.new(self))
	elif "--exterior-film" in args: add_child(ExteriorFilm.new(self))
	elif movie_mode: add_child(RoomFilm.new(self))
	elif qa_mode: review_checks.call_deferred()

func _unhandled_input(event: InputEvent) -> void:
	super._unhandled_input(event)
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_ESCAPE:
		if is_modal: ui.close()
		else: show_menu()

func interact(id: String) -> void:
	match id:
		"pc": computer.enter()
		"desk":
			var col := ui.panel("The desk",Rect2(330,208,620,300))
			col.add_child(ui.paragraph("Schoolbooks, a cold mug and a cassette."))
			col.add_child(ui.button("Leave it",ui.close))
		"bed":
			var col := ui.panel("A quiet moment",Rect2(330,208,620,300))
			col.add_child(ui.paragraph("The rain covers the hum of the computer."))
			col.add_child(ui.button("Get up",ui.close))
		"door":
			var col := ui.panel("The door",Rect2(330,208,620,300))
			col.add_child(ui.paragraph("This review scene only covers the bedroom."))
			col.add_child(ui.button("Stay here",ui.close))

func show_menu() -> void:
	var col := ui.panel("Golden Fall · bedroom review",Rect2(330,142,620,440))
	col.add_child(ui.paragraph("WASD / ZQSD / arrows: walk
Mouse: look · E: interact · Esc: pause",ui.ink,19))
	col.add_child(ui.button("Resume",ui.close))
	col.add_child(ui.button("Rain sound: " + ("on" if sound_enabled else "off"),func(): toggle_sound(); show_menu()))
	col.add_child(ui.button("Quit",close_game))

func save_game(_notify := true) -> void: ui.toast("Review scene: nothing is saved.")

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures.append(message)
		push_error(message)

func capture(name: String) -> void:
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var dir := OS.get_environment("LHC_QA_DIR")
	DirAccess.make_dir_recursive_absolute(dir)
	var result := get_viewport().get_texture().get_image().save_png(dir.path_join(name+".png"))
	check(result == OK,"Capture " + name)
	if name == "01_porte" or name == "21_exterieur":
		var camera_info := {"camera_position":var_to_str(walker.camera.global_position),"camera_basis":var_to_str(walker.camera.global_basis),"vertical_fov":walker.camera.fov,"native_output":[1280,720],"world_pixels":[640,360],"pose_position_input":[-1.68,.03,2.30] if name == "01_porte" else [-.85,.03,-1.55],"pose_target_input":[-.05,.95,-1.45] if name == "01_porte" else [-.80,2.10,-8.0],"weather_time":weather.elapsed}
		var camera_file := FileAccess.open(dir.path_join("camera_comparaison.json" if name == "01_porte" else "camera_exterieur.json"),FileAccess.WRITE)
		camera_file.store_string(JSON.stringify(camera_info,"  "))
		camera_file.close()

func computer_checks() -> void:
	await computer.camera_tween.finished
	check(computer.active and not computer.transitioning,"Computer camera settles in front of the physical screen")
	check(walker.camera.global_position.is_equal_approx(Vector3(-.85,1.19,-1.40)),"Computer camera destination")
	check(is_equal_approx(walker.camera.fov,40.0),"Computer camera focus FOV")
	check(is_instance_valid(computer.screen_mesh),"Physical CRT screen mesh connected")
	check(computer.screen_material.get_shader_parameter("desktop_tex") == computer.display.get_texture(),"OS viewport is the screen material")
	check(ui.modal == null and not ui.root.visible,"No flat overlay replaces the physical screen")
	var frozen_body := walker.global_transform
	await pc_click(pc_target("Icon_browser"))
	check(computer.desktop.windows.has("browser"),"Mouse click on desktop icon opens browser")
	if computer.desktop.windows.has("browser"):
		await pc_click(computer.desktop.browser_input.get_global_rect().get_center())
		check(computer.display.gui_get_focus_owner() == computer.desktop.browser_input,"Physical cursor focuses the OS text field")
		for character in "diner":
			await pc_key(KEY_NONE,character.unicode_at(0))
		check(computer.desktop.browser_input.text == "diner","Keyboard types into physical OS search; got: "+computer.desktop.browser_input.text)
		await pc_key(KEY_ENTER)
		check(computer.desktop.browser_query == "diner","Enter submits OS search")
		var result: Button = computer.desktop.browser_body.get_node_or_null("Result_diner_review")
		check(is_instance_valid(result),"OS search exposes existing archive")
		if is_instance_valid(result):
			await pc_click(result.get_global_rect().get_center())
			check(computer.desktop.browser_page == "diner_review","Mouse opens an archive result")
			await pc_move(Vector2(400,300))
			for i in 6:
				for pressed in [true,false]:
					var wheel := InputEventMouseButton.new()
					wheel.set_meta("computer_qa",true)
					wheel.button_index = MOUSE_BUTTON_WHEEL_DOWN
					wheel.pressed = pressed
					Input.parse_input_event(wheel)
					await get_tree().process_frame
			var note: Button = computer.desktop.browser_body.get_node_or_null("NoteClue")
			check(is_instance_valid(note),"Archive has a physical OS note action")
			if is_instance_valid(note):
				await pc_click(note.get_global_rect().get_center())
				check(state.data.observations.any(func(o): return o.id == "web_diner_review"),"OS click adds the page to the journal")
		await pc_click(pc_target("StartButton"))
		check(computer.desktop.start_menu.visible,"Start menu responds to physical cursor")
		await pc_click(pc_target("Start_notes"))
		check(computer.desktop.windows.has("notes"),"Start menu launches notes")
		var browser: Panel = computer.desktop.windows["browser"]
		await pc_click(browser.get_node("Minimize").get_global_rect().get_center())
		check(not browser.visible,"Window minimize button responds")
		await pc_click(pc_target("Task_browser"))
		check(browser.visible,"Taskbar restores minimized window")
		var initial := browser.position
		await pc_move(initial+Vector2(110,15))
		var press := InputEventMouseButton.new()
		press.set_meta("computer_qa",true)
		press.button_index = MOUSE_BUTTON_LEFT
		press.pressed = true
		Input.parse_input_event(press)
		await get_tree().process_frame
		await pc_move(computer.cursor+Vector2(-12,8))
		press = InputEventMouseButton.new()
		press.set_meta("computer_qa",true)
		press.button_index = MOUSE_BUTTON_LEFT
		press.pressed = false
		Input.parse_input_event(press)
		await get_tree().process_frame
		check(not browser.position.is_equal_approx(initial),"Mouse drags a physical OS window")
	check(walker.global_transform.is_equal_approx(frozen_body),"Typing and mouse use do not move player body")
	var previous := computer.saved_camera
	await pc_key(KEY_ESCAPE)
	await computer.camera_tween.finished
	check(not computer.active and not is_modal and walker.enabled,"Escape restores exploration")
	check(walker.camera.global_transform.is_equal_approx(previous),"Computer exit restores exact previous camera")
	check(is_equal_approx(walker.camera.fov,62.0),"Computer exit restores normal FOV")
	for id in computer.desktop.windows.keys():computer.desktop.close_window(str(id))

func review_checks() -> void:
	for i in 15: await get_tree().physics_frame
	check(walker.is_on_floor(),"Player stands on the floor")
	check(view.size == Vector2i(640,360),"World resolution")
	check(floor_material_surfaces > 0,"Cached low-resolution parquet is bound to the real floor")
	var floor_config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/room_materials.json"))
	var floor_library = load("res://scripts/world/texture_library.gd").new()
	var floor_material = floor_library.material_for_uv(str(floor_config.floor.key),Vector2(1.8,1.8))
	check(floor_material != null and floor_material.albedo_texture.get_width() == 128 and floor_material.texture_filter == BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS,"PSX parquet: 128px nearest with mipmaps")
	check(floor_material != null and floor_material.albedo_texture.get_image().has_mipmaps(),"Parquet mipmap levels are actually imported")
	check(material_pass.applied.size()==floor_config.surfaces.size(),"All targeted room material surfaces are applied")
	var room_maps_valid := true
	for binding in material_pass.applied:room_maps_valid = room_maps_valid and binding.size==[128,128] and binding.mipmaps
	check(room_maps_valid,"Room materials use real imported 128px maps with mipmaps")
	var density_valid := true
	for binding in material_pass.applied:
		if not binding.texels_per_m.is_empty():density_valid = density_valid and is_equal_approx(binding.texels_per_m[0],float(floor_config.cohesion.wood_target_texels_per_m)) and is_equal_approx(binding.texels_per_m[1],float(floor_config.cohesion.wood_target_texels_per_m))
	check(density_valid,"Furniture wood has consistent texel density on both UV axes")
	var actual_model: Node3D
	for item in material_pass.baseline:
		actual_model=item.node.get_parent()
		break
	check(actual_model != null and count_mesh_triangles(actual_model)==room_triangle_count,"Runtime material pass preserves model triangle count")
	check(room_triangle_count+weather.triangle_count() <= 8000,"Room plus rain stays within 8000 triangle budget")
	var rain_audio: AudioStreamWAV = load("res://assets/audio/rain.wav")
	check(absf(rain_audio.get_length()-35.656)<.01,"User rain recording is included in packaged runtime")
	var old_yaw := walker.rotation.y
	var old_pitch := walker.pitch
	walker.look(Vector2(80,-25))
	check(not is_equal_approx(walker.rotation.y,old_yaw) and walker.pitch > old_pitch,"Mouse changes yaw and pitch")
	walker.look(Vector2(0,-100000))
	check(walker.pitch <= 1.30,"Pitch clamp")
	# Head-on wall, then bed: exercise the actual CharacterBody collision solver.
	await pose(Vector3(2.48,.03,1.7),Vector3(2.75,1.62,1.7))
	for i in 36:
		walker.velocity = Vector3(3,0,0)
		walker.move_and_slide()
		await get_tree().physics_frame
	check(walker.position.x < 2.55,"Wall blocks the capsule")
	await pose(Vector3(1.8,.03,.95),Vector3(1.8,1.30,-.5))
	for i in 36:
		walker.velocity = Vector3(0,0,-3)
		walker.move_and_slide()
		await get_tree().physics_frame
	check(walker.position.z > -.15,"Repositioned bed blocks walking")
	for sample in [
		["pc",Vector3(-.85,.03,-.90),Vector3(-.85,1.17,-1.94)],
		["desk",Vector3(-1.52,.03,-1.13),Vector3(-1.55,.78,-1.86)],
		["bed",Vector3(.65,.03,-.40),Vector3(1.65,.55,-1.20)],
		["door",Vector3(-1.75,.03,1.80),Vector3(-1.75,1.2,2.70)]
	]:
		await pose(sample[1],sample[2])
		check(walker.target() == sample[0],"Ray interaction: " + sample[0] + " got " + walker.target())
		interact(sample[0])
		check(is_modal and not walker.enabled,"Interaction opens native UI: " + sample[0])
		if sample[0] == "pc":await computer_checks()
		else:ui.close()
		check(not is_modal and walker.enabled,"Closing UI restores movement")
	check(not web.search("diner").is_empty(),"Existing archive search")
	# Actual WASD input, not a substitute translation.
	await pose(Vector3(-.1,.03,1.65),Vector3(-.1,1.62,-1.0))
	var start_z := walker.position.z
	var key := InputEventKey.new()
	key.physical_keycode = KEY_W
	key.pressed = true
	Input.parse_input_event(key)
	for i in 16: await get_tree().physics_frame
	key = InputEventKey.new()
	key.physical_keycode = KEY_W
	key.pressed = false
	Input.parse_input_event(key)
	check(walker.position.z < start_z-.15,"W key moves player")
	set_modal(true)
	walker.enabled = false
	ui.root.hide()
	await pose(Vector3(-1.68,.03,2.30),Vector3(-.05,.95,-1.45))
	weather.frozen = true
	weather.set_wind(false)
	weather.set_time(2.0)
	await RenderingServer.frame_post_draw
	var rain_before := view.get_texture().get_image()
	weather.set_time(2.23)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var rain_after := view.get_texture().get_image()
	check(rain_before.get_region(Rect2i(170,65,140,105)).get_data() != rain_after.get_region(Rect2i(170,65,140,105)).get_data(),"Falling rain changes pixels through the window")
	check(rain_before.get_region(Rect2i(490,90,90,70)).get_data() == rain_after.get_region(Rect2i(490,90,90,70)).get_data(),"Rain does not overlay the interior")
	check(weather.rain_layers.size() == 3 and weather.rain_layers[0].position.z < -2.9,"Rain layers are outside the room")
	var report := weather.distribution_report()
	var rain_valid := true
	for layer in report.layers:
		var speeds: Array = layer.speeds_m_s
		speeds.sort()
		rain_valid = rain_valid and speeds[-1]-speeds[0]>3.0
		for p in layer.positions_at_2s:rain_valid = rain_valid and p[2]<-2.9
	check(rain_valid,"Independent rain speeds and all drops outside the room")
	check(weather.drops.size()==360 and weather.triangle_count()==720,"Rain geometry counted in total budget")
	var sample: Dictionary = weather.drops[0]
	check(weather.drop_position(sample,2.0).is_equal_approx(weather.drop_position(sample,2.0)),"Frozen weather gives reproducible positions")
	check(not weather.drop_position(sample,2.0).is_equal_approx(weather.drop_position(sample,2.23)),"Independent world-space drops move over time")
	var rain_file := FileAccess.open(OS.get_environment("LHC_QA_DIR").path_join("rain_distribution.json"),FileAccess.WRITE)
	if rain_file:rain_file.store_string(JSON.stringify(report,"  "));rain_file.close()
	check(reticle.text=="·" and "Esc" in help.text,"HUD strings and reticle are intact")
	weather.set_wind(true)
	weather.set_time(2.0)
	var timings: Array[float] = []
	var before := Time.get_ticks_usec()
	for i in 150:
		await get_tree().process_frame
		var now := Time.get_ticks_usec()
		if i >= 30: timings.append((now-before)/1000.0)
		before = now
	timings.sort()
	var total := 0.0
	for timing in timings: total += timing
	var performance := {"samples":timings.size(),"average_frame_ms":total/timings.size(),"p95_frame_ms":timings[int(timings.size()*.95)],"godot_static_mib":Performance.get_monitor(Performance.MEMORY_STATIC)/1048576.0,"gpu":RenderingServer.get_video_adapter_name(),"world_pixels":[640,360],"note":"Single stationary doorway view, after 30 warmup frames; not a hardware target benchmark."}
	performance["room_triangles"] = room_triangle_count
	performance["total_with_rain_triangles"] = room_triangle_count+weather.triangle_count()
	performance["viewport_primitives"] = view.get_render_info(Viewport.RENDER_INFO_TYPE_VISIBLE,Viewport.RENDER_INFO_PRIMITIVES_IN_FRAME)
	performance["viewport_draw_calls"] = view.get_render_info(Viewport.RENDER_INFO_TYPE_VISIBLE,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME)
	DirAccess.make_dir_recursive_absolute(OS.get_environment("LHC_QA_DIR"))
	var perf_file := FileAccess.open(OS.get_environment("LHC_QA_DIR").path_join("performance.json"),FileAccess.WRITE)
	if perf_file: perf_file.store_string(JSON.stringify(performance,"  ")); perf_file.close()
	await capture("01_porte")
	await pose(Vector3(-.49,.03,-.40),Vector3(-.82,1.13,-2.2))
	await capture("02_bureau")
	await pose(Vector3(-1.75,.03,-1.77),Vector3(.98,1.12,.25))
	await capture("03_fenetre")
	walker.set_physics_process(false)
	await pose(Vector3(-.85,.03,-1.55),Vector3(-.80,2.10,-8.0))
	await capture("21_exterieur")
	walker.set_physics_process(true)
	await pose(Vector3(-.10,.03,.10),Vector3(-.87,.93,-1.03))
	await capture("05_chaise")
	await pose(Vector3(.42,.03,-.15),Vector3(1.92,.61,-1.42))
	await capture("06_literie")
	await pose(Vector3(-.90,.03,1.45),Vector3(-1.85,.28,1.03))
	await capture("08_sac")
	await pose(Vector3(-.65,.03,-1.15),Vector3(-.79,.85,-1.83))
	await capture("09_clavier")
	# Texture inspection views; same artwork placements and normal player eye height.
	walker.set_physics_process(false)
	await pose(Vector3(1.79,.03,-1.60),Vector3(1.79,1.96,-2.807))
	await capture("14_posters_fenetre")
	await pose(Vector3(1.58,.03,1.08),Vector3(2.718,1.66,1.08))
	await capture("15_posters_commode")
	walker.set_physics_process(true)
	# Dedicated contact inspections, physics suspended only for camera access.
	walker.set_physics_process(false)
	for shot in [
		["25_casque",Vector3(-1.50,1.30,-1.76),Vector3(-1.6,.95,-2.22),48.0],
		["26_crt_ventilation",Vector3(-.07,1.40,-1.90),Vector3(-.65,1.16,-2.20),46.0],
		["27_chevet",Vector3(.18,1.35,-1.75),Vector3(.78,.84,-2.43),54.0],
		["28_rideau",Vector3(.02,1.60,-1.70),Vector3(.46,1.14,-2.45),55.0],
		["29_amenagement",Vector3(.60,2.38,-.75),Vector3(1.65,.63,-2.40),62.0],
		["30_contacts_sol",Vector3(-.70,.35,-.10),Vector3(-1.58,.22,-1.70),62.0]
	]:
		walker.camera.position = Vector3(0,1.62,0)
		walker.camera.fov = shot[3]
		await pose(shot[1]-Vector3(0,1.62,0),shot[2])
		await capture(shot[0])
	walker.camera.fov = 62
	walker.camera.position = Vector3(0,1.62,0)
	await pose(Vector3(-.49,.03,-.40),Vector3(-.82,1.13,-2.2))
	ui.root.show();set_modal(false)
	await capture("31_interface_corrigee")
	set_modal(true);ui.root.hide()
	walker.set_physics_process(true)
	# Inspection camera only; the player's normal eye height and controls stay intact.
	walker.camera.position.y = .60
	await pose(Vector3(-1.85,.03,2.0),Vector3(-1.85,.24,1.03))
	await capture("12_sac_face")
	await pose(Vector3(-.90,.03,1.03),Vector3(-1.85,.24,1.03))
	await capture("13_sac_profil")
	walker.camera.position.y = 1.62
	await pose(Vector3(-.49,.03,-.40),Vector3(-.82,1.13,-2.2))
	ui.root.show()
	interact("pc")
	await computer.camera_tween.finished
	await capture("04_ordinateur")
	await pc_click(pc_target("Icon_browser"))
	await capture("18_os_navigateur")
	await pc_click(pc_target("Icon_notes"))
	await capture("19_os_carnet")
	computer.leave()
	await computer.camera_tween.finished
	print("ROOM CHECKS: %s checks, %s failures" % [checks,failures.size()])
	get_tree().quit(0 if failures.is_empty() else 1)
