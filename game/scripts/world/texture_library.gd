extends RefCounted
## Opt-in offline material binding. Merely adding this script changes no object.

var catalog: Dictionary = {}

func _init() -> void:
	var path := "res://assets/textures/library/catalog.json"
	if FileAccess.file_exists(path):
		var decoded = JSON.parse_string(FileAccess.get_file_as_string(path))
		if decoded is Dictionary: catalog = decoded

func material_for_uv(key: String, authored_uv_period_m: Vector2) -> StandardMaterial3D:
	if not catalog.has(key) or authored_uv_period_m.x <= 0 or authored_uv_period_m.y <= 0:
		push_error("Texture key missing or UV period unspecified: " + key)
		return null
	var entry: Dictionary = catalog[key]
	var tile: Array = entry.tile_m
	if tile.size() != 2 or float(tile[0]) <= 0 or float(tile[1]) <= 0: return null
	var source := load(str(entry.material)) as StandardMaterial3D
	if source == null: return null
	var material := source.duplicate() as StandardMaterial3D
	# If one authored UV repeat spans 1.8m and source spans 1.5m, scale is 1.2.
	material.uv1_scale = Vector3(authored_uv_period_m.x / float(tile[0]), authored_uv_period_m.y / float(tile[1]), 1)
	return material

func apply_surface(instance: MeshInstance3D, surface: int, key: String, authored_uv_period_m: Vector2) -> Error:
	if instance == null or instance.mesh == null or surface < 0 or surface >= instance.mesh.get_surface_count():
		return ERR_INVALID_PARAMETER
	var arrays := instance.mesh.surface_get_arrays(surface)
	if arrays[Mesh.ARRAY_TEX_UV] == null or arrays[Mesh.ARRAY_TEX_UV].is_empty():
		push_error("Texture application requires existing non-empty UVs")
		return ERR_INVALID_DATA
	var material := material_for_uv(key, authored_uv_period_m)
	if material == null: return ERR_INVALID_DATA
	instance.set_surface_override_material(surface, material)
	return OK
