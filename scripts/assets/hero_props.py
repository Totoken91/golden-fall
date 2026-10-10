"""Low-poly props; executed in build_room.py's Blender context.

Coordinates in metres, Z up. No jacket: the user requested a bare chair.
"""
hero_families={}

def remember(family,before):
    items=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in before]
    for o in items:o['hero_family']=family
    hero_families.setdefault(family,[]).extend(items)
    return items

def cloth_finish(o,thickness=.003):
    for p in o.data.polygons:p.use_smooth=False
    bpy.context.view_layer.objects.active=o
    mod=o.modifiers.new('Bound cloth thickness','SOLIDIFY'); mod.thickness=thickness
    mod.material_offset=1
    o.data.materials.append(mats['lining'])
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return o

def curve_seam(name,points,r=.0015,material='stitch',tag='Cloth'):
    # Subpixel stitches use ribbons; exposed cables/handles use four-sided tubes.
    if len(points)>7:points=[points[round(i*(len(points)-1)/6)] for i in range(7)]
    flat=r<.0025; n=2 if flat else 4;verts=[];faces=[]
    for j,p in enumerate(points):
        tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
        tangent.normalize();right=tangent.cross(Vector((0,1,0)))
        if right.length<.01:right=tangent.cross(Vector((1,0,0)))
        right.normalize();up=tangent.cross(right).normalized()
        if flat:verts.extend([Vector(p)-r*right,Vector(p)+r*right])
        else:
            for i in range(n):verts.append(Vector(p)+r*(math.cos(i/n*math.tau)*right+math.sin(i/n*math.tau)*up))
    for j in range(len(points)-1):
        if flat:faces.append((j*2,j*2+1,j*2+3,j*2+2))
        else:
            for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    return mesh(name,verts,faces,material,tag)

def make_keyboard():
    before=set(bpy.context.scene.objects)
    cx,cy=-.79,1.83
    cube('KeyboardLowerCase',(cx,cy,.835),(.515,.195,.029),'ivory','I_pc',bevel=.009,tile=.6)
    cube('KeyboardDarkWell',(cx,cy+.011,.851),(.487,.161,.008),'metal','I_pc',bevel=.004,tile=.4)
    def key(x,y,w=.022,h=.023,mat='keycaps'):
        z=.855+.016*(y-(cy-.08));vs=[]
        for zz,inset in [(z,0),(z+.014,.002)]:
            vs.extend([(x-w/2+inset,y-h/2+inset,zz),(x+w/2-inset,y-h/2+inset,zz),(x+w/2-inset,y+h/2-inset,zz),(x-w/2+inset,y+h/2-inset,zz)])
        return mesh('IndividualKey',vs,[(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,'I_pc')
    # Full-size 2003 layout: function row, alphanumeric block, arrows and number pad.
    for row in range(5):
        for col in range(13):
            x=cx-.226+col*.024;y=cy+.071-row*.030
            if row==0 and col in [1,5,9]:continue
            if row==4 and col in range(2,9):continue
            key(x,y,.021,.018 if row==0 else .024,'keycaps' if col not in [0,12] else 'ivory')
    key(cx-.106,cy-.049,.163,.024)
    for row in range(5):
        for col in range(3):key(cx+.166+col*.024,cy+.071-row*.030,.021,.018 if row==0 else .024)
    for x in [cx+.102,cx+.126]:
        for y in [cy-.019,cy-.049]:key(x,y,.019,.024)
    for x in [cx+.171,cx+.195,cx+.219]:
        mesh('KeyboardStatusLED',[(x-.002,cy+.087,.855),(x+.002,cy+.087,.855),(x+.002,cy+.089,.855),(x-.002,cy+.089,.855)],[(0,1,2,3)],'paint')
    # Cord enters the casing rather than terminating at the centre of the keys.
    curve_seam('KeyboardCord',[(cx+.17,cy+.098,.838),(cx+.19,cy+.17,.832),(cx+.16,cy+.25,.832),(cx+.11,cy+.30,.832)],.003,'metal','Detail')
    remember('keyboard',before)

def make_mug():
    before=set(bpy.context.scene.objects)
    x,y=-.05,1.88;n=8;vs=[];uv=[];fs=[]
    profile=[(.031,.821),(.043,.828),(.044,.938),(.039,.946),(.035,.938),(.034,.842)]
    for j,(r,z) in enumerate(profile):
        for i in range(n):
            a=i/n*math.tau;vs.append((x+r*math.cos(a),y+r*math.sin(a),z));uv.append((i/n,j/(len(profile)-1)))
    for j in range(len(profile)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    o=mesh('HollowStonewareMug',vs,fs,'ceramic','Detail',uv)
    for p in o.data.polygons:p.use_smooth=False
    mesh('CoffeeInside',[(x+.034*math.cos(i/n*math.tau),y+.034*math.sin(i/n*math.tau),.928) for i in range(n)],[tuple(range(n))],'coffee')
    pts=[]
    for i in range(7):
        a=-math.pi/2+i/6*math.pi
        pts.append((x+.039+.031*math.cos(a),y,.880+.039*math.sin(a)))
    curve_seam('CeramicHandle',pts,.007,'ceramic','Detail')
    # Ceramic grain is in the texture; no subpixel highlight geometry.
    remember('mug',before)

exec(compile((ROOT/'scripts/assets/bag_lowpoly.py').read_text(encoding='utf-8'),'bag_lowpoly.py','exec'))
