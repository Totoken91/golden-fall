extends SceneTree
# Stage 1 traversal QA (P02): walk room -> porch -> street -> diner -> alley -> home with the real
# W key and the real collision solver, then capture the review views. Isolated save.
# LHC_QA_DIR, LHC_CAMPAIGN_SAVE ; run with -- --campaign-check
var checks := 0
var failures: Array[String] = []
var game: Node
var dest: String
var walked := 0.0
var walk_time := 0.0

func _initialize() -> void: run.call_deferred()

func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures.append(message)
		push_error(message)

func town(x: float, y: float, z: float) -> Vector3: return TownZone.ORIGIN+Vector3(x,y,z)

func hold_w(pressed: bool) -> void:
	var key := InputEventKey.new()
	key.physical_keycode = KEY_W
	key.pressed = pressed
	Input.parse_input_event(key)

# Walks to a point on the ground plane; fails if the body stops making progress.
func walk_to(target: Vector3, label: String, timeout := 40.0) -> bool:
	var walker: RoomWalker = game.walker
	var stuck := 0.0
	var last := walker.global_position
	var elapsed := 0.0
	hold_w(true)
	while elapsed < timeout:
		var flat := Vector3(target.x,walker.global_position.y+1.5,target.z)
		walker.aim(flat)
		# Godot releases held keys when the (background) test window loses focus: keep it held.
		if not Input.is_physical_key_pressed(KEY_W): hold_w(true)
		await physics_frame
		elapsed += 1.0/Engine.physics_ticks_per_second
		var moved := walker.global_position.distance_to(last)
		walked += moved
		stuck = stuck+1.0/Engine.physics_ticks_per_second if moved < .005 else 0.0
		last = walker.global_position
		if Vector2(walker.global_position.x-target.x,walker.global_position.z-target.z).length() < .45: break
		if stuck > 1.5: break
	hold_w(false)
	walk_time += elapsed
	var ok: bool = Vector2(walker.global_position.x-target.x,walker.global_position.z-target.z).length() < .6
	check(ok,"Walk reaches "+label+" (at "+str((walker.global_position-TownZone.ORIGIN).snapped(Vector3.ONE*.1))+" town-local)")
	return ok

# Walks toward a point without asserting arrival (for obstacles that should hold).
func try_walk(target: Vector3, seconds: float) -> void:
	hold_w(true)
	var elapsed := 0.0
	while elapsed < seconds:
		game.walker.aim(Vector3(target.x,game.walker.global_position.y+1.5,target.z))
		if not Input.is_physical_key_pressed(KEY_W): hold_w(true)
		await physics_frame
		elapsed += 1.0/Engine.physics_ticks_per_second
	hold_w(false)

func capture(name: String, at: Vector3, look: Vector3) -> void:
	game.walker.set_physics_process(false)
	game.walker.global_position = at
	game.walker.aim(look)
	for frame in 10: await process_frame
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(dest.path_join(name+".png")) == OK,"Capture "+name)
	game.walker.set_physics_process(true)

func run() -> void:
	dest = OS.get_environment("LHC_QA_DIR")
	DirAccess.make_dir_recursive_absolute(dest)
	game = load("res://scenes/campaign.tscn").instantiate()
	root.add_child(game)
	game.start_fresh()
	game.ui.close()
	game.weather.frozen = true
	game.weather.set_time(2.0)
	check(is_instance_valid(game.town) and game.town.doors.has("dinerdoor") and game.town.doors.has("homedoor"),"Town built with its doors")
	# Bedroom door -> porch.
	game.place("bedroom",Vector3(-1.75,.03,1.80),Vector3(-1.75,1.2,2.70))
	await physics_frame
	check(game.walker.target() == "door","Bedroom door is interactive")
	game.interact("door")
	await create_timer(1.2).timeout
	check(game.zone == "street" and game.walker.global_position.distance_to(town(6.9,.4,0)) < .6,"Front door leads to the porch")
	check(not game.is_modal,"Control returns after the fade")
	# Porch -> sidewalk -> cross -> diner door.
	await walk_to(town(5.0,0,0),"porch steps down to the sidewalk")
	await walk_to(town(5.0,0,-30),"east sidewalk (clear of the lamp posts at x 5.8)")
	await walk_to(town(-5.0,0,-30),"road crossing to the west sidewalk")
	await walk_to(town(-5.0,0,-51.2),"west sidewalk to the diner")
	await walk_to(town(-5.9,0,-51.2),"diner entrance")
	check(game.town.area_of(game.walker.global_position) == "street","Outside the diner counts as street")
	game.walker.aim(town(-8,1.6,-51.2))
	await physics_frame
	check(game.walker.target() == "dinerdoor","Diner door is interactive")
	await try_walk(town(-7.6,0,-51.2),3.0)
	check(game.walker.global_position.x > TownZone.ORIGIN.x-6.6,"Closed door is solid")
	game.interact("dinerdoor")
	await create_timer(.6).timeout
	check(game.town.is_open("dinerdoor"),"Diner door opens")
	await walk_to(town(-7.6,0,-51.2),"diner inside the door")
	check(game.town.area_of(game.walker.global_position) == "diner","Inside the diner counts as diner")
	await walk_to(town(-9.7,0,-51.2),"entry, past the first booth")
	await walk_to(town(-9.8,0,-57.0),"aisle by the counter, up to Hannah's booth")
	await walk_to(town(-9.7,0,-51.2),"back down the aisle")
	await walk_to(town(-7.6,0,-51.2),"back to the door")
	await walk_to(town(-5.6,0,-51.2),"out on the sidewalk")
	await walk_to(town(-5.0,0,-63.7),"alley mouth")
	await walk_to(town(-12.1,0,-63.6),"service door")
	check(game.town.area_of(game.walker.global_position) == "alley","Alley area")
	game.walker.aim(town(-12.1,1.2,-62.0))
	await physics_frame
	check(game.walker.target() == "servicedoor","Service door is interactive")
	game.interact("servicedoor")
	check(game.ui.notice.text == "It won't open." and not game.is_modal,"Service door: understated feedback, no panel")
	await walk_to(town(-20.5,0,-63.7),"alley end by the fence")
	await walk_to(town(-5.0,0,-63.7),"back out of the alley")
	await walk_to(town(-5.0,0,-30),"west sidewalk south")
	await walk_to(town(5.0,0,-30),"back across the road")
	await walk_to(town(5.0,0,0),"in front of the house")
	await walk_to(town(6.9,0,0),"porch steps up")
	game.walker.aim(town(8.5,1.6,0))
	await physics_frame
	check(game.walker.target() == "homedoor","House door is interactive")
	game.interact("homedoor")
	await create_timer(1.2).timeout
	check(game.zone == "bedroom" and game.walker.global_position.distance_to(Vector3(-1.55,.03,1.75)) < .6,"House door returns to the bedroom")
	game.save_game(false)
	check(game.save_error == OK,"Save after the round trip")
	var minutes := walk_time/60.0
	check(minutes < 2.0,"Whole round trip under two minutes of walking (%.2f min)" % minutes)
	# Curbs, head-on, both directions and both sides: no slowdown beyond plain walking time.
	game.place("street",town(2.5,0,-10),town(5.0,1.6,-10))
	for leg in [[town(5.0,0,-10),"up the east curb"],[town(2.5,0,-10),"down the east curb"],[town(-2.5,0,-30),"across the road"],[town(-5.0,0,-30),"up the west curb"],[town(-2.5,0,-30),"down the west curb"]]:
		var before := walk_time
		var start: Vector3 = game.walker.global_position
		await walk_to(leg[0],leg[1])
		var ideal: float = Vector2(start.x-leg[0].x,start.z-leg[0].z).length()/RoomWalker.SPEED
		check(walk_time-before < ideal+0.6,"%s without slowing down (%.2f s for %.2f s of walking)" % [leg[1],walk_time-before,ideal])
	# Review views, frozen rain, same light: street from the porch, diner front, interior, alley.
	game.place("street",town(6.9,.4,0),town(-4,1.4,0))
	await capture("01_porch_to_street",town(6.9,.4,0),town(-6,1.8,-14))
	await capture("02_street_north",town(4.6,.15,-14),town(-4,2.0,-50))
	await capture("03_diner_storefront",town(3.0,0,-56),town(-7,2.2,-56))
	await capture("04_diner_inside",town(-7.6,.15,-51.0),town(-12.5,1.2,-57.5))
	await capture("05_hannah_booth_view",town(-9.8,.15,-55.0),town(-7.2,1.0,-57.9))
	await capture("06_alley_approach",town(-4.8,.15,-63.8),town(-20,1.4,-63.8))
	await capture("07_service_door",town(-14.5,.03,-64.2),town(-12.1,1.3,-62.0))
	await capture("08_street_south",town(-5.4,.15,-48),town(4,2.0,0))
	var report := FileAccess.open(dest.path_join("town_checks.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"walked_m":walked,"walk_minutes":minutes},"  "))
	report.close()
	print("TOWN CHECKS: %d checks, %d failures, walked %.1f m in %.2f min" % [checks,failures.size(),walked,minutes])
	game.campaign_started = false
	quit(0 if failures.is_empty() else 1)
