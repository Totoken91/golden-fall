class_name ExteriorFilm
extends Node

var game: Node
var elapsed := 0.0
var poses := [
	[0.0,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)],
	[2.0,Vector3(-1.68,-.015,2.30),Vector3(-.05,.905,-1.45)],
	[5.0,Vector3(-1.32,.03,-1.45),Vector3(-.8,2.10,-12.0)],
	[8.0,Vector3(-1.32,.03,-1.45),Vector3(-.8,2.10,-12.0)],
	[11.0,Vector3(-.40,.03,-1.52),Vector3(-.8,2.10,-12.0)],
	[14.0,Vector3(-.40,.03,-1.52),Vector3(-.8,2.10,-12.0)],
	[16.0,Vector3(-.85,.03,-1.55),Vector3(-.8,2.10,-12.0)]
]

func _init(controller: Node) -> void:game = controller

func _ready() -> void:
	game.set_modal(true)
	game.ui.root.hide()
	game.walker.set_physics_process(false)
	game.weather.frozen = false
	game.weather.set_time(2.0)

func _process(delta: float) -> void:
	elapsed += delta
	for i in range(poses.size()-1):
		var a: Array = poses[i]
		var b: Array = poses[i+1]
		if elapsed >= a[0] and elapsed < b[0]:
			var t := smoothstep(0.0,1.0,(elapsed-float(a[0]))/(float(b[0])-float(a[0])))
			game.walker.position = (a[1] as Vector3).lerp(b[1],t)
			game.walker.aim((a[2] as Vector3).lerp(b[2],t))
			return
	if elapsed >= 16.0:
		set_process(false)
		print("EXTERIOR FILM: live forest parallax, rain, glass, wet ground and user audio; 16 seconds")
		game.close_game()
