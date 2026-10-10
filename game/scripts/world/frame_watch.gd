class_name FrameWatch
extends Node

# Diagnostic V0.20 : chaque image de plus de 60 ms est notée dans user://logs/godot.log
# avec son contexte, pour retrouver la cause des freezes ressentis en jeu.
const THRESHOLD_MS := 60.0
var game: Node
var last := 0
var started := 0
var last_event := "-"

func _init(controller: Node) -> void:
	game = controller

func _ready() -> void:
	process_priority = -1000
	started = Time.get_ticks_msec()
	RenderingServer.viewport_set_measure_render_time(get_viewport().get_viewport_rid(),true)

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed: last_event = "key "+OS.get_keycode_string(event.physical_keycode)
	elif event is InputEventMouseButton and event.pressed: last_event = "mouse button"

func _process(_delta: float) -> void:
	var now := Time.get_ticks_usec()
	if last > 0:
		var ms := (now-last)/1000.0
		if ms > THRESHOLD_MS:
			var computer = game.get("computer")
			var walker = game.get("walker")
			var rid := get_viewport().get_viewport_rid()
			print("[FREEZE] %.0f ms à t=%.1fs | script %.1f ms physique %.1f ms rendu cpu %.1f gpu %.1f ms | pc=%s modal=%s | pos=%s | dernière entrée=%s | draw calls=%d | objets=%d | mémoire=%.0f Mo" % [
				ms,(Time.get_ticks_msec()-started)/1000.0,
				Performance.get_monitor(Performance.TIME_PROCESS)*1000.0,Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)*1000.0,
				RenderingServer.viewport_get_measured_render_time_cpu(rid),RenderingServer.viewport_get_measured_render_time_gpu(rid),
				str(computer.active) if computer else "?",str(game.get("is_modal")),
				str(walker.global_position.snapped(Vector3.ONE*.1)) if walker else "?",last_event,
				Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),
				Performance.get_monitor(Performance.OBJECT_COUNT),
				Performance.get_monitor(Performance.MEMORY_STATIC)/1048576.0])
	last = now
