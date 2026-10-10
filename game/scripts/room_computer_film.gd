class_name RoomComputerFilm
extends Node

var game: Node
var elapsed := 0.0

func _init(controller: Node) -> void:game = controller

func _process(delta: float) -> void:elapsed += delta

func pause(seconds: float) -> void:await get_tree().create_timer(seconds).timeout

func move_cursor(target: Vector2, seconds := .5) -> void:
	var origin: Vector2 = game.computer.cursor
	var frames := maxi(1,int(seconds*30))
	for i in frames:
		await game.pc_move(origin.lerp(target,float(i+1)/frames))

func _ready() -> void:
	game.set_modal(true)
	game.ui.root.hide()
	game.walker.set_physics_process(false)
	game.walker.position = Vector3(-.49,.03,-.40)
	game.walker.aim(Vector3(-.85,1.19,-1.896))
	await pause(1.5)
	game.interact("pc")
	await game.computer.camera_tween.finished
	await pause(1.2)
	await move_cursor(game.pc_target("Icon_browser"))
	await game.pc_click(game.pc_target("Icon_browser"))
	await pause(.8)
	await move_cursor(game.computer.desktop.browser_input.get_global_rect().get_center())
	await game.pc_click(game.computer.desktop.browser_input.get_global_rect().get_center())
	for character in "diner":await game.pc_key(KEY_NONE,character.unicode_at(0))
	await pause(.4)
	await game.pc_key(KEY_ENTER)
	await pause(1.0)
	var result: Button = game.computer.desktop.browser_body.get_node_or_null("Result_diner_review")
	if is_instance_valid(result):
		await move_cursor(result.get_global_rect().get_center())
		await game.pc_click(result.get_global_rect().get_center())
		await pause(1.6)
		await move_cursor(Vector2(400,300))
		for i in 6:
			for pressed in [true,false]:
				var wheel := InputEventMouseButton.new()
				wheel.set_meta("computer_qa",true)
				wheel.button_index = MOUSE_BUTTON_WHEEL_DOWN
				wheel.pressed = pressed
				Input.parse_input_event(wheel)
				await get_tree().process_frame
		var note: Button = game.computer.desktop.browser_body.get_node_or_null("NoteClue")
		if is_instance_valid(note):
			await move_cursor(note.get_global_rect().get_center())
			await game.pc_click(note.get_global_rect().get_center())
	await pause(.8)
	await move_cursor(game.pc_target("StartButton"))
	await game.pc_click(game.pc_target("StartButton"))
	await pause(.7)
	await move_cursor(game.pc_target("Start_notes"))
	await game.pc_click(game.pc_target("Start_notes"))
	await pause(1.6)
	await game.pc_key(KEY_ESCAPE)
	await game.computer.camera_tween.finished
	await pause(maxf(1.0,24.0-elapsed))
	print("COMPUTER FILM: physical desktop, mouse, typed search, archive, note, exit; %.2f seconds" % elapsed)
	game.close_game()
