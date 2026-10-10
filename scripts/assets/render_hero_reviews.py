"""Render genuine Blender studio views of editable hero asset families."""
from pathlib import Path
import bpy,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/blender/hero_props.blend'))
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.world.use_nodes=True
background=scene.world.node_tree.nodes.get('Background')
background.inputs[0].default_value=(.16,.17,.16,1);background.inputs[1].default_value=.45
all_meshes=[o for o in scene.objects if o.type=='MESH']
families={}
for o in all_meshes:
    o.hide_render=True
    if o.get('review_family'):families.setdefault(o['review_family'],[]).append(o)
    elif o.get('hero_family'):families.setdefault(o['hero_family'],[]).append(o)
    elif o.get('group')=='I_bed':families.setdefault('bedding',[]).append(o)
families['curtains']=[o for o in all_meshes if any(token in o.name for token in ['Curtain','Sill','WindowJamb','WindowRail','Mullion','Crossbar'])]
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.lens=55
lights=[]
for loc,power,size in [((-3,-4,5),380,4),((3,-1,3),200,3),((0,3,4),280,3)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;lights.append(o)
out=ROOT/'captures/asset_reviews';out.mkdir(parents=True,exist_ok=True)
for family,objects in families.items():
    if family not in ['headphones','computer','photo_frame','bedding','curtains']:continue
    for o in all_meshes:o.hide_render=o not in objects
    points=[o.matrix_world@Vector(p) for o in objects for p in o.bound_box]
    lower=Vector([min(p[i] for p in points) for i in range(3)]);upper=Vector([max(p[i] for p in points) for i in range(3)])
    center=(lower+upper)/2;extent=upper-lower;scale=max(extent)*1.28
    cam.data.ortho_scale=scale
    views=[('01_trois_quarts',Vector((-1.25,-2,1.0))),('02_face',Vector((0,-2,.12))),('03_profil',Vector((2,0,.12))),('04_ambre',Vector((-1.25,-2,1.0)))]
    if family in ['keyboard','headphones']:views[0]=('01_trois_quarts',Vector((-.7,-1.1,2)));views[3]=('04_ambre',Vector((-.7,-1.1,2)))
    for name,direction in views:
        warm=name.endswith('ambre')
        background.inputs[0].default_value=(.10,.115,.12,1) if warm else (.16,.17,.16,1)
        background.inputs[1].default_value=.28 if warm else .45
        for i,o in enumerate(lights):
            o.location=center+Vector([(-3,-4,5),(3,-1,3),(0,3,4)][i])*max(.5,scale)
            o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
            o.data.color= ((1,.69,.36) if i==0 else (.63,.74,.82)) if warm else (1,1,1)
        cam.location=center+direction.normalized()*max(2,scale*3)
        cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(out/(family+'_'+name+'.png'))
        bpy.ops.render.render(write_still=True)
print('Rendered four genuine views per hero family')
