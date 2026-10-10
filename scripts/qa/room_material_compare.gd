extends SceneTree
func _initialize() -> void: run.call_deferred()

func run() -> void:
    var dest := OS.get_environment("LHC_MATERIAL_COMPARE_DIR")
    if dest.is_empty(): dest = ProjectSettings.globalize_path("res://").path_join("../captures/cohesion_v017")
    DirAccess.make_dir_recursive_absolute(dest)
    var game = load("res://scenes/room_review.tscn").instantiate()
    root.add_child(game)
    game.qa_mode=true
    game.set_modal(true)
    game.ui.root.hide()
    if is_instance_valid(game.ambience):game.ambience.stop()
    game.walker.set_physics_process(false)
    game.weather.frozen=true
    game.weather.set_time(2.0)
    var config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/room_materials.json"))
    var before_config: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/qa_room_materials_v016.json"))
    var materials: Array = game.material_pass.applied.duplicate(true)
    print("MATERIAL TARGETS: ",JSON.stringify(materials))
    assert(materials.size()==config.surfaces.size(),"Every intended surface must be found")
    for item in materials:assert(item.size==[128,128] and item.mipmaps,"Real 128px maps with imported mipmaps")
    var wood_surfaces:=0
    for item in materials:
        if not item.texels_per_m.is_empty():
            assert(is_equal_approx(item.texels_per_m[0],float(config.cohesion.wood_target_texels_per_m)) and is_equal_approx(item.texels_per_m[1],float(config.cohesion.wood_target_texels_per_m)),"Wood texel density must match")
            wood_surfaces+=1
    assert(wood_surfaces==10)
    var geometry_checks:=0
    var maximum_normal_delta:=0.0
    for item in game.material_pass.baseline:
        if item.material.resource_name=="shade":
            assert(item.node.get_active_material(item.surface).emission_operator==item.material.emission_operator,"Shade must retain original emission operation")
        for surface in item.mesh.get_surface_count():
            var a: Array=item.mesh.surface_get_arrays(surface)
            var b: Array=item.node.mesh.surface_get_arrays(surface)
            for attribute in [Mesh.ARRAY_VERTEX,Mesh.ARRAY_NORMAL,Mesh.ARRAY_INDEX]:
                if a[attribute]!=b[attribute]:
                    print("ARRAY DIFFERENCE: ",item.node.name," attribute ",attribute)
                    if attribute==Mesh.ARRAY_NORMAL:
                        var max_delta:=0.0
                        for i in a[attribute].size():max_delta=maxf(max_delta,a[attribute][i].distance_to(b[attribute][i]))
                        print("NORMAL REPACKING MAX DELTA: ",max_delta)
                        maximum_normal_delta=maxf(maximum_normal_delta,max_delta)
                        assert(max_delta<0.0002,"Repacked flat normals changed materially")
                    else:
                        push_error("Material pass changed vertex positions or triangle indices")
                        quit(1)
                        return
                geometry_checks+=1
    var fixed: Dictionary={}
    var records: Dictionary={}
    var model: Node3D=game.scene.get_node("Bedroom") if game.scene.has_node("Bedroom") else null
    if model==null:
        for child in game.scene.get_children():
            if child is Node3D and child.find_children("*","MeshInstance3D",true,false).size()>20:model=child;break
    assert(model!=null)
    for variant in ["avant","apres"]:
        if variant=="avant":game.material_pass.apply(model,before_config.surfaces)
        else:game.material_pass.apply(model,config.surfaces)
        for pose in [
            ["chambre",Vector3(-1.68,1.65,2.30),Vector3(-.05,.95,-1.45),62.0],
            ["bureau",Vector3(-.50,1.45,-.95),Vector3(-.85,.82,-2.02),57.0],
            ["chevet",Vector3(.18,1.35,-1.75),Vector3(.78,.84,-2.43),54.0],
            ["literie",Vector3(.55,1.70,-.65),Vector3(1.92,.62,-1.92),58.0],
            ["sac",Vector3(-.90,.65,1.50),Vector3(-1.85,.26,1.03),54.0],
            ["fenetre",Vector3(-1.42,1.70,-1.30),Vector3(.04,1.55,-2.65),62.0],
            ["commode",Vector3(.65,1.40,1.08),Vector3(2.34,.75,1.08),62.0],
            ["plafond",Vector3(-.8,1.65,.7),Vector3(-.4,2.64,-1.6),62.0],
            ["porte",Vector3(-.52,1.65,1.12),Vector3(-1.75,1.18,2.7),62.0]
        ]:
            game.walker.camera.fov=pose[3]
            await game.pose(pose[1]-Vector3(0,1.62,0),pose[2])
            if not fixed.has(pose[0]):fixed[pose[0]]={"body":game.walker.transform,"camera":game.walker.camera.transform,"pitch":game.walker.pitch}
            else:
                game.walker.transform=fixed[pose[0]].body
                game.walker.camera.transform=fixed[pose[0]].camera
                game.walker.pitch=fixed[pose[0]].pitch
            for frame in 8:await process_frame
            await RenderingServer.frame_post_draw
            var name: String=variant+"_"+pose[0]
            assert(root.get_texture().get_image().save_png(dest.path_join(name+".png"))==OK)
            records[name]={"position":var_to_str(game.walker.camera.global_position),"basis":var_to_str(game.walker.camera.global_basis),
                "fov":game.walker.camera.fov,"weather_time":game.weather.elapsed,"world_size":[640,360],"triangles":game.room_triangle_count+game.weather.triangle_count()}
    var report: Dictionary={"cameras":records,"surfaces":materials,"geometry_attribute_checks":geometry_checks,"floor_binding":config.floor,
        "normal_repacking_max_delta":maximum_normal_delta,"vertices_and_indices":"exactly identical",
        "baseline":"V0.16 materials exactly; same approved parquet in both versions","wood_surfaces":wood_surfaces,"wood_target_texels_per_m":config.cohesion.wood_target_texels_per_m,"captures":records.size()}
    var file:=FileAccess.open(dest.path_join("comparison.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"  "));file.close()
    print("ROOM MATERIAL COMPARISON: ",records.size()," captures, ",materials.size()," surfaces, ",geometry_checks," unchanged geometry attributes")
    quit()
