#!/usr/bin/env python3
"""Demo procedural autumn streetlamp. Run with Blender, not regular Python.

blender -b --python scripts/assets/generate_streetlamp.py -- --out-dir assets
Creates editable .blend and portable .glb, but does NOT validate their look in Godot.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import bpy
    from mathutils import Vector
except ImportError as exc:
    raise SystemExit("Exécuter avec Blender : blender -b --python ...") from exc

ASSET_ID = "prop_streetlamp_sodium"


def material(name: str, rgba: tuple[float, float, float, float], *, emission: bool = False):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs["Base Color"].default_value = rgba
        principled.inputs["Roughness"].default_value = 0.84
        if emission:
            principled.inputs["Emission Color"].default_value = rgba
            principled.inputs["Emission Strength"].default_value = 0.55
    return mat


def set_material(obj, mat):
    obj.data.materials.append(mat)
    return obj


def cube(name, location, scale, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("soft_edges", "BEVEL")
        mod.width = bevel
        mod.segments = 1
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return set_material(obj, mat)


def cylinder(name, loc, radius, depth, mat, vertices=10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    return set_material(obj, mat)


def segment_between(name, p1, p2, radius, mat):
    center = (Vector(p1) + Vector(p2)) * 0.5
    depth = (Vector(p2) - Vector(p1)).length
    obj = cylinder(name, center, radius, depth, mat)
    obj.rotation_euler = (Vector(p2) - Vector(p1)).to_track_quat('Z', 'Y').to_euler()
    return obj


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bronze = material("PBR_dark_oxidized_metal", (0.23, 0.19, 0.15, 1))
    trim = material("PBR_metal_trim", (0.32, 0.27, 0.20, 1))
    warm = material("PBR_lens_warm_amber", (0.95, 0.45, 0.12, 1), emission=True)
    objects = []
    objects.append(cylinder("lamp_base", (0, 0, 0.13), 0.23, 0.26, trim, 12))
    objects.append(cylinder("lamp_pole", (0, 0, 2.05), 0.070, 3.85, bronze, 10))
    objects.append(segment_between("lamp_curve_1", (0,0,3.84), (.26,0,4.09), .055, bronze))
    objects.append(segment_between("lamp_curve_2", (.26,0,4.09), (.90,0,4.08), .055, bronze))
    objects.append(cube("lamp_housing", (.95, 0, 4.02), (.45,.30,.12), bronze, .02))
    objects.append(cube("lamp_lens", (.95, 0, 3.948), (.36,.23,.025), warm))
    objects.append(cube("lamp_brace", (.8,0,3.89), (.22,.07,.05), trim))
    for obj in objects:
        obj.select_set(True)
        # Static scene / origin convention: pivot at world 0, bottom at ground (z=0)
        obj["asset_id"] = ASSET_ID
    return objects


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("assets"))
    options = parser.parse_args(args)
    output = options.out_dir.resolve()
    source = output / "source_blender" / (ASSET_ID + ".blend")
    exported = output / "exported" / (ASSET_ID + ".glb")
    source.parent.mkdir(parents=True, exist_ok=True)
    exported.parent.mkdir(parents=True, exist_ok=True)
    created = build()
    bpy.ops.wm.save_as_mainfile(filepath=str(source))
    bpy.ops.object.select_all(action="DESELECT")
    for obj in created:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = created[0]
    bpy.ops.export_scene.gltf(filepath=str(exported), export_format="GLB", use_selection=True)
    print(f"GÉNÉRÉ : {source} | {exported}")
    print("NON VALIDÉ : vérifier géométrie, éclairage et échelle dans Godot.")


if __name__ == "__main__":
    main()
