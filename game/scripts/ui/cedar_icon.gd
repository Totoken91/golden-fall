class_name CedarIcon
extends Control

# Cedar 03 application icons drawn in code (no image files), 38x38 at scale 1.
var kind := "browser"
var day := "13"
func vgrad(rect: Rect2, top: Color, bottom: Color) -> void:
	draw_polygon(PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)]),PackedColorArray([top,top,bottom,bottom]))
func shadow(rect: Rect2) -> void:
	draw_rect(Rect2(rect.position+Vector2(2,3),rect.size),Color(0,0,0,.30))
func _draw() -> void:
	var ink := Color("1a2a2c")
	match kind:
		"browser":
			draw_circle(Vector2(20,20),15,Color(0,0,0,.28))
			draw_circle(Vector2(18,17),15,Color("1f5f8a"))
			draw_circle(Vector2(18,17),13,Color("3d8fbf"))
			draw_circle(Vector2(15,13),8,Color("74b8dc"))
			# Continents in moss green.
			draw_colored_polygon(PackedVector2Array([Vector2(9,9),Vector2(17,7),Vector2(19,13),Vector2(14,17),Vector2(15,24),Vector2(10,21),Vector2(7,14)]),Color("5d8a3c"))
			draw_colored_polygon(PackedVector2Array([Vector2(22,15),Vector2(29,13),Vector2(30,21),Vector2(24,27),Vector2(21,21)]),Color("4f7a32"))
			draw_circle(Vector2(13,10),3.5,Color(1,1,1,.55))
			draw_arc(Vector2(18,17),15,0,TAU,32,Color("16405c"),1.5)
			# Amber orbit swoosh: CedarSearch's own mark.
			draw_arc(Vector2(18,18),19,deg_to_rad(200),deg_to_rad(330),18,Color("e39a3b"),3.0)
			draw_arc(Vector2(18,18),19,deg_to_rad(20),deg_to_rad(80),10,Color("e39a3b"),3.0)
		"agenda":
			shadow(Rect2(4,5,30,29))
			vgrad(Rect2(4,5,30,29),Color("fffdf4"),Color("e3dcc6"))
			vgrad(Rect2(4,5,30,9),Color("d9643a"),Color("9e3a1d"))
			draw_rect(Rect2(4,5,30,29),ink,false,1.0)
			for x in [11,27]:
				draw_rect(Rect2(x-1,2,3,7),Color("c9cdc6"))
				draw_rect(Rect2(x-1,2,3,7),ink,false,1.0)
			var font := ThemeDB.fallback_font
			draw_string(font,Vector2(4,30),day,HORIZONTAL_ALIGNMENT_CENTER,30,15,Color("2b2b28"))
		"save":
			shadow(Rect2(5,3,28,30))
			vgrad(Rect2(5,3,28,30),Color("3f6f86"),Color("1d3c4f"))
			draw_rect(Rect2(5,3,28,30),ink,false,1.0)
			vgrad(Rect2(11,4,16,10),Color("e8ecef"),Color("a7b0b6"))
			draw_rect(Rect2(21,6,3,6),Color("3c474d"))
			draw_rect(Rect2(10,18,18,14),Color("f7f3e4"))
			for y in [22,25,28]: draw_line(Vector2(12,y),Vector2(26,y),Color("b9b29b"),1.0)
			draw_rect(Rect2(10,18,18,14),ink,false,1.0)
		"notes":
			shadow(Rect2(7,3,25,30))
			vgrad(Rect2(7,3,25,30),Color("8c5a36"),Color("5a3620"))
			draw_rect(Rect2(7,3,25,30),ink,false,1.0)
			vgrad(Rect2(12,9,16,9),Color("f4ecd2"),Color("dcd0ad"))
			draw_rect(Rect2(12,9,16,9),Color("3a2414"),false,1.0)
			for y in range(5,32,4):
				draw_circle(Vector2(7,y),1.6,Color("cfd3cf"))
			draw_line(Vector2(28,3),Vector2(28,33),Color("c8402c"),2.0)
		"files":
			shadow(Rect2(3,10,31,22))
			vgrad(Rect2(4,7,14,6),Color("e9c46b"),Color("c99b3e"))
			draw_rect(Rect2(7,10,24,6),Color("fbfaf2"))
			vgrad(Rect2(3,12,31,20),Color("f3cf72"),Color("c8912e"))
			draw_line(Vector2(4,13),Vector2(33,13),Color(1,1,1,.55),1.0)
			draw_rect(Rect2(3,12,31,20),Color("7a5418"),false,1.0)
		"trash":
			shadow(Rect2(9,7,20,25))
			vgrad(Rect2(9,7,20,25),Color("d8ddd8"),Color("8f9a96"))
			for x in [13,17,21,25]: draw_line(Vector2(x,10),Vector2(x,29),Color("6c7773"),1.0)
			draw_rect(Rect2(9,7,20,25),ink,false,1.0)
			vgrad(Rect2(6,4,26,4),Color("eef1ee"),Color("9aa4a0"))
			draw_rect(Rect2(6,4,26,4),ink,false,1.0)
		"messages":
			# Two speech bubbles: the 2003 instant-messenger shorthand.
			draw_circle(Vector2(15,15),11,Color(0,0,0,.25))
			draw_circle(Vector2(14,13),11,Color("f2c45a"))
			draw_arc(Vector2(14,13),11,0,TAU,24,ink,1.0)
			draw_colored_polygon(PackedVector2Array([Vector2(8,21),Vector2(5,28),Vector2(13,23)]),Color("f2c45a"))
			draw_circle(Vector2(24,22),9,Color("5fa8c9"))
			draw_arc(Vector2(24,22),9,0,TAU,24,ink,1.0)
			draw_colored_polygon(PackedVector2Array([Vector2(28,28),Vector2(33,34),Vector2(23,30)]),Color("5fa8c9"))
			for x in [10.0,14.0,18.0]: draw_circle(Vector2(x,13),1.3,ink)
		"cedar":
			draw_colored_polygon(PackedVector2Array([Vector2(8,1),Vector2(14,10),Vector2(11,10),Vector2(16,17),Vector2(0,17),Vector2(5,10),Vector2(2,10)]),Color("f8f1dc"))
			draw_rect(Rect2(7,17,2,3),Color("f8f1dc"))
		"user":
			vgrad(Rect2(0,0,24,24),Color("e6b35d"),Color("8e4f22"))
			draw_colored_polygon(PackedVector2Array([Vector2(12,3),Vector2(19,13),Vector2(15,13),Vector2(21,21),Vector2(3,21),Vector2(9,13),Vector2(5,13)]),Color("2d4a36"))
			draw_rect(Rect2(0,0,24,24),Color("fbf6e6"),false,2.0)
