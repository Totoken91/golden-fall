extends SceneTree
func _initialize() -> void:run.call_deferred()
func run() -> void:
    var game=load("res://scenes/room_review.tscn").instantiate()
    root.add_child(game)
    game.qa_mode=true;game.set_modal(true);game.ui.root.hide()
    if is_instance_valid(game.ambience):game.ambience.stop()
    game.walker.set_physics_process(false)
    game.weather.frozen=true;game.weather.set_time(2.0)
    for i in 3:await process_frame
    var dest:=OS.get_environment("LHC_REFERENCE_DIR")
    var prefix:=OS.get_environment("LHC_REFERENCE_PREFIX")
    var poses: Dictionary={}
    for shot in [
        ["25_casque",Vector3(-1.50,1.30,-1.76),Vector3(-1.6,.95,-2.22),48.0],
        ["26_crt_ventilation",Vector3(-.07,1.40,-1.90),Vector3(-.65,1.16,-2.20),46.0],
        ["27_chevet",Vector3(.18,1.35,-1.75),Vector3(.78,.84,-2.43),54.0],
        ["28_rideau",Vector3(.02,1.60,-1.70),Vector3(.46,1.14,-2.45),55.0],
        ["29_amenagement",Vector3(.60,2.38,-.75),Vector3(1.65,.63,-2.40),62.0],
        ["30_contacts_sol",Vector3(-.70,.35,-.10),Vector3(-1.58,.22,-1.70),62.0]
    ]:
        game.walker.camera.position=Vector3(0,1.62,0)
        game.walker.camera.fov=shot[3]
        await game.pose(shot[1]-Vector3(0,1.62,0),shot[2])
        for i in 3:await process_frame
        await RenderingServer.frame_post_draw
        assert(root.get_texture().get_image().save_png(dest.path_join(prefix+shot[0]+".png"))==OK)
        poses[shot[0]]={"position":var_to_str(game.walker.camera.global_position),"basis":var_to_str(game.walker.camera.global_basis),"fov":game.walker.camera.fov,"weather_time":game.weather.elapsed,"modal_input_locked":game.is_modal}
    var file:=FileAccess.open(dest.path_join(prefix+"contact_cameras.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(poses,"  "));file.close()
    print("EXACT CONTACT CAPTURES: 6, input locked, camera matrices saved, prefix=",prefix)
    quit()
