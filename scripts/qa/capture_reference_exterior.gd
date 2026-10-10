extends SceneTree

func _initialize() -> void:run.call_deferred()

func run() -> void:
    var game = load("res://scenes/room_review.tscn").instantiate()
    root.add_child(game)
    game.qa_mode = true
    game.ui.root.hide()
    Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
    if is_instance_valid(game.ambience):game.ambience.stop()
    game.walker.set_physics_process(false)
    await game.pose(Vector3(-.85,.03,-1.55),Vector3(-.80,2.10,-8.0))
    game.weather.frozen = true
    game.weather.set_time(2.0)
    for i in 3:await process_frame
    await RenderingServer.frame_post_draw
    var dest := OS.get_environment("LHC_REFERENCE_DIR")
    var result := root.get_texture().get_image().save_png(dest.path_join("00_exterieur_v012.png"))
    var info := {"camera_position":var_to_str(game.walker.camera.global_position),"camera_basis":var_to_str(game.walker.camera.global_basis),"vertical_fov":game.walker.camera.fov,"weather_time":game.weather.elapsed,"source":"Untouched V0.12 project, custom inspection camera only"}
    var file := FileAccess.open(dest.path_join("camera_exterieur_v012.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(info,"  "));file.close()
    print("BASELINE EXTERIOR V0.12: ",result)
    quit(0 if result == OK else 1)
