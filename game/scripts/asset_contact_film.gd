class_name AssetContactFilm
extends Node
var game: Node
var elapsed := 0.0
var poses := [
	[0.0,Vector3(-1.68,1.605,2.30),Vector3(-.05,.905,-1.45),62.0],
	[2.0,Vector3(-1.68,1.605,2.30),Vector3(-.05,.905,-1.45),62.0],
	[4.5,Vector3(-1.50,1.30,-1.76),Vector3(-1.6,.95,-2.22),48.0],
	[7.0,Vector3(-1.95,1.18,-1.76),Vector3(-1.6,.95,-2.22),48.0],
	[8.0,Vector3(-.70,1.55,-1.40),Vector3(-.65,1.16,-2.20),54.0],
	[9.0,Vector3(-.07,1.40,-1.90),Vector3(-.65,1.16,-2.20),46.0],
	[11.0,Vector3(.03,1.35,-1.98),Vector3(-.65,1.16,-2.20),46.0],
	[13.0,Vector3(.18,1.35,-1.75),Vector3(.78,.84,-2.43),54.0],
	[15.0,Vector3(.35,1.15,-1.75),Vector3(.78,.74,-2.43),54.0],
	[17.0,Vector3(.02,1.60,-1.70),Vector3(.41,1.50,-2.50),55.0],
	[19.0,Vector3(.60,2.38,-.75),Vector3(1.65,.63,-2.40),62.0],
	[21.0,Vector3(-.85,1.65,-1.55),Vector3(-.80,2.10,-8),62.0],
	[24.0,Vector3(-.85,1.65,-1.55),Vector3(-.80,2.10,-8),62.0]
]
func _init(controller: Node) -> void:game=controller
func _ready() -> void:
	game.set_modal(true);game.ui.root.hide()
	game.walker.set_physics_process(false)
	game.weather.frozen=false;game.weather.set_time(2.0)
func _process(delta: float) -> void:
	elapsed+=delta
	for i in range(poses.size()-1):
		var a: Array=poses[i];var b: Array=poses[i+1]
		if elapsed>=a[0] and elapsed<b[0]:
			var t:=smoothstep(0.0,1.0,(elapsed-float(a[0]))/(float(b[0])-float(a[0])))
			game.walker.position=(a[1] as Vector3).lerp(b[1],t)-Vector3(0,1.62,0)
			game.walker.camera.fov=lerpf(a[3],b[3],t)
			game.walker.aim((a[2] as Vector3).lerp(b[2],t))
			return
	if elapsed>=24:
		set_process(false)
		print("CONTACT FILM: 24 seconds, live Godot inspection of supports, ventilation, curtain, layout and rain")
		game.close_game()
