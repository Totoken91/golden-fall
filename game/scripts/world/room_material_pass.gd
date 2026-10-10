extends RefCounted
## Material-only pass. Original meshes/materials are retained for exact before/after QA.
var baseline: Array = []
var applied: Array = []

func apply(model: Node3D, rules: Array) -> void:
	restore()
	applied.clear()
	var library = load("res://scripts/world/texture_library.gd").new()
	for node in model.find_children("*", "MeshInstance3D", true, false):
		for rule in rules:
			if str(node.name).replace(".","_") != str(rule.node).replace(".","_"): continue
			for surface in node.mesh.get_surface_count():
				var original = node.get_active_material(surface)
				if not original is StandardMaterial3D or original.resource_name != rule.material_name: continue
				if not baseline.any(func(item): return item.node == node and item.surface == surface):
					baseline.append({"node":node,"surface":surface,"mesh":node.mesh,"material":original})
				var material: StandardMaterial3D
				if rule.has("key"):
					var period: Array = rule.get("uv_period_m",[1.0,1.0])
					material = library.material_for_uv(str(rule.key),Vector2(period[0],period[1]))
				else:
					material = load(str(rule.material)).duplicate()
				assert(material != null)
				if rule.get("metric_wood_uv",false): node.mesh = metric_wood_mesh(node.mesh,str(rule.get("grain_axis","u")))
				if rule.has("texels_per_m"):
					assert(rule.get("metric_wood_uv",false),"Density settings require UVs in metres")
					var density := float(rule.texels_per_m)
					material.uv1_scale=Vector3(density/material.albedo_texture.get_width(),density/material.albedo_texture.get_height(),1)
				material.resource_name = original.resource_name
				material.normal_scale = float(rule.get("normal_scale",material.normal_scale))
				material.metallic = float(rule.get("metallic",0.0))
				if rule.has("tint"):
					var tint: Array = rule.tint
					material.albedo_color = Color(tint[0],tint[1],tint[2])
				if rule.get("double_sided",false): material.cull_mode = BaseMaterial3D.CULL_DISABLED
				if rule.get("keep_emission",false):
					material.emission_enabled = original.emission_enabled
					material.emission = original.emission
					material.emission_operator = original.emission_operator
					material.emission_texture = material.albedo_texture
					material.emission_energy_multiplier = original.emission_energy_multiplier
				node.set_surface_override_material(surface,material)
				applied.append({"node":str(node.name),"surface":surface,"material":str(original.resource_name),
					"source":str(rule.get("key",rule.get("material",""))),
					"size":[material.albedo_texture.get_width(),material.albedo_texture.get_height()],
					"mipmaps":material.albedo_texture.get_image().has_mipmaps(),
					"texels_per_m": [material.albedo_texture.get_width()*material.uv1_scale.x,material.albedo_texture.get_height()*material.uv1_scale.y] if rule.get("metric_wood_uv",false) else [],
					"uv_mode":"metres, grain along longest face axis" if rule.get("metric_wood_uv",false) else "authored UV preserved"})

func restore() -> void:
	for item in baseline:
		item.node.mesh = item.mesh
		item.node.set_surface_override_material(item.surface,item.material)

func metric_wood_mesh(source: Mesh, grain_axis: String) -> ArrayMesh:
	# Project each existing flat face in metres. No vertex, normal, index or collision moves.
	# Furniture groups contain cubes with different old UV periods: one group-wide scale is wrong.
	var result := ArrayMesh.new()
	for surface in source.get_surface_count():
		var arrays: Array = source.surface_get_arrays(surface).duplicate(true)
		var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var normals: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
		var uv: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
		var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		var tangents := PackedFloat32Array()
		tangents.resize(vertices.size()*4)
		for start in range(0,indices.size(),3):
			var ids := [indices[start],indices[start+1],indices[start+2]]
			var normal: Vector3 = normals[ids[0]].abs()
			var drop := normal.max_axis_index()
			var axes: Array[int] = []
			for axis in 3:
				if axis != drop: axes.append(axis)
			var a: Vector3 = vertices[ids[0]]
			var b: Vector3 = vertices[ids[1]]
			var c: Vector3 = vertices[ids[2]]
			var extent: Vector3 = a.max(b).max(c)-a.min(b).min(c)
			if extent[axes[1]] > extent[axes[0]]: axes.reverse()
			if grain_axis=="v": axes.reverse()
			var u_axis := Vector3.ZERO
			var v_axis := Vector3.ZERO
			u_axis[axes[0]]=1.0
			v_axis[axes[1]]=1.0
			for id in ids:
				uv[id]=Vector2(vertices[id][axes[0]],vertices[id][axes[1]])
				var n: Vector3 = normals[id]
				var t: Vector3 = (u_axis-n*n.dot(u_axis)).normalized()
				tangents[id*4]=t.x
				tangents[id*4+1]=t.y
				tangents[id*4+2]=t.z
				tangents[id*4+3]=1.0 if n.cross(t).dot(v_axis)>0 else -1.0
		arrays[Mesh.ARRAY_TEX_UV]=uv
		arrays[Mesh.ARRAY_TANGENT]=tangents
		result.add_surface_from_arrays(source.surface_get_primitive_type(surface),arrays)
		result.surface_set_material(surface,source.surface_get_material(surface))
	return result
