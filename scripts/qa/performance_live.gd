extends SceneTree
func _initialize() -> void:run.call_deferred()
func run() -> void:
    var game=load("res://scenes/room_review.tscn").instantiate()
    root.add_child(game)
    game.qa_mode=true;game.set_modal(true);game.ui.root.hide()
    game.walker.set_physics_process(false)
    await game.pose(Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45))
    game.weather.frozen=false;game.weather.set_time(2.0)
    var times: Array[float]=[]
    var before:=Time.get_ticks_usec()
    for i in 150:
        await process_frame
        var now:=Time.get_ticks_usec()
        if i>=30:times.append((now-before)/1000.0)
        before=now
    times.sort()
    var total:=0.0
    for timing in times:total+=timing
    var info: Dictionary={"samples":times.size(),"average_frame_ms":total/times.size(),"p95_frame_ms":times[int(times.size()*.95)],"godot_static_mib":Performance.get_monitor(Performance.MEMORY_STATIC)/1048576.0,"gpu":RenderingServer.get_video_adapter_name(),"world_pixels":[640,360],"room_triangles":game.room_triangle_count,"total_with_rain_triangles":game.room_triangle_count+game.weather.triangle_count(),"viewport_primitives":game.view.get_render_info(Viewport.RENDER_INFO_TYPE_VISIBLE,Viewport.RENDER_INFO_PRIMITIVES_IN_FRAME),"viewport_draw_calls":game.view.get_render_info(Viewport.RENDER_INFO_TYPE_VISIBLE,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),"weather_live":true,"audio_live":is_instance_valid(game.ambience) and game.ambience.playing,"note":"Single stationary doorway view, live weather and audio, 30 warmup frames plus 120 samples. No other capture/build process active. Not a hardware target benchmark."}
    var file:=FileAccess.open(OS.get_environment("LHC_QA_DIR").path_join("performance_live.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(info,"  "));file.close()
    print("LIVE PERFORMANCE: ",JSON.stringify(info))
    quit()
