class_name CedarDesktop
extends Control

signal leave_requested
signal chime

# Cedar 03 — original mid-2000s look: glossy taskbar, framed windows with drop shadows,
# painted wallpaper, tray clock and balloons. Geometry of icons, taskbar, start menu and
# windows is unchanged from V0.19 because QA drives them with physical coordinates.
const DISPLAY := Vector2(640,480)
const GLOSS := preload("res://shaders/cedar_gloss.gdshader")
const WALLPAPER := preload("res://shaders/cedar_wallpaper.gdshader")
const INK := Color("24302c")
const MUTED := Color("6b726a")
const LINK := Color("1d4f9e")
const FRAME := Color("27565d")
const FRAME_IDLE := Color("7f8b86")
const TITLE_TOP := Color("4f8f95")
const TITLE_BOTTOM := Color("163b42")
const IDLE_TOP := Color("a7b1ab")
const IDLE_BOTTOM := Color("6f7c77")
const APP_NAMES := {"agenda":"Calendar","notes":"Journal","messages":"Messages","save":"Save","browser":"Morrow Search","files":"My Documents","trash":"Recycle Bin"}

var game: Node
var windows: Dictionary = {}
var task_buttons: HBoxContainer
var start_menu: Panel
var pointer: Control
var dragging: Panel
var drag_offset := Vector2.ZERO
var browser_input: LineEdit
var browser_body: VBoxContainer
var browser_page := ""
var browser_query := ""
var browser_history: Array[Dictionary] = []
var last_note_succeeded := false
var date_caption: Label
var weekday_caption: Label
var clock_caption: Label
var focused_id := ""
var start_gloss: ColorRect
var balloon: Panel
var ui_font: SystemFont
var bold_font: SystemFont
var title_font: SystemFont
var serif_font: SystemFont

func _init(controller: Node) -> void:
	game = controller

func _ready() -> void:
	size = DISPLAY
	mouse_filter = Control.MOUSE_FILTER_STOP
	ui_font = system_font(["Tahoma","Verdana","Segoe UI","DejaVu Sans"])
	bold_font = system_font(["Tahoma","Verdana","Segoe UI","DejaVu Sans"],700)
	title_font = system_font(["Trebuchet MS","Tahoma","DejaVu Sans"],700)
	serif_font = system_font(["Georgia","Times New Roman","DejaVu Serif"],700)
	theme = build_theme()
	var wallpaper := ColorRect.new()
	wallpaper.name = "Wallpaper"
	wallpaper.size = Vector2(640,448)
	var paint := ShaderMaterial.new()
	paint.shader = WALLPAPER
	paint.set_shader_parameter("rect_size",wallpaper.size)
	wallpaper.material = paint
	wallpaper.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(wallpaper)
	var brand := shadowed_label("cedar",34,Color("fbf1da"),title_font)
	brand.position = Vector2(470,352)
	add_child(brand)
	var brand_version := shadowed_label("03",34,Color("f0a64c"),title_font)
	brand_version.position = Vector2(566,352)
	add_child(brand_version)
	weekday_caption = shadowed_label("",12,Color("f0a64c"),bold_font)
	weekday_caption.position = Vector2(472,413)
	add_child(weekday_caption)
	date_caption = shadowed_label("OCTOBER 15, 2003",12,Color("f1e6cc"),bold_font)
	date_caption.position = Vector2(472,396)
	add_child(date_caption)
	var entries: Array = []
	for id in ["agenda","notes","messages","save","browser","files","trash"]: entries.append([id,APP_NAMES[id]])
	for index in entries.size():
		var entry: Array = entries[index]
		var icon := Button.new()
		icon.name = "Icon_"+entry[0]
		icon.position = Vector2(12+floori(index/4.0)*104,12+(index%4)*91)
		icon.size = Vector2(100,80)
		icon.add_theme_stylebox_override("normal",StyleBoxEmpty.new())
		icon.add_theme_stylebox_override("hover",rounded(Color(.78,.9,.92,.22),Color(.9,.97,1,.55),5))
		icon.add_theme_stylebox_override("pressed",rounded(Color(.95,.66,.3,.35),Color(1,.85,.6,.7),5))
		icon.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
		icon.pressed.connect(open_app.bind(str(entry[0])))
		add_child(icon)
		var image := app_icon(entry[0])
		image.position = Vector2(31,4)
		icon.add_child(image)
		var caption := shadowed_label(entry[1],14,Color("ffffff"))
		caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		caption.position = Vector2(0,46)
		caption.size = Vector2(100,22)
		icon.add_child(caption)
	build_taskbar()
	build_start_menu()
	pointer = CedarPointer.new()
	pointer.name = "ScreenPointer"
	pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	pointer.z_index = 4095
	pointer.hide()
	add_child(pointer)

func system_font(names: Array, weight := 400) -> SystemFont:
	var font := SystemFont.new()
	font.font_names = PackedStringArray(names)
	font.font_weight = weight
	font.hinting = TextServer.HINTING_LIGHT
	return font

func build_theme() -> Theme:
	var result := Theme.new()
	result.default_font = ui_font
	result.default_font_size = 15
	result.set_color("font_color","Label",INK)
	var track := rounded(Color("e7e2d3"),Color("c9c2ad"),0)
	var grab := rounded(Color("a9c2bf"),Color("587a78"),3)
	var grab_hover := rounded(Color("bfd6d2"),Color("3f6663"),3)
	for kind in ["VScrollBar","HScrollBar"]:
		result.set_stylebox("scroll",kind,track)
		result.set_stylebox("scroll_focus",kind,track)
		result.set_stylebox("grabber",kind,grab)
		result.set_stylebox("grabber_highlight",kind,grab_hover)
		result.set_stylebox("grabber_pressed",kind,grab_hover)
	return result

func rounded(color: Color, border := Color("79867c"), radius := 3, width := 1) -> StyleBoxFlat:
	var result := StyleBoxFlat.new()
	result.bg_color = color
	result.border_color = border
	result.set_border_width_all(width)
	result.set_corner_radius_all(radius)
	result.content_margin_left = 6
	result.content_margin_right = 6
	result.content_margin_top = 2
	result.content_margin_bottom = 2
	return result

func box(color: Color, border := Color("79867c")) -> StyleBoxFlat:
	return rounded(color,border,3)

func gloss(rect: Rect2, top: Color, bottom: Color, radius := 6.0, round_bottom := false, border := Color("0e2a2f"), shine := 1.0) -> ColorRect:
	var surface := ColorRect.new()
	surface.position = rect.position
	surface.size = rect.size
	surface.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var material_gloss := ShaderMaterial.new()
	material_gloss.shader = GLOSS
	material_gloss.set_shader_parameter("rect_size",rect.size)
	material_gloss.set_shader_parameter("radius",radius)
	material_gloss.set_shader_parameter("round_bottom",round_bottom)
	material_gloss.set_shader_parameter("gloss",shine)
	surface.material = material_gloss
	paint_gloss(surface,top,bottom,border)
	return surface

func paint_gloss(surface: ColorRect, top: Color, bottom: Color, border: Color) -> void:
	var material_gloss := surface.material as ShaderMaterial
	material_gloss.set_shader_parameter("top_color",top)
	material_gloss.set_shader_parameter("bottom_color",bottom)
	material_gloss.set_shader_parameter("border_color",border)

func app_icon(kind: String, scale_factor := 1.0) -> CedarIcon:
	var image := CedarIcon.new()
	image.kind = kind
	image.size = Vector2(38,38)
	image.scale = Vector2.ONE*scale_factor
	image.day = str(Calendar.day_number(game.state.date()))
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return image

func text_label(value: String, font_size := 15, color := INK, font: Font = null) -> Label:
	var result := Label.new()
	result.text = value
	result.add_theme_font_size_override("font_size",font_size)
	result.add_theme_color_override("font_color",color)
	if font != null: result.add_theme_font_override("font",font)
	result.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return result

func shadowed_label(value: String, font_size := 15, color := Color.WHITE, font: Font = null) -> Label:
	var result := text_label(value,font_size,color,font)
	result.add_theme_color_override("font_shadow_color",Color(0,0,0,.75))
	result.add_theme_constant_override("shadow_offset_x",1)
	result.add_theme_constant_override("shadow_offset_y",1)
	return result

func button(value: String, action: Callable) -> Button:
	var result := Button.new()
	result.text = value
	result.custom_minimum_size.y = 28
	result.add_theme_color_override("font_color",INK)
	result.add_theme_color_override("font_hover_color",INK)
	result.add_theme_color_override("font_pressed_color",INK)
	result.add_theme_color_override("font_disabled_color",Color("9a9d93"))
	var normal := rounded(Color("f8f4e7"),Color("6f7f78"),4)
	normal.shadow_color = Color(0,0,0,.12)
	normal.shadow_offset = Vector2(0,1)
	normal.shadow_size = 1
	var hover := rounded(Color("fffaeb"),Color("d98a2b"),4)
	hover.shadow_color = Color(.95,.6,.2,.45)
	hover.shadow_size = 2
	result.add_theme_stylebox_override("normal",normal)
	result.add_theme_stylebox_override("hover",hover)
	result.add_theme_stylebox_override("pressed",rounded(Color("e2dbc6"),Color("54645e"),4))
	result.add_theme_stylebox_override("disabled",rounded(Color("ebe7da"),Color("b6b8ad"),4))
	result.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
	result.pressed.connect(action)
	return result

func primary_button(value: String, action: Callable) -> Button:
	var result := button(value,action)
	result.add_theme_font_override("font",bold_font)
	for state_name in ["font_color","font_hover_color","font_pressed_color"]:
		result.add_theme_color_override(state_name,Color("fffaf0"))
	var normal := rounded(Color("cf7d2c"),Color("7d3f12"),5)
	normal.shadow_color = Color(0,0,0,.18)
	normal.shadow_offset = Vector2(0,1)
	normal.shadow_size = 1
	var hover := rounded(Color("e3923c"),Color("7d3f12"),5)
	hover.shadow_color = Color(.95,.6,.2,.5)
	hover.shadow_size = 2
	result.add_theme_stylebox_override("normal",normal)
	result.add_theme_stylebox_override("hover",hover)
	result.add_theme_stylebox_override("pressed",rounded(Color("a95d1c"),Color("5d2c0a"),5))
	return result

func link(value: String, action: Callable, font_size := 15) -> Button:
	var result := Button.new()
	result.text = value
	result.flat = true
	result.alignment = HORIZONTAL_ALIGNMENT_LEFT
	result.set_meta("hand",true)
	result.add_theme_font_size_override("font_size",font_size)
	result.add_theme_color_override("font_color",LINK)
	result.add_theme_color_override("font_hover_color",Color("c4561d"))
	result.add_theme_color_override("font_pressed_color",Color("6b3a8c"))
	result.add_theme_color_override("font_disabled_color",Color("8a8f86"))
	for state_name in ["normal","hover","pressed","focus","disabled"]:
		var style := StyleBoxEmpty.new()
		style.content_margin_left = 0
		style.content_margin_top = 1
		style.content_margin_bottom = 1
		result.add_theme_stylebox_override(state_name,style)
	result.pressed.connect(action)
	return result

func build_taskbar() -> void:
	var bar := Panel.new()
	bar.position = Vector2(0,448)
	bar.size = Vector2(640,32)
	bar.z_index = 2000
	bar.add_theme_stylebox_override("panel",StyleBoxEmpty.new())
	add_child(bar)
	bar.add_child(gloss(Rect2(0,0,640,32),Color("3a7279"),Color("10292e"),0.0,false,Color("0a1d21"),.9))
	start_gloss = gloss(Rect2(0,1,106,30),Color("e9a44e"),Color("9b4f17"),12.0,true,Color("5a2a0a"))
	bar.add_child(start_gloss)
	var start := Button.new()
	start.name = "StartButton"
	start.text = "start"
	start.position = Vector2(3,2)
	start.size = Vector2(100,28)
	start.alignment = HORIZONTAL_ALIGNMENT_LEFT
	var empty := StyleBoxEmpty.new()
	empty.content_margin_left = 25
	for state_name in ["normal","hover","pressed","focus"]: start.add_theme_stylebox_override(state_name,empty)
	start.add_theme_font_override("font",system_font(["Trebuchet MS","Tahoma","DejaVu Sans"],700))
	start.add_theme_font_size_override("font_size",16)
	for state_name in ["font_color","font_hover_color","font_pressed_color"]: start.add_theme_color_override(state_name,Color("fffaf0"))
	start.add_theme_color_override("font_outline_color",Color(.35,.15,.02,.8))
	start.add_theme_constant_override("outline_size",2)
	start.mouse_entered.connect(func(): paint_gloss(start_gloss,Color("f6b862"),Color("b15d1d"),Color("5a2a0a")))
	start.mouse_exited.connect(func(): paint_gloss(start_gloss,Color("e9a44e"),Color("9b4f17"),Color("5a2a0a")))
	# z_index orders drawing only; the menu must also be last in the tree to receive clicks first.
	start.pressed.connect(func():
		start_menu.visible = not start_menu.visible
		if start_menu.visible: start_menu.move_to_front())
	bar.add_child(start)
	var mark := app_icon("cedar")
	mark.position = Vector2(8,6)
	start.add_child(mark)
	task_buttons = HBoxContainer.new()
	task_buttons.position = Vector2(110,2)
	task_buttons.size = Vector2(434,28)
	task_buttons.add_theme_constant_override("separation",3)
	bar.add_child(task_buttons)
	var tray := Panel.new()
	tray.position = Vector2(548,1)
	tray.size = Vector2(92,30)
	var tray_style := StyleBoxFlat.new()
	tray_style.bg_color = Color("123a42")
	tray_style.border_color = Color("0a2227")
	tray_style.border_width_left = 1
	tray_style.shadow_color = Color(1,1,1,.12)
	tray.add_theme_stylebox_override("panel",tray_style)
	tray.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bar.add_child(tray)
	var icons := CedarTray.new()
	icons.position = Vector2(6,7)
	icons.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tray.add_child(icons)
	clock_caption = shadowed_label("4:10 PM",13,Color("f4f1e6"))
	clock_caption.position = Vector2(38,6)
	tray.add_child(clock_caption)

func build_start_menu() -> void:
	start_menu = Panel.new()
	var items: Array = []
	for id in ["agenda","notes","messages","save","browser","files"]: items.append([APP_NAMES[id],id])
	var height: int = 80+items.size()*36
	start_menu.position = Vector2(3,448-height)
	start_menu.size = Vector2(254,height)
	start_menu.z_index = 2500
	var frame := rounded(Color("fbf8ee"),FRAME,8,2)
	frame.corner_radius_bottom_left = 0
	frame.corner_radius_bottom_right = 0
	frame.shadow_color = Color(0,0,0,.45)
	frame.shadow_size = 6
	frame.shadow_offset = Vector2(3,2)
	start_menu.add_theme_stylebox_override("panel",frame)
	add_child(start_menu)
	start_menu.add_child(gloss(Rect2(0,0,254,33),TITLE_TOP,TITLE_BOTTOM,8.0,false,FRAME))
	var avatar := app_icon("user")
	avatar.position = Vector2(7,4)
	start_menu.add_child(avatar)
	var title := shadowed_label("My Computer",16,Color("ffffff"),title_font)
	title.position = Vector2(40,6)
	start_menu.add_child(title)
	var footer_y: float = height-46
	start_menu.add_child(gloss(Rect2(0,footer_y,254,height-footer_y),TITLE_TOP,TITLE_BOTTOM,0.0,false,FRAME,.6))
	for index in items.size():
		var item: Array = items[index]
		var launch := menu_entry(item[0],str(item[1]))
		launch.name = "Start_"+str(item[1])
		launch.position = Vector2(10,36+index*36)
		launch.size = Vector2(234,32)
		start_menu.add_child(launch)
	var leave := Button.new()
	leave.name = "LeaveComputer"
	leave.text = "Leave computer"
	leave.position = Vector2(10,height-40)
	leave.size = Vector2(234,30)
	leave.alignment = HORIZONTAL_ALIGNMENT_RIGHT
	var leave_normal := StyleBoxEmpty.new()
	leave_normal.content_margin_right = 8
	leave.add_theme_stylebox_override("normal",leave_normal)
	leave.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
	var leave_hover := rounded(Color(1,1,1,.14),Color(1,1,1,.35),4)
	leave_hover.content_margin_right = 8
	leave.add_theme_stylebox_override("hover",leave_hover)
	leave.add_theme_stylebox_override("pressed",leave_hover)
	for state_name in ["font_color","font_hover_color","font_pressed_color"]: leave.add_theme_color_override(state_name,Color("ffffff"))
	leave.pressed.connect(func(): leave_requested.emit())
	start_menu.add_child(leave)
	var power := gloss(Rect2(80,5,20,20),Color("ef8a52"),Color("a23b17"),10.0,true,Color("5b1d08"))
	leave.add_child(power)
	var glyph := text_label("⏻",13,Color("fff4ea"))
	glyph.position = Vector2(4,0)
	power.add_child(glyph)
	start_menu.hide()

func menu_entry(value: String, kind: String) -> Button:
	var entry := Button.new()
	entry.text = value
	entry.alignment = HORIZONTAL_ALIGNMENT_LEFT
	var normal := StyleBoxEmpty.new()
	normal.content_margin_left = 34
	var hover := rounded(Color("2f6b74"),Color("1d4950"),3)
	hover.content_margin_left = 34
	entry.add_theme_stylebox_override("normal",normal)
	entry.add_theme_stylebox_override("hover",hover)
	entry.add_theme_stylebox_override("pressed",hover)
	entry.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
	entry.add_theme_font_override("font",bold_font)
	entry.add_theme_color_override("font_color",INK)
	entry.add_theme_color_override("font_hover_color",Color("ffffff"))
	entry.add_theme_color_override("font_pressed_color",Color("ffffff"))
	entry.pressed.connect(open_app.bind(kind))
	var image := app_icon(kind,.62)
	image.position = Vector2(4,3)
	entry.add_child(image)
	return entry

func open_app(id: String) -> void:
	start_menu.hide()
	match id:
		"agenda": open_agenda()
		"messages": open_messages()
		"save": open_save()
		"browser": open_browser()
		"notes": open_notes()
		"files":
			var col := window_content("files","My Documents",Rect2(160,94,420,268))
			col.add_child(text_label("My Documents",20,Color("1f4c52"),title_font))
			col.add_child(file_row("notes","notes.txt","Text Document · 4 KB",open_notes))
			col.add_child(file_row("browser","Favorites","Morrow Search shortcuts",open_browser))
		"trash":
			var col := window_content("trash","Recycle Bin",Rect2(195,134,340,150))
			col.add_child(text_label("The Recycle Bin is empty.",15,MUTED))

func file_row(kind: String, value: String, detail: String, action: Callable) -> Control:
	var row := HBoxContainer.new()
	var holder := Control.new()
	holder.custom_minimum_size = Vector2(30,30)
	holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	holder.add_child(app_icon(kind,.75))
	row.add_child(holder)
	var info := VBoxContainer.new()
	info.add_theme_constant_override("separation",0)
	info.add_child(link(value,action))
	info.add_child(text_label(detail,12,MUTED))
	row.add_child(info)
	return row

func window_content(id: String, title: String, rect: Rect2) -> VBoxContainer:
	refresh_metadata()
	if not windows.has(id):
		var window := Panel.new()
		window.name = "Window_"+id
		window.position = rect.position
		window.size = rect.size
		var frame := rounded(Color("f4efe1"),FRAME,8,3)
		frame.corner_radius_bottom_left = 3
		frame.corner_radius_bottom_right = 3
		frame.shadow_color = Color(0,0,0,.42)
		frame.shadow_size = 8
		frame.shadow_offset = Vector2(3,4)
		window.add_theme_stylebox_override("panel",frame)
		add_child(window)
		windows[id] = window
		window.gui_input.connect(func(event: InputEvent):
			if event is InputEventMouseButton and event.pressed:
				focus_window(id))
		var titlebar := gloss(Rect2(3,3,rect.size.x-6,28),TITLE_TOP,TITLE_BOTTOM,6.0,false,FRAME)
		titlebar.name = "Titlebar"
		titlebar.mouse_filter = Control.MOUSE_FILTER_STOP
		window.add_child(titlebar)
		titlebar.gui_input.connect(func(event: InputEvent):
			if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
				if event.pressed:
					focus_window(id)
					dragging = window
					drag_offset = get_viewport().get_mouse_position()-window.position
				else: dragging = null)
		var mini := app_icon(id,.5)
		mini.position = Vector2(6,4)
		titlebar.add_child(mini)
		var caption := shadowed_label(title,15,Color("ffffff"),title_font)
		caption.position = Vector2(28,4)
		caption.size.x = rect.size.x-100
		caption.clip_text = true
		titlebar.add_child(caption)
		var minimize := caption_button("_",Color("6aa2a8"),Color("2d6168"))
		minimize.name = "Minimize"
		minimize.position = Vector2(rect.size.x-62,5)
		minimize.pressed.connect(func(): window.hide(); refresh_tasks())
		window.add_child(minimize)
		var close_button := caption_button("×",Color("d8653a"),Color("8e2f12"))
		close_button.name = "Close"
		close_button.position = Vector2(rect.size.x-33,5)
		close_button.pressed.connect(close_window.bind(id))
		window.add_child(close_button)
		var body := VBoxContainer.new()
		body.name = "Body"
		body.position = Vector2(10,39)
		body.size = rect.size-Vector2(20,49)
		body.add_theme_constant_override("separation",7)
		window.add_child(body)
	var current: Panel = windows[id]
	current.show()
	focus_window(id)
	var content: VBoxContainer = current.get_node("Body")
	for child in content.get_children():
		content.remove_child(child)
		child.queue_free()
	refresh_tasks()
	return content

func caption_button(glyph: String, top: Color, border: Color) -> Button:
	var result := Button.new()
	result.text = glyph
	result.size = Vector2(24,22)
	result.custom_minimum_size = Vector2(24,22)
	var normal := rounded(top,border,4)
	normal.content_margin_top = 0
	normal.content_margin_bottom = 2
	var hover := rounded(top.lightened(.18),border,4)
	hover.content_margin_top = 0
	hover.content_margin_bottom = 2
	result.add_theme_stylebox_override("normal",normal)
	result.add_theme_stylebox_override("hover",hover)
	result.add_theme_stylebox_override("pressed",rounded(top.darkened(.2),border,4))
	result.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
	result.add_theme_font_override("font",bold_font)
	result.add_theme_font_size_override("font_size",15)
	for state_name in ["font_color","font_hover_color","font_pressed_color"]: result.add_theme_color_override(state_name,Color("ffffff"))
	return result

func focus_window(id: String) -> void:
	if not windows.has(id): return
	focused_id = id
	(windows[id] as Panel).move_to_front()
	for key in windows:
		var window: Panel = windows[key]
		var active: bool = key == id
		var frame := window.get_theme_stylebox("panel") as StyleBoxFlat
		frame.border_color = FRAME if active else FRAME_IDLE
		var titlebar := window.get_node("Titlebar") as ColorRect
		if active: paint_gloss(titlebar,TITLE_TOP,TITLE_BOTTOM,FRAME)
		else: paint_gloss(titlebar,IDLE_TOP,IDLE_BOTTOM,FRAME_IDLE)
	refresh_tasks()

func close_window(id: String) -> void:
	if not windows.has(id):return
	var window: Panel = windows[id]
	windows.erase(id)
	remove_child(window)
	window.queue_free()
	if focused_id == id:
		focused_id = ""
		for key in windows:
			if (windows[key] as Panel).visible: focused_id = key
		if focused_id != "": focus_window(focused_id)
	refresh_tasks()

func refresh_tasks() -> void:
	if task_buttons == null: return
	for child in task_buttons.get_children():
		task_buttons.remove_child(child)
		child.queue_free()
	for id in windows:
		var window: Panel = windows[id]
		var task := Button.new()
		task.name = "Task_"+str(id)
		task.text = APP_NAMES[id]
		task.custom_minimum_size = Vector2(72,28)
		task.clip_text = true
		task.alignment = HORIZONTAL_ALIGNMENT_LEFT
		task.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		task.add_theme_font_size_override("font_size",13)
		var active: bool = id == focused_id and window.visible
		var normal := rounded(Color("1d4d55") if active else Color("3d7880"),Color("0b2328") if active else Color("5f979e"),4)
		normal.content_margin_left = 26
		var hover := rounded(Color("4c8a92"),Color("8cc0c5"),4)
		hover.content_margin_left = 26
		task.add_theme_stylebox_override("normal",normal)
		task.add_theme_stylebox_override("hover",hover)
		task.add_theme_stylebox_override("pressed",normal)
		task.add_theme_stylebox_override("focus",StyleBoxEmpty.new())
		for state_name in ["font_color","font_hover_color","font_pressed_color"]: task.add_theme_color_override(state_name,Color("f6f3e8"))
		task.pressed.connect(toggle_window.bind(str(id)))
		var image := app_icon(id,.5)
		image.position = Vector2(4,4)
		task.add_child(image)
		task_buttons.add_child(task)

func toggle_window(id: String) -> void:
	var window: Panel = windows[id]
	if window.visible and focused_id != id:
		focus_window(id)
		return
	window.visible = not window.visible
	if window.visible: focus_window(id)
	else: refresh_tasks()

func _input(event: InputEvent) -> void:
	if not is_instance_valid(dragging):return
	if event is InputEventMouseMotion:
		dragging.position = (event.position-drag_offset).clamp(Vector2.ZERO,Vector2(640,448)-dragging.size)
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and not event.pressed:
		dragging = null

func browser_chrome(content: VBoxContainer, address: String) -> void:
	var menus := HBoxContainer.new()
	menus.add_theme_constant_override("separation",12)
	for word in ["File","Edit","View","Favorites","Tools","Help"]:
		menus.add_child(text_label(word,12,Color("4b524b")))
	content.add_child(menus)
	var navigation := HBoxContainer.new()
	navigation.add_theme_constant_override("separation",4)
	content.add_child(navigation)
	var back := button("◀ Back",browser_back)
	back.disabled = browser_history.is_empty()
	navigation.add_child(back)
	navigation.add_child(button("⌂ Home",func(): browse("","")))
	var field := PanelContainer.new()
	field.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	field.add_theme_stylebox_override("panel",rounded(Color("ffffff"),Color("7d9496"),2))
	field.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var address_row := HBoxContainer.new()
	address_row.add_child(text_label("Address",11,MUTED))
	var url := text_label(address,12,INK)
	url.clip_text = true
	url.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	address_row.add_child(url)
	field.add_child(address_row)
	navigation.add_child(field)
	var searchbar := HBoxContainer.new()
	searchbar.add_theme_constant_override("separation",5)
	content.add_child(searchbar)
	var logo := RichTextLabel.new()
	logo.bbcode_enabled = true
	logo.fit_content = true
	logo.autowrap_mode = TextServer.AUTOWRAP_OFF
	logo.scroll_active = false
	logo.custom_minimum_size = Vector2(98,24)
	logo.add_theme_font_override("normal_font",title_font)
	logo.add_theme_font_size_override("normal_font_size",15)
	logo.text = "[color=#2f6b72]Morrow[/color][color=#c8701f]Search[/color]"
	logo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	searchbar.add_child(logo)
	browser_input = LineEdit.new()
	browser_input.name = "SearchInput"
	browser_input.placeholder_text = "Search Morrow Creek…"
	browser_input.text = browser_query
	browser_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	browser_input.custom_minimum_size.y = 26
	browser_input.add_theme_font_size_override("font_size",15)
	browser_input.add_theme_color_override("font_color",INK)
	browser_input.add_theme_color_override("caret_color",INK)
	browser_input.add_theme_color_override("font_placeholder_color",Color("8a9087"))
	browser_input.add_theme_stylebox_override("normal",rounded(Color("ffffff"),Color("7d9496"),2))
	browser_input.add_theme_stylebox_override("focus",rounded(Color("fffdf3"),Color("d98a2b"),2))
	browser_input.text_submitted.connect(func(_value: String): submit_search())
	searchbar.add_child(browser_input)
	var search := primary_button("Search",submit_search)
	search.name = "SearchButton"
	search.custom_minimum_size.y = 26
	searchbar.add_child(search)

func page_frame(content: VBoxContainer) -> VBoxContainer:
	var scroll := ScrollContainer.new()
	scroll.name = "PageScroll"
	scroll.custom_minimum_size.y = 200
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	var paper := rounded(Color("fffefa"),Color("8d9a94"),0)
	paper.content_margin_left = 12
	paper.content_margin_right = 12
	paper.content_margin_top = 10
	paper.content_margin_bottom = 10
	scroll.add_theme_stylebox_override("panel",paper)
	content.add_child(scroll)
	var page := VBoxContainer.new()
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation",7)
	scroll.add_child(page)
	return page

func status_bar(content: VBoxContainer, loading: bool) -> void:
	var bar := HBoxContainer.new()
	bar.add_theme_constant_override("separation",8)
	content.add_child(bar)
	var status := text_label("Opening page…" if loading else "Done",12,MUTED)
	status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_child(status)
	var progress := ProgressBar.new()
	progress.show_percentage = false
	progress.custom_minimum_size = Vector2(70,10)
	progress.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	progress.add_theme_stylebox_override("background",rounded(Color("e3ddcc"),Color("a8ab9f"),2))
	progress.add_theme_stylebox_override("fill",rounded(Color("4f9a58"),Color("2e6a35"),2))
	progress.value = 0.0 if loading else 100.0
	progress.visible = loading
	bar.add_child(progress)
	bar.add_child(text_label("Connected at 56.0 Kbps",12,MUTED))
	if loading:
		var tween := status.create_tween()
		tween.tween_property(progress,"value",100.0,.45).set_trans(Tween.TRANS_QUAD)
		tween.tween_callback(func():
			status.text = "Done"
			progress.hide())

func open_browser(page_id := "", query := "") -> void:
	var loading := page_id != browser_page or query != browser_query
	browser_page = page_id
	browser_query = query
	var content := window_content("browser",game.db.site_name+" — Internet",Rect2(118,24,508,410))
	content.add_theme_constant_override("separation",5)
	var address := "http://www.morrowsearch.com/"
	if not page_id.is_empty(): address = str(game.db.page(page_id).get("url",""))
	elif not query.is_empty(): address = "http://www.morrowsearch.com/search?q="+query.uri_encode()
	browser_chrome(content,address)
	browser_body = page_frame(content)
	if not page_id.is_empty():
		var page: Dictionary = game.web.open_page(page_id)
		if page.is_empty():
			browser_body.add_child(paragraph("The page cannot be displayed."))
		else:
			var heading := paragraph(str(page.title),19)
			heading.add_theme_font_override("font",serif_font)
			heading.add_theme_color_override("font_color",Color("5a2516"))
			browser_body.add_child(heading)
			browser_body.add_child(rule())
			browser_body.add_child(text_label("Posted "+Calendar.full_date(str(page.published)),12,MUTED))
			browser_body.add_child(paragraph(str(page.body)))
			var note := primary_button("Add to journal",note_current_page)
			note.name = "NoteClue"
			note.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
			note.disabled = has_observation("web_"+page_id)
			if note.disabled: note.text = "✓ In your journal"
			browser_body.add_child(note)
	elif not query.is_empty():
		var results: Array = game.web.search(query)
		browser_body.add_child(text_label("Results 1 - %d for \"%s\"" % [results.size(),query],12,MUTED))
		browser_body.add_child(rule())
		for result in results:
			var page: Dictionary = result.page
			var result_button := link(str(page.title),browse.bind(str(page.id),query),15)
			result_button.name = "Result_"+str(page.id)
			result_button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			browser_body.add_child(result_button)
			browser_body.add_child(paragraph(str(page.body).left(104)+"…",13))
			browser_body.add_child(text_label(str(page.get("url","")).trim_prefix("http://"),11,Color("2f7a3a")))
		if results.is_empty(): browser_body.add_child(paragraph("No results found. Try different words."))
	else:
		home_page(browser_body)
		browser_body.add_child(text_label("Popular in Morrow Creek",13,INK,bold_font))
		for page in game.db.web_pages.values():
			browser_body.add_child(link("› "+str(page.title),browse.bind(str(page.id),"")))
		browser_body.add_child(text_label("© 2003 Morrow Search",11,MUTED))
	status_bar(content,loading)

func has_observation(id: String) -> bool:
	return game.state.data.observations.any(func(o): return o is Dictionary and o.get("id") == id)

func home_page(page: VBoxContainer) -> void:
	var logo := RichTextLabel.new()
	logo.bbcode_enabled = true
	logo.fit_content = true
	logo.scroll_active = false
	logo.add_theme_font_override("normal_font",serif_font)
	logo.add_theme_font_size_override("normal_font_size",32)
	logo.text = "[center][color=#2f6b72]Morrow[/color][color=#c8701f]Search[/color][/center]"
	logo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	page.add_child(logo)
	var tagline := paragraph("Find it in Morrow Creek.\nLocal businesses, music and town news.",14)
	tagline.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tagline.add_theme_color_override("font_color",MUTED)
	page.add_child(tagline)
	page.add_child(rule())

func rule() -> HSeparator:
	var line := HSeparator.new()
	var style := StyleBoxLine.new()
	style.color = Color("d6cfbb")
	style.thickness = 1
	line.add_theme_stylebox_override("separator",style)
	return line

func paragraph(value: String, font_size := 15) -> Label:
	var label := text_label(value,font_size)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	return label

func browse(page_id: String, query: String) -> void:
	browser_history.append({"page":browser_page,"query":browser_query})
	open_browser(page_id,query)

func submit_search() -> void:
	browse("",browser_input.text.strip_edges())

func browser_back() -> void:
	if browser_history.is_empty(): open_browser()
	else:
		var previous: Dictionary = browser_history.pop_back()
		open_browser(str(previous.page),str(previous.query))

func note_current_page() -> void:
	last_note_succeeded = game.web.note(browser_page)
	open_browser(browser_page,browser_query)
	if windows.has("notes"): open_notes()
	if last_note_succeeded: show_balloon("Journal","Added to your journal.","notes")

func open_notes() -> void:
	var content := window_content("notes","Journal — notes.txt",Rect2(160,68,430,340))
	var header := HBoxContainer.new()
	header.add_child(text_label("My journal",20,Color("5a3620"),title_font))
	var count := text_label("%d entries" % game.state.data.observations.size(),12,MUTED)
	count.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	count.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(count)
	content.add_child(header)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.y = 227
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	var paper := StyleBoxFlat.new()
	paper.bg_color = Color("fdf8e6")
	paper.border_color = Color("c8402c")
	paper.border_width_left = 2
	paper.content_margin_left = 16
	paper.content_margin_right = 10
	paper.content_margin_top = 8
	paper.content_margin_bottom = 8
	scroll.add_theme_stylebox_override("panel",paper)
	content.add_child(scroll)
	var body := VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation",3)
	scroll.add_child(body)
	if game.state.data.observations.is_empty(): body.add_child(paragraph("Nothing written yet.",15))
	for entry in game.state.data.observations:
		if entry is Dictionary:
			body.add_child(text_label(Calendar.long_date(str(entry.get("date",""))),12,Color("4a6a8c")))
			var text := paragraph(str(entry.get("text","")),15)
			body.add_child(text)
			body.add_child(rule())

func open_messages() -> void:
	var content := window_content("messages","Messages — mossline",Rect2(150,60,400,330))
	content.add_theme_constant_override("separation",5)
	var header := HBoxContainer.new()
	var buddy := text_label("● mossline",14,Color("3c8a46"),bold_font)
	buddy.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(buddy)
	header.add_child(text_label("Away",12,MUTED))
	content.add_child(header)
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.add_theme_stylebox_override("panel",rounded(Color("ffffff"),Color("8d9a94"),0))
	content.add_child(scroll)
	var log := VBoxContainer.new()
	log.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	log.add_theme_constant_override("separation",6)
	scroll.add_child(log)
	var shown: Array = game.state.messages_until_today()
	if shown.is_empty(): log.add_child(paragraph("No messages.",14))
	for message in shown:
		log.add_child(text_label("%s · %s" % [str(message.from),Calendar.long_date(GoldenState.DATES[int(message.day)])],11,Color("2f6b72"),bold_font))
		log.add_child(paragraph(str(message.text),14))
		game.state.mark_read(str(message.id))
	content.add_child(text_label("mossline is away and may not reply.",11,MUTED))

func set_pointer(point: Vector2, enabled: bool) -> void:
	pointer.position = point.round()
	pointer.visible = enabled
	if not enabled: return
	var hovered: Control = null
	var viewport := get_viewport()
	if viewport != null and viewport.has_method("gui_get_hovered_control"): hovered = viewport.gui_get_hovered_control()
	var kind := "arrow"
	if hovered is LineEdit: kind = "beam"
	elif hovered is Button and hovered.has_meta("hand") and not (hovered as Button).disabled: kind = "hand"
	(pointer as CedarPointer).kind = kind

func show_balloon(title: String, message: String, icon_kind := "save") -> void:
	if is_instance_valid(balloon): balloon.queue_free()
	balloon = Panel.new()
	balloon.name = "Balloon"
	balloon.z_index = 2600
	balloon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	balloon.size = Vector2(230,74)
	balloon.position = Vector2(384,366)
	var style := rounded(Color("fffbe2"),Color("2c3a36"),7)
	style.shadow_color = Color(0,0,0,.35)
	style.shadow_size = 4
	style.shadow_offset = Vector2(2,2)
	balloon.add_theme_stylebox_override("panel",style)
	add_child(balloon)
	var icon := app_icon(icon_kind,.55)
	icon.position = Vector2(8,8)
	balloon.add_child(icon)
	var heading := text_label(title,14,INK,bold_font)
	heading.position = Vector2(34,6)
	balloon.add_child(heading)
	var text := text_label(message if message.length() <= 64 else message.left(62)+"…",13,INK)
	text.position = Vector2(34,26)
	text.size = Vector2(188,44)
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	balloon.add_child(text)
	chime.emit()
	var shown := balloon
	var tween := shown.create_tween()
	tween.tween_interval(3.5)
	tween.tween_property(shown,"modulate:a",0.0,.4)
	tween.tween_callback(shown.queue_free)

# Calendar: October 2003, the three days of this prototype marked, today highlighted.
func open_agenda() -> void:
	var col := window_content("agenda","Calendar — October 2003",Rect2(120,24,500,410))
	col.add_theme_constant_override("separation",6)
	var today: String = game.state.date()
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation",10)
	var page := Control.new()
	page.custom_minimum_size = Vector2(52,52)
	page.mouse_filter = Control.MOUSE_FILTER_IGNORE
	page.add_child(app_icon("agenda",1.35))
	header.add_child(page)
	var titles := VBoxContainer.new()
	titles.add_theme_constant_override("separation",0)
	titles.add_child(text_label(Calendar.weekday(today),22,Color("1f4c52"),title_font))
	titles.add_child(text_label(Calendar.full_date(today),15,INK))
	titles.add_child(text_label(game.state.clock(),13,Color("b0601f"),bold_font))
	header.add_child(titles)
	col.add_child(header)
	col.add_child(rule())
	var grid := GridContainer.new()
	grid.columns = 7
	grid.add_theme_constant_override("h_separation",4)
	grid.add_theme_constant_override("v_separation",4)
	for name in ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]:
		var head := text_label(name,12,MUTED,bold_font)
		head.custom_minimum_size = Vector2(62,0)
		head.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		grid.add_child(head)
	# October 1, 2003 was a Wednesday.
	for blank in 3: grid.add_child(Control.new())
	for day in range(1,32):
		var iso := "2003-10-%02d" % day
		var cell := PanelContainer.new()
		cell.custom_minimum_size = Vector2(62,26)
		var fill := Color("fbf8ee")
		if iso in GoldenState.DATES: fill = Color("f3dfb8")
		if iso == today: fill = Color("e3a04f")
		cell.add_theme_stylebox_override("panel",rounded(fill,Color("c9c2ad"),3))
		var number := text_label(str(day),13,Color("ffffff") if iso == today else INK,bold_font if iso in GoldenState.DATES else null)
		number.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		cell.add_child(number)
		grid.add_child(cell)
	col.add_child(grid)
	col.add_child(paragraph("Fall Market — Saturday the 25th.",13))

func refresh_metadata() -> void:
	var today: String = game.state.date()
	weekday_caption.text = Calendar.weekday(today).to_upper()
	date_caption.text = Calendar.full_date(today).to_upper()
	clock_caption.text = game.state.clock()
	for icon in find_children("*","CedarIcon",true,false):
		(icon as CedarIcon).day = str(Calendar.day_number(today))
		icon.queue_redraw()

func refresh_apps() -> void:
	var opened: Array = []
	for child in get_children():
		if child is Panel and str(child.name).begins_with("Window_"):
			opened.append([str(child.name).trim_prefix("Window_"),child.visible])
	for item in opened:
		open_app(item[0])
		windows[item[0]].visible = item[1]
	refresh_tasks()
	var unread: Dictionary = game.state.unread_message()
	if not unread.is_empty(): show_balloon("mossline says:",str(unread.text),"messages")

func open_save(message: String = "") -> void:
	var col := window_content("save","Save — Golden Fall",Rect2(136,80,480,290))
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation",14)
	var holder := Control.new()
	holder.custom_minimum_size = Vector2(64,64)
	holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	holder.add_child(app_icon("save",1.6))
	row.add_child(holder)
	var info := VBoxContainer.new()
	info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info.add_child(text_label("Morrow Creek",19,Color("1f4c52"),title_font))
	info.add_child(paragraph("%s · %s" % [Calendar.long_date(game.state.date()),game.state.clock()],14))
	info.add_child(paragraph("Progress also saves on its own when you leave the computer, before you sleep and when you quit.",13))
	row.add_child(info)
	col.add_child(row)
	col.add_child(rule())
	var save := primary_button("Save now",manual_save)
	save.name = "ManualSave"
	save.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	col.add_child(save)
	if not message.is_empty():
		var ok: bool = game.get("save_error") == OK
		var status := paragraph(("✓ " if ok else "✗ ")+message,15)
		status.name = "SaveStatus"
		status.add_theme_color_override("font_color",Color("2f7a3a") if ok else Color("a8321c"))
		col.add_child(status)

func manual_save() -> void:
	game.save_game(false)
	var ok: bool = game.get("save_error") == OK
	open_save("Saved." if ok else "Couldn't save (error %s)." % game.get("save_error"))
	if ok: show_balloon("Saved","Progress saved to disk.")
