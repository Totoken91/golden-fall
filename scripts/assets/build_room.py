"""Run with Blender 4.2 -b -P. Original bedroom geometry, UVs and editable source."""
from pathlib import Path
import bpy, math, random
import shutil, os
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'game/assets/room'
SOURCE=ROOT/'assets/blender'
SOURCE.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
rng=random.Random(130103)
mats={}
for p in sorted((OUT/'textures').glob('*.png')):
    m=bpy.data.materials.new(p.stem); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Roughness'].default_value=.88
    tex=m.node_tree.nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(p)); tex.interpolation='Closest'; tex.extension='REPEAT'
    m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    if p.stem=='glass':
        m.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']); m.surface_render_method='DITHERED'
    if p.stem.startswith(('leaves','canopy','treeline')) or p.stem in ['pinecard','underbrush']:
        m.node_tree.links.new(tex.outputs['Alpha'],bs.inputs['Alpha']); m.surface_render_method='DITHERED'; m.use_backface_culling=False
    if p.stem in ['screen','shade']:
        m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Emission Color'])
        bs.inputs['Emission Strength'].default_value=.45 if p.stem=='screen' else .18
    mats[p.stem]=m

def color(name,c):
    m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*c,1); bs.inputs['Roughness'].default_value=.95
    mats[name]=m
for n,c in [('leaf_ochre',(.30,.17,.055)),('leaf_copper',(.40,.20,.075)),('leaf_olive',(.19,.21,.12)),('pine',(.11,.16,.13)),('sky',(.32,.37,.38)),('coffee',(.07,.045,.02))]: color(n,c)

def setup(obj,mat,tag):
    obj.name=tag+'_'+obj.name
    obj.data.materials.append(mats[mat]); obj['group']=tag
    return obj

def cube(name,loc,dim,mat='wood',tag='Detail',bevel=0,tile=1):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    uv=o.data.uv_layers.active
    for poly in o.data.polygons:
        n=poly.normal; axis=max(range(3),key=lambda i:abs(n[i])); axes=[i for i in range(3) if i!=axis]
        for li in poly.loop_indices:
            v=o.data.vertices[o.data.loops[li].vertex_index].co
            uv.data[li].uv=(v[axes[0]]/tile+.5,v[axes[1]]/tile+.5)
    # Only the large CRT bezel and mattress need a silhouette chamfer.
    # All small furniture edges remain angular; wear is carried by the textures.
    if name not in ['CRTBezel','Mattress']:bevel=0
    if name=='Mattress':bevel=min(bevel,.025)
    if bevel:
        mod=o.modifiers.new('Worn edges','BEVEL'); mod.width=bevel; mod.segments=1
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return setup(o,mat,tag)

def cyl(name,loc,r,depth,mat='wood',tag='Detail',verts=8,r2=None,cap=True):
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r,radius2=r if r2 is None else r2,depth=depth,location=loc,end_fill_type='NGON' if cap else 'NOTHING')
    o=bpy.context.object; o.name=name; return setup(o,mat,tag)

def beam(name,a,b,r,mat='wood',tag='Detail',r2=None):
    a,b=Vector(a),Vector(b)
    if tag=='Outside' and name=='TreeBranch':
        # Crossed tapered ribbons retain distant silhouettes in all window views.
        axis=(b-a).normalized();right=axis.cross(Vector((0,1,0)))
        if right.length<.01:right=axis.cross(Vector((1,0,0)))
        right.normalize();up=axis.cross(right).normalized();tip=r if r2 is None else r2
        verts=[]
        for direction in [right,up]:verts.extend([a-direction*r,a+direction*r,b+direction*tip,b-direction*tip])
        return mesh(name,verts,[(0,1,2,3),(4,5,6,7)],mat,tag,[(0,0),(1,0),(1,1),(0,1)]*2)
    o=cyl(name,(a+b)/2,r,(b-a).length,mat,tag,verts=3 if tag=='Outside' else 4,r2=r2,cap=False)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o

def mesh(name,verts,faces,mat,tag='Detail',uvs=None):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o); setup(o,mat,tag)
    uv=me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        for li in poly.loop_indices:
            idx=me.loops[li].vertex_index; uv.data[li].uv=uvs[idx] if uvs else (verts[idx][0],verts[idx][2])
    return o

def front_panel(name,x,y,z,w,h,mat,tag='Detail'):
    return mesh(name,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[(0,1,2,3)],mat,tag,[(0,0),(1,0),(1,1),(0,1)])

exec(compile((Path(__file__).parent/'hero_props.py').read_text(encoding='utf-8'),'hero_props.py','exec'))

# Shell. A real window opening and a full door; all surfaces stay in place.
cube('Floor',(0,0,-.10),(5.6,5.8,.20),'floor','C_static',tile=1.8)
cube('Ceiling',(0,0,2.87),(5.6,5.8,.12),'ceiling','C_static',tile=1.5)
for x in [-2.8,2.8]: cube('SideWall',(x,0,1.425),(.14,5.8,2.85),'wall','C_static',tile=1.15)
cube('FrontWall',(0,-2.9,1.425),(5.6,.15,2.85),'wall','C_static',tile=1.15)
cube('WindowWallLeft',(-2.36,2.9,1.425),(.88,.15,2.85),'wall','C_static',tile=1.15)
cube('WindowWallRight',(1.56,2.9,1.425),(2.48,.15,2.85),'wall','C_static',tile=1.15)
cube('BelowWindow',(-.8,2.9,.48),(2.24,.15,.96),'wall','C_static',tile=1.15)
cube('AboveWindow',(-.8,2.9,2.75),(2.24,.15,.20),'wall','C_static',tile=1.15)
for x in [-2.7,2.7]:
    cube('Skirting',(x,0,.105),(.055,5.8,.21),'darkwood','Detail',tile=.8)
    cube('Cornice',(x,0,2.72),(.09,5.8,.10),'darkwood','Detail',tile=.8)
for y in [-2.79,2.79]:
    cube('Skirting',(0,y,.105),(5.4,.055,.21),'darkwood','Detail',tile=.8)
    cube('Cornice',(0,y,2.72),(5.4,.09,.10),'darkwood','Detail',tile=.8)

# Deep wooden window, four panes, outside gray daylight.
for x in [-1.96,.36]: cube('WindowJamb',(x,2.78,1.80),(.12,.19,1.78),'darkwood','Detail',bevel=.01,tile=.7)
for z in [.94,2.64]: cube('WindowRail',(-.8,2.78,z),(2.43,.19,.12),'darkwood','Detail',bevel=.008,tile=.7)
cube('Sill',(-.8,2.64,.92),(2.6,.43,.10),'wood','Detail',bevel=.018,tile=.8)
cube('Mullion',(-.80,2.76,1.8),(.055,.10,1.65),'paint','Detail',tile=.7)
cube('Crossbar',(-.8,2.76,1.65),(2.18,.10,.055),'paint','Detail',tile=.7)
front_panel('RainGlass',-.8,2.83,1.8,2.18,1.62,'glass','Glass')
beam('CurtainPole',(-2.31,2.52,2.69),(.72,2.52,2.69),.025,'brass')
for x in [-2.27,.67]:beam('CurtainBracket',(x,2.823,2.69),(x,2.52,2.69),.012,'brass')
for x in [-2.06,.41]:
    vs=[]; uvs=[]; cols=6
    for row in range(3):
        for col in range(cols+1):
            xx=x+(col/cols-.5)*(.38 if x>0 else .46); yy=2.52+math.sin(col/cols*math.pi*6)*.045
            zz=1.015+row/2*1.615+(.015*math.sin(col*1.7) if row==0 else 0)
            vs.append((xx,yy,zz)); uvs.append((col/cols,row/2*2))
    faces=[]
    for row in range(2):
        for col in range(cols):
            i=row*(cols+1)+col; faces.append((i,i+1,i+cols+2,i+cols+1))
    mesh('Curtain',vs,faces,'curtain','Detail',uvs)
    # Six flat fabric loops hang over the pole, clear of sill and wooden jambs.
    for offset in [-.1533,0,.1533]:
        points=[(2.485,2.62),(2.485,2.69),(2.50,2.716),(2.54,2.716),(2.555,2.69),(2.555,2.62)]
        v=[(x+offset+side,y,z) for y,z in points for side in [-.0175,.0175]]
        mesh('CurtainLoop',v,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(points)-1)],'curtain')

# Closed door near the entry camera. Handle is on the room side.
cube('Door',(-1.75,-2.78,1.1),(.88,.08,2.2),'door','I_door',bevel=.008,tile=.7)
for x in [-2.23,-1.27]: cube('DoorTrim',(x,-2.70,1.14),(.08,.10,2.28),'darkwood','Detail',tile=.7)
cube('DoorTrim',(-1.75,-2.70,2.27),(1.03,.10,.09),'darkwood','Detail',tile=.7)
for z in [.65,1.64]:
    cube('DoorInset',(-1.75,-2.72,z),(.69,.028,.70),'darkwood','I_door',bevel=.007,tile=.75)
    cube('DoorRaisedPanel',(-1.75,-2.698,z),(.61,.025,.62),'door','I_door',bevel=.008,tile=.75)
beam('DoorHandle',(-1.39,-2.64,1.0),(-1.39,-2.57,1.0),.025,'brass','I_door')
beam('DoorLever',(-1.39,-2.57,1),(-1.52,-2.57,1),.018,'brass','I_door')

# Desk, chamfered overhang, drawer pedestal, legs and modest hardware.
cube('DeskTop',(-.83,2.12,.77),(2.1,.78,.085),'wood','I_desk',bevel=.018,tile=.75)
cube('DeskApron',(-.83,2.38,.66),(2.00,.08,.17),'darkwood','I_desk',tile=.7)
cube('DrawerPedestal',(-1.59,2.14,.36375),(.46,.65,.7275),'wood','I_desk',bevel=.01,tile=.7)
for z in [.16,.38,.60]:
    cube('DrawerFront',(-1.59,1.804,z),(.43,.035,.20),'wood','I_desk',bevel=.005,tile=.6)
    beam('DrawerPull',(-1.69,1.77,z),(-1.49,1.77,z),.012,'brass')
    for x in [-1.69,-1.49]:beam('DrawerPullMount',(x,1.77,z),(x,1.79,z),.005,'brass')
for x in [.05]:
    for y in [1.84,2.39]: cube('DeskLeg',(x,y,.36375),(.075,.075,.7275),'wood','I_desk',bevel=.008,tile=.65)
cube('DeskBrace',(-.68,2.40,.20),(1.5,.06,.09),'darkwood','I_desk',tile=.7)

# CRT: tapered case, bevelled bezel, inset curved face, back vents, base.
cx,cy=-.85,2.20
cube('CRTStand',(cx,cy,.8475),(.31,.30,.07),'ivory','I_pc',bevel=.025,tile=.6)
cube('CRTNeck',(cx,cy,.92),(.17,.18,.14),'ivory','I_pc',bevel=.025,tile=.5)
# Front near viewer y=1.91, rear narrows towards window.
verts=[(cx+x,cy+y,z) for y,w,z0,z1 in [(-.25,.50,.93,1.39),(.28,.33,.99,1.32)] for x,z in [(-w/2,z0),(w/2,z0),(w/2,z1),(-w/2,z1)]]
case=mesh('CRTCase',verts,[(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(3,2,6,7),(4,5,1,0)],'ivory','I_pc')
# Vents belong to the actual tapered side: paint its existing face, no slat meshes.
case.data.materials.append(mats['crt_side'])
side=case.data.polygons[1];side.material_index=1
for li,uv in zip(side.loop_indices,[(0,0),(1,0),(1,1),(0,1)]):case.data.uv_layers.active.data[li].uv=uv
cube('CRTBezel',(cx,cy-.26,1.16),(.52,.055,.48),'ivory','I_pc',bevel=.025,tile=.65)
cube('CRTScreenRecess',(cx,cy-.294,1.19),(.413,.014,.326),'metal','I_pc',bevel=.022,tile=.5)
front_panel('CRTScreen',cx,cy-.304,1.19,.382,.292,'screen','I_pc')
for x in [-.16,-.12,.12,.16]:
    o=cyl('CRTButton',(cx+x,cy-.303,.968),.012,.009,'metal','I_pc',verts=8); o.rotation_euler.x=math.pi/2
cube('Tower',(-1.31,2.30,.9875),(.22,.41,.35),'ivory','I_pc',bevel=.013,tile=.65)
cube('CDDrive',(-1.31,2.091,1.0815),(.17,.008,.028),'metal','I_pc',tile=.5)
make_keyboard()
for o in hero_families['keyboard']:o.location.z-=.008
cube('MousePad',(-.33,1.85,.8165),(.22,.22,.008),'denim','I_pc',tile=.4)
o=cube('Mouse',(-.33,1.86,.838),(.055,.09,.035),'ivory','I_pc',bevel=.017,tile=.3)
curve_seam('MouseCord',[(-.33,1.903,.836),(-.32,1.93,.818),(-.30,2.05,.8155),(-.34,2.26,.8155),(-.40,2.43,.8155),(-1.12,2.47,.8155),(-1.205,2.47,.84)],.003,'metal')
curve_seam('KeyboardCord',[(-.79,1.928,.832),(-1.07,2.00,.8155),(-1.07,2.40,.8155),(-1.205,2.46,.845)],.003,'metal')

# Slatted chair with tapered legs and a slightly tilted back.
for x in [-1.08,-.66]:
    for y in [1.05,1.46]:
        beam('ChairLeg',(x+(x+.87)*.15,y-.035,.025),(x,y,.47),.027,'darkwood','C_static',r2=.037)
cube('ChairSeat',(-.87,1.255,.47),(.51,.51,.055),'wood','C_static',bevel=.02,tile=.55)
for x in [-1.08,-.66]: beam('BackUpright',(x,1.04,.49),(x,1.0,1.06),.026,'wood','C_static')
for x in [-1.00,-.87,-.74]: cube('BackSlat',(x,1.02,.80),(.065,.035,.45),'wood','C_static',bevel=.004,tile=.7)
cube('ChairTopRail',(-.87,1.0,1.06),(.50,.06,.075),'wood','C_static',bevel=.012,tile=.7)
beam('ChairStretcher',(-1.08,1.05,.20),(-.66,1.05,.20),.017,'darkwood','C_static')

# Bed: low frame, headboard panels, compressed mattress, irregular cloth.
cube('BedFrame',(1.77,.72,.215),(1.44,2.25,.23),'darkwood','I_bed',bevel=.012,tile=.8)
for x in [1.12,2.42]:
    for y in [-.30,1.75]: cube('BedLeg',(x,y,.17),(.10,.10,.34),'wood','I_bed',bevel=.008,tile=.7)
mattress=cube('Mattress',(1.77,.72,.45),(1.39,2.17,.24),'linen','I_bed',bevel=.065,tile=.7)
cube('Headboard',(1.77,1.87,.73),(1.48,.12,1.15),'wood','I_bed',bevel=.015,tile=.8)
for x in [1.12,2.42]:
    cube('BedPost',(x,1.87,.715),(.10,.15,1.43),'darkwood','I_bed',bevel=.015,tile=.8)
for x in [1.40,1.77,2.14]: cube('HeadboardPanel',(x,1.793,.84),(.29,.025,.57),'darkwood','I_bed',bevel=.005,tile=.6)
# Low-poly cloth with a soft cross-section, irregular hem and long diagonal folds.
cols,rows=8,9
vs=[]; uv=[]
for j in range(rows+1):
    v=j/rows
    for i in range(cols+1):
        u=i/cols; edge=min(u,1-u)
        # Keep the descending hem outside the mattress until it is above its bevel.
        if i==0: x,cross_z=1.025,.25
        elif i==1: x,cross_z=1.035,.50
        elif i==2: x,cross_z=1.085,.584
        elif i==cols: x,cross_z=2.515,.25
        elif i==cols-1: x,cross_z=2.505,.50
        elif i==cols-2: x,cross_z=2.455,.584
        else: x,cross_z=1.215+(i-3)/(cols-6)*1.11,.584
        x+=.006*math.sin(v*20+u*6)
        ymax=1.16+.07*math.sin(u*math.pi*3+.3)+.025*math.cos(u*11)
        if j==0: y,foot_z=-.45,.25
        elif j==1: y,foot_z=-.44,.50
        elif j==2: y,foot_z=-.37,.584
        else: y,foot_z=-.26+(j-3)/(rows-3)*(ymax+.26),.584
        z=min(cross_z,foot_z)
        z+=.006*math.sin(u*29+v*11)*math.sin(v*13-u*8)
        z+=.018*math.exp(-((v-.39-.08*math.sin(u*6))/.11)**2)*math.sin(math.pi*u)
        z+=.015*math.exp(-((v-.90)/.09)**2)*(1-.35*math.cos(u*17))
        vs.append((x,y,z)); uv.append((u,v))
fs=[]
for j in range(rows):
    for i in range(cols):
        a=j*(cols+1)+i; fs.extend([(a,a+1,a+cols+2),(a,a+cols+2,a+cols+1)])
quilt=mesh('RumpledQuilt',vs,fs,'quilt','I_bed',uv)
for poly in quilt.data.polygons: poly.use_smooth=False
mod=quilt.modifiers.new('Cloth thickness','SOLIDIFY'); mod.thickness=.006
bpy.context.view_layer.objects.active=quilt; quilt.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)

def pillow(x,y,rotation):
    verts=[]; tex=[]; faces=[]; nx,ny=4,2
    for side in [1,-1]:
        for j in range(ny+1):
            v=j/ny*2-1
            for i in range(nx+1):
                u=i/nx*2-1; pinch=1-.10*abs(u*v)**3
                z=.657+side*(.065*(1-abs(u)**2.8)*(1-abs(v)**2.8)+.007)
                z+=.004*math.sin(u*16+v*5)*(1-abs(v))*(1-abs(u))
                verts.append((u*.285*pinch,v*.22*pinch,z)); tex.append(((u+1)/2,(v+1)/2))
    count=(nx+1)*(ny+1)
    for side in range(2):
        for j in range(ny):
            for i in range(nx):
                a=side*count+j*(nx+1)+i
                f=(a,a+1,a+nx+2,a+nx+1)
                faces.append(f if side==0 else tuple(reversed(f)))
    border=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
    for i,a in enumerate(border):
        b=border[(i+1)%len(border)]; faces.append((a,a+count,b+count,b))
    o=mesh('SoftPillow',verts,faces,'pillow_linen','I_bed',tex); o.location=(x,y,-.0145); o.rotation_euler.z=rotation
    for poly in o.data.polygons: poly.use_smooth=False
    # Perimeter stitches are baked in pillow_linen, no subpixel piping mesh.
pillow(1.49,1.52,.13); pillow(2.04,1.51,-.10)
cube('BedsideCabinet',(.64,1.83,.28625),(.62,.55,.5725),'wood','C_static',bevel=.01,tile=.7)
cube('BedsideTop',(.64,1.83,.60),(.68,.61,.055),'wood','C_static',bevel=.012,tile=.7)
cube('BedsideDrawer',(.64,1.5425,.43),(.55,.025,.20),'darkwood','Detail',bevel=.005,tile=.7)
beam('BedsidePull',(.57,1.523,.44),(.71,1.523,.44),.01,'brass')

# Warm lamp with a real shade opening and dark metal stem.
lamp_before=set(bpy.context.scene.objects)
cyl('LampFoot',(.69,1.89,.658),.12,.045,'brass',verts=8)
beam('LampStem',(.69,1.89,.68),(.69,1.89,.96),.019,'metal')
vs=[]; uv=[]; n=8
for z,r in [(.90,.20),(1.19,.105)]:
    for i in range(n+1):
        a=i/n*math.tau; vs.append((.69+r*math.cos(a),1.89+r*math.sin(a),z)); uv.append((i/n,z*2))
mesh('PleatedShade',vs,[(i,i+1,i+n+2,i+n+1) for i in range(n)],'shade','Shade',uv)
for z,r in [(.90,.20),(1.19,.105)]:
    for i in range(n):
        a=i/n*math.tau; b=(i+1)/n*math.tau
        beam('ShadeRim',(.69+r*math.cos(a),1.89+r*math.sin(a),z),(.69+r*math.cos(b),1.89+r*math.sin(b),z),.004,'brass','Shade')

for o in set(bpy.context.scene.objects)-lamp_before:o.location.z-=.008

# Bookshelf facing inward from the left wall, varied spines, small boxes.
cube('ShelfBack',(-2.60,.97,1.11),(.08,1.38,2.18),'darkwood','C_static',tile=.7)
for y in [.25,1.69]: cube('ShelfSide',(-2.40,y,1.11),(.46,.065,2.22),'wood','C_static',bevel=.008,tile=.8)
for z in [.12,.53,.94,1.35,1.76,2.21]: cube('Shelf',(-2.40,.97,z),(.46,1.50,.06),'wood','C_static',bevel=.006,tile=.8)
bookcolors=['denim','darkwood','fabric','wood','paper','metal']
for row,z in enumerate([.16,.57,.98,1.39,1.80]):
    y=.33
    while y<1.57:
        width=rng.uniform(.035,.09); h=rng.uniform(.22,.34)
        o=cube('BookSpine',(-2.28,y+width/2,z+h/2-.01),(.23,width,h),rng.choice(bookcolors),'Detail',bevel=.002,tile=.38)
        color_index=bookcolors.index(o.data.materials[0].name)
        o.data.materials.append(mats['bookspines'])
        # Drop shelf-hidden back and bottom; keep top and both depth sides.
        keep=[p for p in o.data.polygons if p.normal.x>-.9 and p.normal.z>-.9]
        vertices=[tuple(v.co) for v in o.data.vertices]
        reduced=bpy.data.meshes.new('BookSpineVisibleFaces')
        reduced.from_pydata(vertices,[],[tuple(p.vertices) for p in keep]);reduced.update()
        original_uv=o.data.uv_layers.active
        reduced_uv=reduced.uv_layers.new(name='UVMap')
        for target,source in zip(reduced.polygons,keep):
            target.material_index=1 if source.normal.x>.9 else 0
            for new_loop,old_loop in zip(target.loop_indices,source.loop_indices):
                co=reduced.vertices[reduced.loops[new_loop].vertex_index].co
                reduced_uv.data[new_loop].uv=((color_index+co.y/width+.5)/6,co.z/h+.5) if target.material_index==1 else original_uv.data[old_loop].uv
        old_materials=list(o.data.materials);o.data=reduced
        for material in old_materials:o.data.materials.append(material)
        y+=width+.007

book_stacks=[]
def book_stack(x,y,z,n=5):
    stack=[]
    for i in range(n):
        width=.26+rng.uniform(-.03,.03)
        o=cube('BookStack',(x,y,z+.0125+i*.025),(width,.19,.025),bookcolors[i%len(bookcolors)],tile=.4)
        o.rotation_euler.z=rng.uniform(-.09,.09)
        bpy.context.view_layer.update()
        # Page edge follows the same transform as its cover, and is flush to it.
        page=front_panel('BookPages',0,-.0952,0,width-.025,.014,'paper')
        page.matrix_world=o.matrix_world.copy()
        stack.append(o)
    book_stacks.append(stack)
book_stack(-1.60,2.22,.8125,5);book_stack(.49,1.65,.6275,3)
for i in range(7):
    z=.8125+.006+i*.012
    cube('CDCase',(-.11,2.30,z),(.15,.15,.012),['metal','ivory','denim','wood'][i%4],tile=.3)
    front_panel('CDLabel',-.11,2.2248,z,.12,.007,'paper')

# Hollow ceramic mug and shaped handle.
make_mug()
for o in hero_families['mug']:o.location.z-=.0085

# Open agenda on the desk, pencil and postcards taped to wallpaper.
cube('Notebook',(-1.45,1.87,.8215),(.27,.21,.018),'paper','I_desk',tile=.4)
mesh('AgendaPage',[(-1.575,1.77,.8307),(-1.325,1.77,.8307),(-1.325,1.97,.8307),(-1.575,1.97,.8307)],[(0,1,2,3)],'notebook','I_desk',[(0,0),(1,0),(1,1),(0,1)])
beam('Pencil',(-1.24,1.77,.8165),(-1.28,1.94,.8165),.004,'wood')
front_panel('Poster',1.54,2.807,1.99,.55,.74,'poster')
front_panel('PosterSmall',2.18,2.807,1.86,.38,.51,'poster2')
for x,z in [(1.31,2.34),(1.77,2.34),(2.03,2.10),(2.32,2.10)]: cube('Tape',(x,2.798,z),(.07,.003,.025),'paper',tile=.3)
cube('Rug',(.10,-.28,.006),(2.66,2.87,.012),'rug',tile=2.85)

# User requested a bare chair. No garment geometry is constructed.
chair_parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(n in o.name for n in ['ChairLeg','ChairSeat','BackUpright','BackSlat','ChairTopRail','ChairStretcher'])]
bpy.context.view_layer.update()
chair_floor=min((o.matrix_world@v.co).z for o in chair_parts for v in o.data.vertices)
for o in chair_parts:o['hero_family']='chair';o.location.z-=chair_floor

def world_bvh(objects):
    verts=[]; faces=[]
    for obj in objects:
        offset=len(verts); verts.extend([obj.matrix_world@v.co for v in obj.data.vertices])
        faces.extend([tuple(offset+i for i in p.vertices) for p in obj.data.polygons])
    return BVHTree.FromPolygons(verts,faces,all_triangles=False)
bpy.context.view_layer.update()
quilt_overlaps=world_bvh([quilt]).overlap(world_bvh([mattress]))
assert not quilt_overlaps,f'Quilt intersects mattress: {len(quilt_overlaps)} triangle pairs'
print('QUILT / MATTRESS: zero mesh intersections')

# A low dresser on the near right wall, with a radio and pinned photos above it.
cube('Dresser',(2.44,-1.08,.42625),(.49,1.20,.8525),'wood','C_static',bevel=.015,tile=.7)
cube('DresserTop',(2.44,-1.08,.88),(.55,1.27,.055),'wood','C_static',bevel=.012,tile=.7)
for z in [.18,.43,.68]:
    cube('DresserDrawer',(2.183,-1.08,z),(.025,1.12,.22),'darkwood',bevel=.004,tile=.7)
    for y in [-1.34,-.82]:
        beam('DresserPull',(2.15,y-.06,z),(2.15,y+.06,z),.012,'brass')
        for yy in [y-.06,y+.06]:
            mesh('DresserPullMount',[(2.15,yy-.004,z),(2.174,yy-.004,z),(2.174,yy+.004,z),(2.15,yy+.004,z)],[(0,1,2,3)],'brass')
cube('Radio',(2.42,-1.16,1.0075),(.23,.37,.20),'darkwood',bevel=.024,tile=.4)
cube('RadioSpeaker',(2.3025,-1.22,1.0175),(.005,.18,.13),'fabric',tile=.2)
beam('RadioAntenna',(2.44,-1.15,1.1075),(2.44,-1.26,1.3875),.003,'metal')
book_stack(2.38,-.70,.9075,3)
for y,z,w,h,mat in [(-.85,1.67,.40,.56,'poster2'),(-1.36,1.81,.27,.36,'poster'),(-1.33,1.36,.25,.19,'book')]:
    p=front_panel('WallPicture',0,0,0,w,h,mat)
    p.rotation_euler.z=-math.pi/2
    p.location=(2.718,y,z)

# Everyday clutter: school bag, old cassette, cable and wastebasket.
make_bag()
cube('Cassette',(-1.40,-.80,.007),(.105,.067,.014),'metal',bevel=.004,tile=.2)
cube('CassetteLabel',(-1.40,-.80,.015),(.075,.038,.002),'paper',tile=.2)
cyl('Wastebasket',(-2.06,1.97,.17),.13,.34,'metal','C_static',verts=10,r2=.17,cap=False)
cyl('WastebasketDark',(-2.06,1.97,.285),.16,.005,'darkwood',verts=10)
for i in range(5):
    a=i/5*math.tau
    o=mesh('DiscardedPaper',[(-.024,-.021,0),(0,-.021,.012),(.024,-.021,.002),(-.024,.021,0),(0,.021,.012),(.024,.021,.002)],[(0,1,4,3),(1,2,5,4)],'paper')
    o.location=(-2.06+math.cos(a)*.075,1.97+math.sin(a)*.075,.2875)
    o.rotation_euler.z=rng.uniform(0,6)

# Personal details, with no imposed character biography.
# Small leaning frame with a rear prop and a real tabletop contact.
photo_before=set(bpy.context.scene.objects)
frame=cube('PhotoFrame',(0,0,.085),(.15,.014,.17),'darkwood',tile=.3)
picture=front_panel('PhotoImage',0,-.0072,.085,.13,.15,'photo')
bpy.context.view_layer.update()
pose=Matrix.Translation((.39,1.99,.6275+.007*math.sin(math.radians(12))))@Matrix.Rotation(math.radians(-12),4,'X')
for o in [frame,picture]:o.matrix_world=pose@o.matrix_world
beam('PhotoRearStand',pose@Vector((0,.007,.10)),(.39,2.075,.6335),.003,'darkwood')
cube('PhotoStandFoot',(.39,2.075,.6305),(.055,.045,.006),'darkwood',tile=.3)
for o in set(bpy.context.scene.objects)-photo_before:o['review_family']='photo_frame' 
front_panel('PinnedPhoto',.85,2.805,1.70,.18,.21,'photo')
cube('PhotoTape',(.85,2.798,1.806),(.075,.005,.024),'paper',tile=.3)
cube('MixtapeOnDesk',(-1.48,1.92,.8395),(.11,.075,.018),'metal','I_desk',bevel=.004,tile=.2)
mesh('MixtapeLabel',[(-1.526,1.889,.8487),(-1.434,1.889,.8487),(-1.434,1.951,.8487),(-1.526,1.951,.8487)],[(0,1,2,3)],'mixtape','I_desk',[(0,0),(1,0),(1,1),(0,1)])
# Headphones lie on the upper book: both cushions have a measured support.
headphones_before=set(bpy.context.scene.objects)
for i in range(9):
    a=math.pi*i/9;b=math.pi*(i+1)/9
    beam('HeadphoneBand',(-1.6+.075*math.cos(a),2.205+.073*math.sin(a),.956),(-1.6+.075*math.cos(b),2.205+.073*math.sin(b),.956),.008,'metal')
for x in [-1.675,-1.525]:cyl('HeadphoneCushion',(x,2.205,.951),.038,.027,'denim',verts=8)
curve_seam('HeadphoneCable',[(-1.675,2.18,.951),(-1.71,2.14,.941),(-1.76,2.105,.941),(-1.78,2.08,.8155),(-1.69,2.05,.8155)],.003,'metal')
for o in set(bpy.context.scene.objects)-headphones_before:o['review_family']='headphones'
for o in bpy.context.scene.objects:
    if o.get('group')=='I_pc' and 'Keyboard' not in o.name and not o.get('hero_family'):o['review_family']='computer'

# Layout: headboard and bedside against the rear skirting, no empty alcove.
# Move complete assemblies, including cloth, books, frame, lamp and their support.
bpy.context.view_layer.update()
for o in bpy.context.scene.objects:
    if o.type!='MESH':continue
    if o.get('group')=='I_bed':o.location+=Vector((.15,.805,0))
    elif any(token in o.name for token in ['Bedside','LampFoot','LampStem','PleatedShade','ShadeRim','PhotoFrame','PhotoImage','PhotoRearStand','PhotoStandFoot']):o.location+=Vector((.15,.615,0))
# Book/page pairing uses the same object index order as its stack.
for o in book_stacks[1]:o.location+=Vector((.15,.615,0))
for o in bpy.context.scene.objects:
    if 'BookPages' in o.name and .30<o.matrix_world.translation.x<.70:o.location+=Vector((.15,.615,0))
for o in bpy.context.scene.objects:
    if o.get('hero_family')=='bag':o.location.z-=.0068
bpy.context.view_layer.update()
# The pencil lies directly on the desk, using its actual faceted lower surface.
pencil=next(o for o in bpy.context.scene.objects if 'Pencil' in o.name)
pencil.location.z+=.8125-min((pencil.matrix_world@v.co).z for v in pencil.data.vertices)

# Exterior, forest and materials retained from V0.13.
(ROOT/'verification').mkdir(exist_ok=True)
exec(compile((Path(__file__).parent/'build_forest.py').read_text(encoding='utf-8'),'build_forest.py','exec'))

(ROOT/'verification').mkdir(exist_ok=True)
(ROOT/'verification/model_checks.json').write_text(json.dumps({'jacket_removed':True,'quilt_mattress_triangle_intersections':len(quilt_overlaps),'chair_pieces':len(chair_parts),'nearest_tree_distance_from_window_m':min(tree_distances),'quilt_grid':[cols+1,rows+1]},indent=2))

if snapshot_path:=os.environ.get('LHC_ASSEMBLY_SNAPSHOT'):
    Path(snapshot_path).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=snapshot_path)
exec(compile((Path(__file__).parent/'contact_checks.py').read_text(encoding='utf-8'),'contact_checks.py','exec'))
exec(compile((Path(__file__).parent/'asset_geometry_checks.py').read_text(encoding='utf-8'),'asset_geometry_checks.py','exec'))
exec(compile((Path(__file__).parent/'export_room.py').read_text(encoding='utf-8'),'export_room.py','exec'))
