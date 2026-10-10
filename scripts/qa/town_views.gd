extends SceneTree
# Town review captures only (art passes): same cameras, frozen rain, same weather time, so a
# before/after pair differs only by the pass. Saves the camera transforms actually captured.
# LHC_QA_DIR, LHC_CAMPAIGN_SAVE ; run with -- --campaign-check against a PCK.
const VIEWS := [
	["01_porch_to_street",Vector3(6.9,.4,0),Vector3(-6,1.8,-14)],
	["02_street_north",Vector3(4.6,.15,-14),Vector3(-4,2.0,-50)],
	["03_diner_storefront",Vector3(3.0,0,-56),Vector3(-7,2.2,-56)],
	["04_diner_inside",Vector3(-7.6,.15,-51.0),Vector3(-12.5,1.2,-57.5)],
	["05_hannah_booth_view",Vector3(-9.8,.15,-55.0),Vector3(-7.2,1.0,-57.9)],
	["06_alley_approach",Vector3(-4.8,.15,-63.8),Vector3(-20,1.4,-63.8)],
	["07_service_door",Vector3(-14.5,.03,-64.2),Vector3(-12.1,1.3,-62.0)],
	["08_street_south",Vector3(-5.4,.15,-48),Vector3(4,2.0,0)],
	# Close material views: ground at the curb, a clapboard house, the record shop brick, the roofline.
	["09_curb_close",Vector3(4.9,.15,-6),Vector3(2.4,0,-9.5)],
	["10_house_facade",Vector3(5.2,.15,-21),Vector3(10,2.2,-21)],
	["11_records_brick",Vector3(-4.6,.15,-24),Vector3(-6.5,1.8,-29)],
	["12_home_roofline",Vector3(-5.2,.15,6),Vector3(9,4.5,0)],
]
var game: Node

func _initialize() -> void: run.call_deferred()

func run() -> void:
	var dest := OS.get_environment("LHC_QA_DIR")
	DirAccess.make_dir_recursive_absolute(dest)
	game = load("res://scenes/campaign.tscn").instantiate()
	root.add_child(game)
	game.start_fresh()
	game.ui.close()
	game.weather.frozen = true
	game.weather.set_time(2.0)
	game.place("street",TownZone.ORIGIN+Vector3(6.9,.4,0),TownZone.ORIGIN+Vector3(-4,1.4,0))
	game.set_modal(true)   # no stray mouse look between aim and capture
	game.walker.set_physics_process(false)
	var cameras := {}
	var failed := 0
	for view in VIEWS:
		game.walker.global_position = TownZone.ORIGIN+view[1]
		game.walker.aim(TownZone.ORIGIN+view[2])
		for frame in 12: await process_frame
		await RenderingServer.frame_post_draw
		if root.get_texture().get_image().save_png(dest.path_join(view[0]+".png")) != OK: failed += 1
		cameras[view[0]] = var_to_str(game.walker.camera.global_transform)
	var file := FileAccess.open(dest.path_join("cameras.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(cameras,"  "))
	file.close()
	print("TOWN VIEWS: %d captured, %d failed" % [VIEWS.size()-failed,failed])
	game.campaign_started = false
	quit(0 if failed == 0 else 1)
