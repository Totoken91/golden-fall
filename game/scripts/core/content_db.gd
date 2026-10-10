class_name ContentDB
extends RefCounted

# Authored English content from the Golden Fall V0.9 pack (game/data/*_en.json).
var dialogues: Dictionary = {}
var rehearsal: Dictionary = {}
var days: Array = []
var messages: Array = []
var web_pages: Dictionary = {}
var site_name := "Morrow Search"
var blips: Dictionary = {}
var state_template: Dictionary = {}

func _init() -> void:
	var dialogue_doc := load_json("dialogues_en")
	for node in dialogue_doc.get("nodes",[]): dialogues[node.id] = node
	rehearsal = dialogue_doc.get("rehearsal",{})
	days = load_json("events_en").get("days",[])
	messages = load_json("messages_en").get("messages",[])
	var web_doc := load_json("web_pages_en")
	site_name = str(web_doc.get("site_name",site_name))
	for entry in web_doc.get("pages",[]): web_pages[entry.id] = entry
	blips = load_json("blip_profiles")
	state_template = load_json("state_example").get("new_game",{})

static func load_json(name: String) -> Dictionary:
	var path := "res://data/%s.json" % name
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		push_error("Unreadable content file: "+path)
		return {}
	return parsed

func page(id: String) -> Dictionary:
	return web_pages.get(id,{})
