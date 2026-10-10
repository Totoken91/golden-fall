"""Blender 4.2 -b --python-exit-code 1 -P scripts/assets/apply_poster_art.py.

Replace two image nodes in both editable sources, preserving all geometry,
then export the runtime room. Run prepare_poster_textures.py first.
"""
from pathlib import Path
import bpy, shutil, json

ROOT = Path(__file__).resolve().parents[2]
TEXTURES = ROOT/'game/assets/room/textures'
report = {}
for name in ['hero_props', 'bedroom_psx']:
    source = ROOT/'assets/blender'/(name+'.blend')
    bpy.ops.wm.open_mainfile(filepath=str(source))
    def geometry():
        return {
            o.name: {
                'vertices': [tuple(v.co) for v in o.data.vertices],
                'polygons': [tuple(p.vertices) for p in o.data.polygons],
                'matrix': [tuple(row) for row in o.matrix_world],
                'uvs': [[tuple(v.uv) for v in layer.data] for layer in o.data.uv_layers],
                'materials': [m.name for m in o.data.materials],
            } for o in bpy.context.scene.objects if o.type == 'MESH'
        }
    before = geometry()
    for material_name in ['poster','poster2']:
        mat = bpy.data.materials[material_name]
        nodes = [n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE']
        assert len(nodes) == 1, material_name
        image = bpy.data.images.load(str(TEXTURES/(material_name+'.png')),check_existing=False)
        image.name = material_name+'_imagegen_v011'
        nodes[0].image = image
        nodes[0].interpolation = 'Closest'
        image.pack()
    for image in bpy.data.images:
        local = TEXTURES/Path(image.filepath).name
        if local.exists():
            image.filepath = '//../../game/assets/room/textures/'+local.name
        if image.source == 'FILE' and not image.packed_file:
            image.pack()
    assert before == geometry(), 'Texture pass altered geometry'
    bpy.ops.wm.save_as_mainfile(filepath=str(source))
    report[name] = {'mesh_objects':len(before),'geometry_transforms_uvs_material_assignments_unchanged':True}
    if name == 'bedroom_psx':
        output = ROOT/'game/assets/room/bedroom.glb'
        bpy.ops.export_scene.gltf(filepath=str(output),export_format='GLB',export_cameras=False,
            export_lights=False,export_yup=True,export_apply=True)
        shutil.copy2(output,ROOT/'assets/exported/bedroom_psx.glb')
(ROOT/'verification/poster_source_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Poster images applied; all geometry, transforms, UVs and assignments unchanged.')
