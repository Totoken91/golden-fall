class_name RoomFilm
extends Node

var game: Node
var elapsed := 0.0
var recording := false
var poses := [
	[0.0,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)],
	[2.5,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)],
	[6.0,Vector3(-.28,-.015,-.40),Vector3(-.80,1.38,-2.83)],
	[8.5,Vector3(-.28,-.015,-.40),Vector3(-.80,1.38,-2.83)],
	[11.5,Vector3(.42,-.015,-.15),Vector3(1.75,.68,-.65)],
	[13.0,Vector3(.42,-.015,-.15),Vector3(1.75,.68,-.65)],
	[15.0,Vector3(-.10,-.015,.10),Vector3(-.87,.93,-1.03)],
	[16.5,Vector3(-.10,-.015,.10),Vector3(-.87,.93,-1.03)],
	[20.0,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)],
	[21.0,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)]
]

func _init(controller: Node) -> void: game = controller

func _ready() -> void:
	game.set_modal(true)
	game.ui.root.hide()
	game.walker.set_physics_process(false)
	game.weather.frozen = false
	game.weather.set_time(2.0)
	recording = true

func _process(delta: float) -> void:
	if not recording: return
	elapsed += delta
	for i in range(poses.size()-1):
		var a: Array = poses[i]
		var b: Array = poses[i+1]
		if elapsed >= a[0] and elapsed < b[0]:
			var t := smoothstep(0.0,1.0,(elapsed-float(a[0]))/(float(b[0])-float(a[0])))
			game.walker.position = (a[1] as Vector3).lerp(b[1],t)
			game.walker.aim((a[2] as Vector3).lerp(b[2],t))
			return
	if elapsed >= 21.0:
		recording = false
		print("ROOM FILM: 21 seconds, scripted camera through the live 3D scene")
		game.close_game()
