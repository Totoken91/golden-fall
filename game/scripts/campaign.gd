extends RoomScene

# Golden Fall micro-MVP campaign. The independent review scene (room_review.gd) shares only RoomScene.
# Time never moves for walking, reading or using the PC; only sleep (and later, committed
# conversations) advances it. See docs/golden_fall/01_MICRO_MVP_GAMEPLAY.md.
const SAVE_PATH := SaveManager.PATH
var campaign_started := false
var save_error := OK

func _ready() -> void:
	super._ready()
	show_menu()

func detect_qa_mode() -> bool: return "--campaign-check" in OS.get_cmdline_user_args()
func prompt_captions() -> Dictionary:
	return {"pc":"use the computer", "desk":"look at the desk", "bed":"sleep", "door":"go outside"}

func campaign_path() -> String:
	# Automated tests must never replace the player's slot.
	var override := OS.get_environment("LHC_CAMPAIGN_SAVE")
	return override if qa_mode and not override.is_empty() else SAVE_PATH

func set_modal(value: bool) -> void:
	super.set_modal(value or not campaign_started or state.data.finished_micro_mvp)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode in [KEY_F5,KEY_TAB,KEY_J]:
			if campaign_started: ui.toast("Your journal and saves are on the computer.")
			return
		if event.physical_keycode == KEY_ESCAPE:
			if is_modal and campaign_started and not state.data.finished_micro_mvp: ui.close()
			else: show_menu()
			return
	if campaign_started and not state.data.finished_micro_mvp: super._unhandled_input(event)

func reset_desktop() -> void:
	for id in computer.desktop.windows.keys(): computer.desktop.close_window(id)
	computer.desktop.browser_history.clear()
	computer.desktop.browser_page = ""
	computer.desktop.browser_query = ""
	computer.desktop.start_menu.hide()

func new_game() -> void:
	if computer.active or computer.transitioning: return
	if campaign_started or FileAccess.file_exists(campaign_path()):
		var col := ui.panel("Start over?",Rect2(300,200,680,300))
		col.add_child(ui.paragraph("Your saved progress will be replaced. Start again on Wednesday afternoon?"))
		col.add_child(ui.button("Start over",start_fresh))
		col.add_child(ui.button("Keep my save",show_menu))
		return
	start_fresh()

func start_fresh() -> void:
	state.data = state.new_game()
	web = WebArchive.new(state)
	reset_desktop()
	campaign_started = true
	walker.position = Vector3(-1.68,.03,2.30)
	walker.velocity = Vector3.ZERO
	walker.aim(Vector3(-.05,.95,-1.45))
	walker.camera.fov = 62
	ui.close()
	save_game(false)
	announce_day()

func announce_day() -> void:
	ui.toast("%s · %s" % [Calendar.long_date(state.date()),state.clock()])

func show_menu() -> void:
	var col := ui.panel("Golden Fall",Rect2(330,110,620,500))
	col.add_child(ui.paragraph("Morrow Creek, Oregon · October 2003",ui.ink,20))
	if campaign_started:
		if not state.data.finished_micro_mvp: col.add_child(ui.button("Resume",ui.close))
		col.add_child(ui.button("Back to title",return_to_title))
	else:
		var resume := ui.button("Continue",continue_game)
		resume.disabled = not FileAccess.file_exists(campaign_path())
		col.add_child(resume)
		col.add_child(ui.button("New game",new_game))
	col.add_child(ui.button("Rain sound: " + ("on" if sound_enabled else "off"),func(): toggle_sound(); show_menu()))
	col.add_child(ui.button("Quit",close_game))
	col.add_child(ui.paragraph("WASD / ZQSD to move · mouse to look · E to interact\nEsc to pause · progress saves automatically",ui.ink,16))

func return_to_title() -> void:
	if computer.active or computer.transitioning: return
	if campaign_started: save_game(false)
	campaign_started = false
	show_menu()

func open_computer(app: String = "") -> void:
	if not campaign_started or computer.active or computer.transitioning: return
	computer.enter()
	computer.desktop.refresh_apps()
	if app!="": computer.desktop.open_app(app)
	save_game(false)

func interact(id: String) -> void:
	if not campaign_started or state.data.finished_micro_mvp or computer.transitioning: return
	match id:
		"pc": open_computer()
		"desk":
			var col := ui.panel("The desk",Rect2(300,180,680,330))
			col.add_child(ui.paragraph("Schoolbooks you haven't opened since Monday, a mug gone cold, and a cassette with a label you wrote in pencil and can't read anymore."))
			col.add_child(ui.button("Leave it",ui.close))
		"bed": show_bed()
		"door":
			var col := ui.panel("The front door",Rect2(300,180,680,330))
			col.add_child(ui.paragraph("Rain on the porch steps. You can hear the gutter running."))
			col.add_child(ui.paragraph("(The street isn't in this build yet.)",ui.ink,17))
			col.add_child(ui.button("Stay in",ui.close))

func show_bed() -> void:
	var col := ui.panel("Sleep?",Rect2(300,170,680,360))
	if state.is_last_day():
		col.add_child(ui.paragraph("It's still raining. Friday is almost over."))
		col.add_child(ui.button("Sleep",sleep_day))
	else:
		var tomorrow: String = GoldenState.DATES[int(state.data.day_index)+1]
		col.add_child(ui.paragraph("The rain sounds closer with the lights off. Sleep until %s?" % Calendar.weekday(tomorrow)))
		col.add_child(ui.button("Sleep",sleep_day))
	col.add_child(ui.button("Not yet",ui.close))

func sleep_day() -> void:
	if not campaign_started or computer.active or computer.transitioning: return
	save_game(false)
	if not state.sleep(): return
	save_game(false)
	if state.data.finished_micro_mvp: show_end()
	else:
		ui.close()
		walker.position = Vector3(.65,.03,-.40)
		walker.velocity = Vector3.ZERO
		walker.aim(Vector3(-.85,1.0,-1.6))
		announce_day()

func show_end() -> void:
	var col := ui.panel("End of this prototype",Rect2(300,150,680,420))
	col.add_child(ui.paragraph("Thanks for playing this early build of Golden Fall."))
	col.add_child(ui.paragraph("The street, the diner and the people in them come next.",ui.ink,18))
	col.add_child(ui.button("Back to title",return_to_title))

func computer_closed() -> void:
	save_game(false)

func snapshot() -> void:
	state.data.location = "bedroom"
	state.data.view = {"position":[walker.position.x,walker.position.y,walker.position.z],"yaw":walker.rotation.y,"pitch":walker.pitch}
	var desktop := computer.desktop
	state.data.pc = {"open":computer.active,"apps":desktop.windows.keys(),"page":desktop.browser_page,"query":desktop.browser_query}

func save_game(notify: bool = true) -> void:
	if not campaign_started: return
	snapshot()
	save_error = SaveManager.write(state,campaign_path())
	if save_error!=OK: ui.toast("Couldn't save (error %s)." % save_error)
	elif notify and not computer.active: ui.toast("Progress saved.")

func continue_game() -> void:
	if computer.active or computer.transitioning: return
	var candidate := GoldenState.new(db)
	if not SaveManager.read_into(candidate,campaign_path()):
		ui.toast("This save can't be loaded.")
		return
	state.data = candidate.data
	web = WebArchive.new(state)
	campaign_started = true
	reset_desktop()
	var stored: Dictionary = state.data.view
	var pos: Array = stored.get("position",[-1.68,.03,2.30])
	walker.position = Vector3(pos[0],pos[1],pos[2])
	walker.velocity = Vector3.ZERO
	walker.rotation.y = float(stored.get("yaw",0))
	walker.pitch = float(stored.get("pitch",0))
	walker.camera.position = Vector3(0,1.62,0)
	walker.camera.rotation = Vector3(walker.pitch,0,0)
	walker.camera.fov = 62
	ui.close()
	if state.data.finished_micro_mvp:
		show_end()
		return
	var pc: Dictionary = state.data.pc
	if bool(pc.get("open",false)):
		computer.enter()
		var apps = pc.get("apps",[])
		if apps is Array:
			for app in apps:
				if app in CedarDesktop.APP_NAMES and app != "browser": computer.desktop.open_app(str(app))
			if "browser" in apps: computer.desktop.open_browser(str(pc.get("page","")),str(pc.get("query","")))
	else: announce_day()

func close_game() -> void:
	if closing: return
	if campaign_started: save_game(false)
	super.close_game()
