class_name CedarPointer
extends Control

# Cedar 03 mouse pointer drawn in code: arrow, pointing hand over links, text beam.
var kind := "arrow":
	set(value):
		if value != kind:
			kind = value
			queue_redraw()
func _draw() -> void:
	var ink := Color("101614")
	var paper := Color("fbfaf3")
	match kind:
		"hand":
			for part in [Rect2(5,0,5,11),Rect2(2,9,14,9),Rect2(4,17,10,5)]:
				draw_rect(part,paper)
			for part in [Rect2(5,0,5,11),Rect2(2,9,14,9),Rect2(4,17,10,5)]:
				draw_rect(part,ink,false,1.0)
			draw_rect(Rect2(5.5,8.5,4,2),paper)
			draw_rect(Rect2(3,17,12,1),paper)
			for x in [9.5,12.5]: draw_line(Vector2(x,10),Vector2(x,13),ink,1.0)
		"beam":
			draw_line(Vector2(4,1),Vector2(4,19),ink,2.0)
			for y in [1.0,19.0]: draw_line(Vector2(1,y),Vector2(7,y),ink,2.0)
			draw_line(Vector2(4,2),Vector2(4,18),paper,1.0)
		_:
			var points := PackedVector2Array([Vector2(0,0),Vector2(0,19),Vector2(5,14),Vector2(9,23),Vector2(13,21),Vector2(9,13),Vector2(16,13),Vector2(0,0)])
			draw_colored_polygon(PackedVector2Array([Vector2(2,2),Vector2(2,21),Vector2(7,16),Vector2(11,25),Vector2(15,23),Vector2(11,15),Vector2(18,15)]),Color(0,0,0,.28))
			draw_colored_polygon(points,paper)
			draw_polyline(points,ink,1.0)
