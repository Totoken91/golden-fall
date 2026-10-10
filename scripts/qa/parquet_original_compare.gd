extends SceneTree
## Original GLB floor versus the downloaded, reduced 128px floor. Actual engine captures.
func _initialize() -> void: run.call_deferred()

func run() -> void:
    var dest := ProjectSettings.globalize_path("res://").path_join("../captures/parquet_origine_vs_128")
    DirAccess.make_dir_recursive_absolute(dest)
    var library = load("res://scripts/world/texture_library.gd").new()
    var game = load("res://scenes/room_review.tscn").instantiate()
    root.add_child(game)
    game.qa_mode = true
    game.set_modal(true)
    game.ui.root.hide()
    if is_instance_valid(game.ambience): game.ambience.stop()
    game.walker.set_physics_process(false)
    game.weather.frozen = true
    game.weather.set_time(2.0)
    var surfaces: Array = []
    for node in game.scene.find_children("*", "MeshInstance3D", true, false):
        for surface in node.mesh.get_surface_count():
            var active = node.get_active_material(surface)
            if active is StandardMaterial3D and active.resource_name == "floor":
                var original = node.mesh.surface_get_material(surface)
                assert(original is StandardMaterial3D and original.resource_name == "floor")
                assert(original.albedo_texture != active.albedo_texture)
                surfaces.append([node,surface,original])
    assert(not surfaces.is_empty(), "Expected original floor material preserved in GLB")
    var cameras: Dictionary = {}
    var fixed_poses: Dictionary = {}
    var selected_key := "polyhaven/wood_planks/parquet_psx_128_411b6ec8"
    for variant in ["avant_origine", "apres_128"]:
        for pair in surfaces:
            if variant == "avant_origine":
                pair[0].set_surface_override_material(pair[1],pair[2])
            else:
                assert(library.apply_surface(pair[0],pair[1],selected_key,Vector2(1.8,1.8)) == OK)
        var material = surfaces[0][0].get_active_material(surfaces[0][1])
        if variant == "apres_128": assert(material.albedo_texture.get_width() == 128)
        for pose in [
            ["chambre",Vector3(-1.68,.03,2.30),Vector3(-.05,.95,-1.45)],
            ["detail",Vector3(-.65,.03,.30),Vector3(-.9,0,-.3)]
        ]:
            game.walker.camera.fov = 62.0
            await game.pose(pose[1],pose[2])
            if not fixed_poses.has(pose[0]):
                fixed_poses[pose[0]] = {"body":game.walker.transform,"camera":game.walker.camera.transform,"pitch":game.walker.pitch}
            else:
                game.walker.transform = fixed_poses[pose[0]].body
                game.walker.camera.transform = fixed_poses[pose[0]].camera
                game.walker.pitch = fixed_poses[pose[0]].pitch
            for i in 8: await process_frame
            await RenderingServer.frame_post_draw
            var name: String = variant + "_" + pose[0]
            assert(root.get_texture().get_image().save_png(dest.path_join(name+".png")) == OK)
            cameras[name] = {"position":var_to_str(game.walker.camera.global_position),
                "basis":var_to_str(game.walker.camera.global_basis),"fov":game.walker.camera.fov,
                "weather_time":game.weather.elapsed,"input_locked":game.is_modal,
                "material": "original GLB floor" if variant == "avant_origine" else selected_key,
                "texture_path":material.albedo_texture.resource_path,
                "texture_size":[material.albedo_texture.get_width(),material.albedo_texture.get_height()],
                "world_size":[640,360],"triangles":game.room_triangle_count+game.weather.triangle_count()}
    var file := FileAccess.open(dest.path_join("cameras.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(cameras,"  "))
    file.close()
    print("PARQUET ORIGINAL: 4 real captures, original GLB floor versus downloaded 128px, locked cameras")
    quit()
