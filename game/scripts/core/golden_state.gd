class_name GoldenState
extends RefCounted

# Durable Golden Fall state (docs/golden_fall/08_STATE_DATA_CONTRACT.md).
# Three days, Oct 15-17 2003. Time moves only by sleeping and committed conversations;
# walking, reading and using the PC never cost time.
signal changed

const SCHEMA := "0.9.0"
const DATES := ["2003-10-15","2003-10-16","2003-10-17"]
const LAST_DAY := 2
const CLOCK := {"afternoon":"4:10 PM","evening":"7:40 PM","night":"10:15 PM"}

var db: ContentDB
var data: Dictionary

func _init(content: ContentDB) -> void:
	db = content
	data = new_game()

func new_game() -> Dictionary:
	var fresh: Dictionary = db.state_template.duplicate(true)
	fresh.schema_version = SCHEMA
	for key in ["search_history","read_messages"]: fresh[key] = []
	fresh.pc = {"open":false,"apps":[],"page":"","query":""}
	fresh.view = {}
	return fresh

func date() -> String: return DATES[clampi(int(data.day_index),0,LAST_DAY)]
func clock() -> String: return CLOCK.get(data.time_slot,"4:10 PM")
func is_last_day() -> bool: return int(data.day_index) >= LAST_DAY

func flag(id: String) -> bool: return bool(data.flags.get(id,false))

func set_flag(id: String, value := true) -> void:
	data.flags[id] = value
	changed.emit()

# Journal entries are first-hand observations or things the player chose to note.
func observe(id: String, text: String, kind := "witnessed") -> bool:
	for entry in data.observations:
		if entry is Dictionary and entry.get("id") == id: return false
	data.observations.append({"id":id,"day":int(data.day_index),"date":date(),"kind":kind,"text":text})
	changed.emit()
	return true

func messages_until_today() -> Array:
	return db.messages.filter(func(m): return int(m.day) <= int(data.day_index))

func unread_message() -> Dictionary:
	for message in messages_until_today():
		if message.id not in data.read_messages: return message
	return {}

func mark_read(id: String) -> void:
	if id not in data.read_messages:
		data.read_messages.append(id)
		changed.emit()

# Advances exactly one day. On the last day it ends the prototype instead.
func sleep() -> bool:
	if data.finished_micro_mvp: return false
	if is_last_day():
		data.finished_micro_mvp = true
	else:
		data.day_index = int(data.day_index)+1
		data.time_slot = "afternoon"
	data.location = "bedroom"
	changed.emit()
	return true
