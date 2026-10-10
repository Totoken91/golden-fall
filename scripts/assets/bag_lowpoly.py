"""Low-poly satchel: flap follows the actual body facets instead of cutting them."""
def make_bag():
    before=set(bpy.context.scene.objects)
    cx,cy=-1.85,-1.03;n=8;vs=[];uv=[];fs=[]
    profile=[(.008,.14,.09),(.04,.19,.125),(.20,.205,.135),(.36,.19,.12),(.44,.15,.10),(.46,.08,.06)]
    for j,(z,rx,ry) in enumerate(profile):
        for i in range(n):
            a=i/n*math.tau;c=math.cos(a);s=math.sin(a)
            xx=rx*math.copysign(abs(c)**.55,c);yy=ry*math.copysign(abs(s)**.65,s)
            vs.append((cx+xx,cy+yy,z));uv.append((i/n,j/5))
    for j in range(5):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    fs.extend([tuple(reversed(range(n))),tuple(5*n+i for i in range(n))])
    body=mesh('CanvasSatchel',vs,fs,'canvas','C_static',uv)
    for p in body.data.polygons:p.use_smooth=False
    body.data.calc_loop_triangles()
    # Intersect a convex flap pattern with the body front's actual triangles.
    # Coarser facets require 18 mm forward offset so the 3 mm lining also clears
    # the steep shoulders (normal.y may be only -.25). Check all three assemblies.
    mask=[(cx-.148,.405),(cx+.148,.405),(cx+.16,.26),(cx+.125,.245),(cx-.125,.245),(cx-.16,.26)]
    mask.reverse()
    def side(p,a,b):return (b[0]-a[0])*(p.z-a[1])-(b[1]-a[1])*(p.x-a[0])
    def clip(poly,a,b):
        result=[]
        for i,p in enumerate(poly):
            q=poly[(i+1)%len(poly)];dp,dq=side(p,a,b),side(q,a,b)
            if dp>=-1e-9:result.append(p)
            if (dp>0) != (dq>0) and abs(dp-dq)>1e-12:result.append(p+(q-p)*(dp/(dp-dq)))
        return result
    fv=[];fu=[];ff=[];lookup={}
    for tri in body.data.loop_triangles:
        if tri.normal.y>-.25:continue
        poly=[body.data.vertices[i].co.copy() for i in tri.vertices]
        for i,a in enumerate(mask):
            if not poly:break
            poly=clip(poly,a,mask[(i+1)%len(mask)])
        if len(poly)<3:continue
        indices=[]
        for p in poly:
            p.y-=.018;key=tuple(round(v,7) for v in p)
            if key not in lookup:
                lookup[key]=len(fv);fv.append(p);fu.append(((p.x-(cx-.17))/.34,(p.z-.235)/.18))
            if not indices or indices[-1]!=lookup[key]:indices.append(lookup[key])
        if len(set(indices))>=3:ff.append(tuple(indices))
    flap=cloth_finish(mesh('ConformingSatchelFlap',fv,ff,'bag_flap','Detail',fu),.003)
    # The strap is a flat belt: its floor section stays horizontal, not a tube
    # or a twisting ribbon penetrating the floor. Endpoints sit outside the sides.
    pts=[(cx-.206,cy+.01,.34),(cx-.27,cy-.04,.29),(cx-.31,cy-.12,.12),(cx-.29,cy-.20,.007),(cx-.17,cy-.26,.007),(cx+.06,cy-.26,.007),(cx+.25,cy-.17,.11),(cx+.206,cy+.01,.34)]
    sv=[];su=[]
    for j,p in enumerate(pts):
        sv.extend([Vector(p)+Vector((0,-.015,0)),Vector(p)+Vector((0,.015,0))]);su.extend([(0,j*.2),(1,j*.2)])
    strap=cloth_finish(mesh('BagShoulderStrap',sv,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(pts)-1)],'leather','Detail',su),.003)
    remember('bag',before)
    return body,flap,strap
