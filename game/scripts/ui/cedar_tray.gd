class_name CedarTray
extends Control

# Notification-area glyphs: speaker and dial-up connection.
func _draw() -> void:
	var ink := Color("dfe9e4")
	# Speaker.
	draw_colored_polygon(PackedVector2Array([Vector2(0,6),Vector2(4,6),Vector2(9,2),Vector2(9,16),Vector2(4,12),Vector2(0,12)]),ink)
	draw_arc(Vector2(9,9),5,-0.9,0.9,8,ink,1.0)
	# Dial-up connection: two small monitors.
	for offset in [Vector2(17,1),Vector2(23,7)]:
		draw_rect(Rect2(offset,Vector2(9,7)),Color("9fd0d6"))
		draw_rect(Rect2(offset,Vector2(9,7)),Color("0d2226"),false,1.0)
		draw_rect(Rect2(offset+Vector2(3,7),Vector2(3,2)),ink)
