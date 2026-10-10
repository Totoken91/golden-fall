"""Shared export stage. ROOT, OUT and SOURCE come from the authoring script."""
for im in bpy.data.images:im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'hero_props.blend'))
(ROOT/'assets/exported').mkdir(parents=True,exist_ok=True)
families={}
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.get('hero_family'):families.setdefault(o['hero_family'],[]).append(o)
for family,objects in families.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets/exported'/f'{family}.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_yup=True,export_apply=True)
groups={}
for o in list(bpy.context.scene.objects):
    if o.type=='MESH':groups.setdefault((o.get('group','Detail'),tuple(m.name for m in o.data.materials)),[]).append(o)
for (tag,materials),objects in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join();o=bpy.context.object;o.name=f'{tag}_{materials[0]}'
    mod=o.modifiers.new('Stable triangles','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=mod.name)
for im in bpy.data.images:im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'bedroom_psx.blend'))
bpy.ops.export_scene.gltf(filepath=str(OUT/'bedroom.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_yup=True,export_apply=True)
shutil.copy2(OUT/'bedroom.glb',ROOT/'assets/exported/bedroom_psx.glb')
print('Exported original bedroom:',OUT/'bedroom.glb')
