extends SceneTree
# Golden Fall home loop QA (docs/golden_fall/09_PRODUCTION_AND_TESTS.md: P01, P03, P06, P15, P17).
# Three successive processes share one isolated save: day1 -> day2 -> day3/end.
# LHC_QA_DIR, LHC_CAMPAIGN_SAVE, LHC_CAMPAIGN_STAGE=day1|day2|day3 ; run with -- --campaign-check
var checks := 0
var failures: Array[String] = []
var game: Node
var dest: String
const FRENCH := ["é","è","à","ç","ê","ù","â","î","ô","Sauvegarde","Journal de","Recherche","Démarrer"]

func _initialize() -> void: run.call_deferred()

func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures.append(message)
		push_error(message)

func capture(name: String) -> void:
	for frame in 8: await process_frame
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(dest.path_join(name+".png")) == OK,"Capture "+name)

func click(name: String) -> void:
	for frame in 3: await process_frame
	var target: Vector2 = game.pc_target(name)
	check(target.x >= 0,"Physical click target exists: "+name)
	if target.x >= 0: await game.pc_click(target)

func visible_texts(node: Node) -> Array:
	var texts: Array = []
	for child in node.find_children("*","",true,false):
		if (child is Label or child is Button) and child.is_visible_in_tree(): texts.append(str(child.text))
	return texts

func english_only(node: Node, where: String) -> void:
	var bad: Array = visible_texts(node).filter(func(t): return FRENCH.any(func(m): return m in t))
	check(bad.is_empty(),"US English only in "+where+": "+str(bad))

func panel_buttons() -> Array:
	return game.ui.modal.find_children("*","Button",true,false).map(func(b): return str(b.text)) if game.ui.modal else []

func sleep_through_bed() -> void:
	game.interact("bed")
	var labels := panel_buttons()
	check("Sleep" in labels and "Not yet" in labels,"Bed asks before sleeping: "+str(labels))
	check(not labels.any(func(t): return "Study" in t or "Rest" in t),"No Study/Rest activity buttons (P17)")
	game.sleep_day()

func run() -> void:
	dest = OS.get_environment("LHC_QA_DIR")
	DirAccess.make_dir_recursive_absolute(dest)
	var stage := OS.get_environment("LHC_CAMPAIGN_STAGE")
	game = load("res://scenes/campaign.tscn").instantiate()
	root.add_child(game)
	check(game.qa_mode and game.campaign_path() == OS.get_environment("LHC_CAMPAIGN_SAVE"),"Isolated test save")
	check(game.room_triangle_count+game.weather.triangle_count() == 7970,"Bedroom geometry unchanged (P01)")
	game.weather.frozen = true
	game.weather.set_time(2.0)
	english_only(game.ui.root,"title menu")
	if stage == "day1":
		game.start_fresh()
		var state: GoldenState = game.state
		check(state.data.day_index == 0 and state.date() == "2003-10-15" and state.clock() == "4:10 PM","Day 1 is Wednesday Oct 15, 4:10 PM")
		check(Calendar.long_date(state.date()) == "Wednesday, October 15","US calendar wording")
		check(game.ui.root.find_children("*","Button",true,false).is_empty(),"No HUD buttons while exploring")
		game.interact("desk")
		check(not panel_buttons().any(func(t): return "Study" in t),"Desk has no study activity (P17)")
		game.ui.close()
		game.interact("pc")
		await create_timer(1.2).timeout
		check(game.computer.active,"PC opens")
		check(game.computer.desktop.date_caption.text == "OCTOBER 15, 2003" and game.computer.desktop.clock_caption.text == "4:10 PM","Desktop date and clock follow the day")
		await click("Icon_agenda")
		check(game.computer.desktop.windows.has("agenda"),"Real click opens Calendar")
		await capture("01_calendar")
		await click("Icon_messages")
		check(game.computer.desktop.windows.has("messages") and "im_day1" in state.data.read_messages,"Messages shows the day 1 IM and marks it read")
		for id in game.computer.desktop.windows.keys(): game.computer.desktop.close_window(str(id))
		await click("Icon_browser")
		check(game.computer.desktop.windows.has("browser"),"Browser opens without any time cost")
		game.computer.desktop.browse("","diner")
		var result = game.computer.desktop.browser_body.find_child("Result_diner_review",true,false)
		check(result != null,"Search finds the diner review")
		game.computer.desktop.browse("diner_review","diner")
		await click("NoteClue")
		check(state.data.observations.any(func(o): return o.id == "web_diner_review"),"Add to journal records the page")
		await capture("02_browser")
		await click("Icon_save")
		await click("ManualSave")
		check(game.save_error == OK and game.computer.desktop.windows.save.find_child("SaveStatus",true,false) != null,"Manual save shows its result inside the CRT")
		english_only(game.computer.desktop,"PC desktop")
		await capture("03_save")
		check(state.data.day_index == 0 and state.data.time_slot == "afternoon","Using the PC costs no time")
		game.computer.leave()
		await game.computer.camera_tween.finished
		check(not game.computer.active and not game.is_modal,"Leaving the PC returns to the room")
		sleep_through_bed()
		check(state.data.day_index == 1 and state.date() == "2003-10-16" and not state.data.finished_micro_mvp,"Sleep advances exactly one day (P06)")
		english_only(game.ui.root,"room after sleep")
	elif stage == "day2":
		game.continue_game()
		var state: GoldenState = game.state
		check(state.data.day_index == 1,"Reload keeps Thursday, no extra day (P06)")
		check(state.data.observations.size() == 1 and "im_day1" in state.data.read_messages,"Journal and read IM survive a new process")
		check(state.unread_message().get("id") == "im_day2","Thursday brings a new IM")
		game.interact("pc")
		await create_timer(1.2).timeout
		check(game.computer.desktop.date_caption.text == "OCTOBER 16, 2003","Desktop shows Thursday")
		await click("Icon_notes")
		check(game.computer.desktop.windows.has("notes"),"Journal opens")
		await capture("04_journal")
		game.computer.leave()
		await game.computer.camera_tween.finished
		sleep_through_bed()
		check(state.data.day_index == 2 and state.date() == "2003-10-17","Second sleep reaches Friday")
	elif stage == "day3":
		game.continue_game()
		var state: GoldenState = game.state
		check(state.data.day_index == 2 and state.is_last_day(),"Reload keeps Friday")
		sleep_through_bed()
		check(state.data.finished_micro_mvp and state.data.day_index == 2,"Friday sleep ends the prototype without a fourth day")
		check(game.ui.modal != null and "Back to title" in panel_buttons(),"Neutral end screen")
		await capture("05_end")
		game.return_to_title()
		var original: Dictionary = state.data.duplicate(true)
		var bad: Dictionary = original.duplicate(true)
		bad.schema_version = "0.8.0"
		var file := FileAccess.open(game.campaign_path(),FileAccess.WRITE)
		file.store_string(JSON.stringify(bad))
		file.close()
		game.continue_game()
		check(state.data == original,"A foreign save cannot replace the live state")
		game.start_fresh()
		check(game.state.data.day_index == 0 and game.state.data.observations.is_empty() and not game.state.data.finished_micro_mvp,"New game starts clean on Wednesday")
	else: check(false,"Unknown stage "+stage)
	var report := FileAccess.open(dest.path_join(stage+"_checks.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"stage":stage,"checks":checks,"failures":failures},"  "))
	report.close()
	print("GOLDEN ",stage,": ",checks," checks, ",failures.size()," failures")
	game.campaign_started = false
	quit(0 if failures.is_empty() else 1)
