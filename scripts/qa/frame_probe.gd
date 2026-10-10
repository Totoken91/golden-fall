extends SceneTree
# Frame-time probe along a fixed path (room, PC entry, apps, exit). Reports every frame
# over 50 ms with the step it happened in. Works on V0.19 and later PCKs.
var game: Node
var step := "boot"
var last := 0
var spikes: Array = []
var totals := {}

func _initialize() -> void:
	process_frame.connect(tick)
	run.call_deferred()

func tick() -> void:
	var now := Time.get_ticks_usec()
	if last > 0:
		var ms := (now-last)/1000.0
		totals[step] = totals.get(step,[0,0.0,0.0])
		totals[step][0] += 1
		totals[step][1] += ms
		totals[step][2] = maxf(totals[step][2],ms)
		if ms > 50.0: spikes.append("%s %.0f ms" % [step,ms])
	last = now

func phase(name: String, seconds: float) -> void:
	step = name
	await create_timer(seconds).timeout

func press(name: String) -> void:
	for button in game.computer.desktop.find_children("*","Button",true,false):
		if button.name == name:
			button.pressed.emit()
			return

func run() -> void:
	game = load("res://scenes/campaign.tscn").instantiate()
	root.add_child(game)
	step = "load"
	game.start_fresh()
	game.ui.close()
	await phase("room_idle",4.0)
	step = "look_around"
	for i in 240:
		game.walker.look(Vector2(12,0))
		await process_frame
	step = "pc_enter"
	game.interact("pc")
	await phase("pc_enter",1.5)
	await phase("pc_idle",3.0)
	for app in ["Icon_agenda","Icon_notes","Icon_save","Icon_browser","Icon_files"]:
		step = "open "+app
		press(app)
		await phase("open "+app,.8)
	step = "start_menu"
	press("StartButton")
	await phase("start_menu",.8)
	await phase("pc_idle_windows",3.0)
	step = "pc_leave"
	game.finish_activity()
	await phase("pc_leave",1.5)
	await phase("room_after",4.0)
	step = "pc_reenter"
	game.interact("pc")
	await phase("pc_reenter",2.0)
	for key in totals:
		var t: Array = totals[key]
		print("STEP %-22s frames %4d  avg %6.1f ms  max %6.1f ms" % [key,t[0],t[1]/t[0],t[2]])
	print("SPIKES>50ms: ",spikes)
	game.campaign_started = false
	quit(0)
