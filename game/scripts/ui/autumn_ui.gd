class_name AutumnUI
extends CanvasLayer

# Native overlay outside the PC: interaction prompt, notices and modal paper panels.
# Agenda, journal, search and saving live on the physical PC (CedarDesktop) since V0.19.
var game: Node
var root: Control
var modal: Control
var content: VBoxContainer
var prompt: Label
var notice: Label
var paper := Color("e8d9bd")
var ink := Color("302c26")
var notice_timer: Timer

func _init(controller: Node) -> void:
	game = controller

func _ready() -> void:
	root = Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var theme := Theme.new()
	theme.default_font_size = 19
	root.theme = theme
	add_child(root)
	prompt = label("",18,paper)
	prompt.position = Vector2(34,648)
	prompt.size = Vector2(1210,40)
	root.add_child(prompt)
	notice = label("",18,paper)
	notice.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	notice.position = Vector2(550,601)
	notice.size = Vector2(690,40)
	root.add_child(notice)
	for shaded in [prompt,notice]:
		shaded.add_theme_color_override("font_shadow_color",Color(0,0,0,.9))
		shaded.add_theme_constant_override("shadow_offset_x",1)
		shaded.add_theme_constant_override("shadow_offset_y",1)
	notice_timer = Timer.new()
	notice_timer.one_shot = true
	notice_timer.wait_time = 4.0
	notice_timer.timeout.connect(func(): notice.text = "")
	add_child(notice_timer)

func label(text: String, font_size := 20, color := Color("302c26")) -> Label:
	var result := Label.new()
	result.text = text
	result.add_theme_font_size_override("font_size",font_size)
	result.add_theme_color_override("font_color",color)
	return result

func serif_label(text: String, font_size := 38, color := Color("302c26")) -> Label:
	var result := label(text,font_size,color)
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Georgia","DejaVu Serif"])
	result.add_theme_font_override("font",font)
	return result

func style(color: Color, border: Color, margin := 12) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = color
	s.border_color = border
	s.set_border_width_all(1)
	s.content_margin_left = margin
	s.content_margin_right = margin
	s.content_margin_top = margin/2.0
	s.content_margin_bottom = margin/2.0
	return s

func button(text: String, action: Callable) -> Button:
	var b := Button.new()
	b.text = text
	b.custom_minimum_size.y = 42
	for state_name in ["font_color","font_hover_color","font_focus_color"]: b.add_theme_color_override(state_name,ink)
	b.add_theme_stylebox_override("normal",style(Color("dfcfaf"),Color("a18d6c")))
	b.add_theme_stylebox_override("hover",style(Color("f2e5cd"),Color("b58a50")))
	b.add_theme_stylebox_override("pressed",style(Color("c6b491"),Color("8b7049")))
	b.add_theme_stylebox_override("focus",style(Color(0,0,0,0),Color("bb9257"),2))
	b.pressed.connect(action)
	return b

func paragraph(text: String, color := Color("302c26"), font_size := 20) -> Label:
	var p := label(text,font_size,color)
	p.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	p.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	return p

func close() -> void:
	if modal != null:
		root.remove_child(modal)
		modal.queue_free()
		modal = null
	game.set_modal(false)

func panel(title: String, rect := Rect2(270,118,740,500)) -> VBoxContainer:
	close()
	game.set_modal(true)
	modal = Control.new()
	modal.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	modal.mouse_filter = Control.MOUSE_FILTER_STOP
	root.add_child(modal)
	var shade := ColorRect.new()
	shade.color = Color(0.05,0.07,0.06,0.38)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	modal.add_child(shade)
	var card := PanelContainer.new()
	card.position = rect.position
	card.size = rect.size
	card.add_theme_stylebox_override("panel",style(paper,Color("9a8260"),26))
	modal.add_child(card)
	content = VBoxContainer.new()
	content.add_theme_constant_override("separation",12)
	card.add_child(content)
	if not title.is_empty(): content.add_child(serif_label(title,34))
	return content

func toast(text: String) -> void:
	notice.text = text
	notice_timer.start()
