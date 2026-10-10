class_name SaveManager
extends RefCounted

# Atomic JSON save of GoldenState. A rejected file never replaces the live state.
const PATH := "user://golden_fall_v1.json"

static func write(state: GoldenState, path: String = PATH) -> Error:
	var file := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if file == null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify(state.data, "\t"))
	file.close()
	return DirAccess.rename_absolute(ProjectSettings.globalize_path(path + ".tmp"), ProjectSettings.globalize_path(path))

static func read_into(state: GoldenState, path: String = PATH) -> bool:
	if not FileAccess.file_exists(path): return false
	var value = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not value is Dictionary or str(value.get("schema_version","")) != GoldenState.SCHEMA: return false
	var merged: Dictionary = state.new_game()
	merged.merge(value, true)
	var day = merged.get("day_index")
	if not (day is int or day is float) or int(day) < 0 or int(day) > GoldenState.LAST_DAY: return false
	merged.day_index = int(day)
	if not GoldenState.CLOCK.has(merged.get("time_slot")): return false
	for key in ["dialogue_choices","flags","npc_memories","rehearsal_state","pc","view"]:
		if not merged.get(key) is Dictionary: return false
	for key in ["dialogue_exchanges","visited_sites","observations","search_history","read_messages"]:
		if not merged.get(key) is Array: return false
	if not merged.get("finished_micro_mvp") is bool: return false
	if not valid_view(merged.view): return false
	state.data = merged
	state.changed.emit()
	return true

# The bedroom is 5.6 x 5.8 m; anything outside means a corrupted or foreign save.
static func valid_view(view: Dictionary) -> bool:
	if view.is_empty(): return true
	var pos = view.get("position")
	if not pos is Array or pos.size() != 3: return false
	for number in pos + [view.get("yaw",0),view.get("pitch",0)]:
		if not (number is float or number is int) or not is_finite(float(number)): return false
	if absf(float(pos[0])) > 3.0 or absf(float(pos[2])) > 3.5 or float(pos[1]) < -.2 or float(pos[1]) > .5: return false
	return absf(float(view.get("pitch",0))) <= 1.31
