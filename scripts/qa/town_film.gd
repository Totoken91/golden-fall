extends SceneTree
# Stage 1 review film: real engine walk from the bedroom door to the porch, up the street, across,
# into the diner. Use with --write-movie <file>.avi --fixed-fps 30 and -- --campaign-check.
var game: Node

func _initialize() -> void: run.call_deferred()

func town(x: float, z: float) -> Vector3: return TownZone.ORIGIN+Vector3(x,0,z)

func key_w(pressed: bool) -> void:
	var key := InputEventKey.new()
	key.physical_keycode = KEY_W
	key.pressed = pressed
	Input.parse_input_event(key)

# Smoothly turns toward the next point while walking, like a player would.
func walk_to(target: Vector3, max_seconds := 30.0) -> void:
	var walker: RoomWalker = game.walker
	var elapsed := 0.0
	while elapsed < max_seconds:
		var to := Vector2(target.x-walker.global_position.x,target.z-walker.global_position.z)
		if to.length() < .5: break
		var wanted := atan2(-to.x,-to.y)
		walker.rotation.y = lerp_angle(walker.rotation.y,wanted,.08)
		walker.pitch = lerpf(walker.pitch,-.05,.05)
		walker.camera.rotation.x = walker.pitch
		if not Input.is_physical_key_pressed(KEY_W): key_w(true)
		await physics_frame
		elapsed += 1.0/Engine.physics_ticks_per_second
	key_w(false)

func look_toward(target: Vector3, seconds: float) -> void:
	var walker: RoomWalker = game.walker
	var elapsed := 0.0
	while elapsed < seconds:
		var to := Vector2(target.x-walker.global_position.x,target.z-walker.global_position.z)
		walker.rotation.y = lerp_angle(walker.rotation.y,atan2(-to.x,-to.y),.05)
		await physics_frame
		elapsed += 1.0/Engine.physics_ticks_per_second

func run() -> void:
	game = load("res://scenes/campaign.tscn").instantiate()
	root.add_child(game)
	game.start_fresh()
	game.ui.close()
	game.place("bedroom",Vector3(-1.75,.03,1.80),Vector3(-1.75,1.2,2.70))
	for i in 20: await process_frame
	game.interact("door")
	await create_timer(1.3).timeout
	await look_toward(town(-4,-6),1.2)
	await walk_to(town(5.0,-1.0))
	await walk_to(town(5.0,-30))
	await walk_to(town(-5.0,-34))
	await walk_to(town(-5.0,-51.2))
	await walk_to(town(-5.9,-51.2))
	game.interact("dinerdoor")
	await create_timer(.6).timeout
	await walk_to(town(-8.8,-51.2))
	await look_toward(town(-7.2,-57.9),2.0)
	await create_timer(1.0).timeout
	game.campaign_started = false
	quit(0)
