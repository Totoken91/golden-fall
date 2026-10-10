"""Shared bpy stage. The room authoring namespace supplies mesh/beam/front_panel."""
out_rng=random.Random(818313)
verts=[];tex=[];faces=[];nx,ny=4,4
for j in range(ny+1):
    y=3+j*18
    for i in range(nx+1):
        x=-40+i*20;z=-.42-.009*y+.12*math.sin(x*.16+y*.12)
        verts.append((x,y,z));tex.append((x/4,y/4))
for j in range(ny):
    for i in range(nx):
        a=j*(nx+1)+i;faces.extend([(a,a+1,a+nx+2),(a,a+nx+2,a+nx+1)])
mesh('DampGround',verts,faces,'wetsoil','Outside',tex)
for x in range(-12,13,3):
    beam('FencePost',(x,11,-.45),(x+.025,11,.66),.045,'darkwood','Outside',r2=.035)
    if x<12:
        for z in [.1,.48]:beam('FenceRail',(x,11,z),(x+3,11,z-.025),.026,'darkwood','Outside')

tree_distances=[];forest_layers=[]
for layer,(count,near,far,span,minh,maxh) in enumerate([(24,16,25,22,10,15),(32,27,42,33,13,21),(34,43,62,46,17,26)]):
    # Stratified positions avoid the large accidental gaps of uniform random placement.
    for j in range(count):
        x=-span+(j+out_rng.uniform(.1,.9))*2*span/count
        y=out_rng.uniform(near,far);h=out_rng.uniform(minh,maxh)
        tree_distances.append(y-2.9)
        lean=out_rng.uniform(-.5,.5)
        beam('DistantTrunk',(x,y,-.45),(x+lean,y,h*.91),out_rng.uniform(.10,.19),'bark','Outside',r2=.028)
        if (j+layer)%3==0:
            for angle in [0,math.pi/3,2*math.pi/3]:
                p=front_panel('PineBranches',0,0,0,h*out_rng.uniform(.42,.59),h*.96,'pinecard','Foliage')
                p.rotation_euler.z=angle+out_rng.uniform(-.15,.15);p.location=(x+lean*.5,y,h*.45)
        else:
            for k in range(4-layer):
                a=k*2.4+out_rng.random();reach=out_rng.uniform(.8,1.8)
                xx=x+math.cos(a)*reach;yy=y+math.sin(a)*reach;zz=h*(.48+.34*k/(3-layer))+out_rng.uniform(-.3,.3)
                beam('TreeBranch',(x,y,h*.30),(xx,yy,zz),.045,'bark','Outside',r2=.01)
                # Broad, irregular canopy masses extend down through the trunk zone.
                width=out_rng.uniform(4.2,6.3)*(1+layer*.12)
                height=out_rng.uniform(4.4,6.6)*(1+layer*.16)
                for angle in [0,math.pi/2]:
                    p=front_panel('AutumnCrown',0,0,0,width,height,'canopy'+str((j+layer)%3),'Foliage')
                    p.rotation_euler.z=angle+out_rng.uniform(-.4,.4);p.location=(xx,yy,zz)
    forest_layers.append({'trees':count,'depth_range_m':[near,far],'span_m':span*2})
for j in range(28):
    x=out_rng.uniform(-24,24);y=out_rng.uniform(12,35);h=out_rng.uniform(1.2,2.8)
    for angle in [out_rng.uniform(-.4,.4),math.pi/2]:
        p=front_panel('Understorey',0,0,0,out_rng.uniform(2.2,3.8),h,'underbrush','Foliage')
        p.rotation_euler.z=angle;p.location=(x,y,h*.5-.45-.009*y)
# Two almost free silhouette masses close distant gaps without moving foreground trees.
for index,(x,y,w,h) in enumerate([(-9,59,114,25),(12,64,130,29)]):
    front_panel('DistantForestMass',x,y,h*.5-.9,w,h,'treeline'+str(index),'Outside')
front_panel('OvercastSky',0,67,25,170,80,'sky','Sky')
(ROOT/'verification/forest.json').write_text(json.dumps({'trees':90,'layers':forest_layers,'understorey_clusters':28,'distant_mass_planes':2,'sky_planes':1,'nearest_tree_distance_from_window_m':min(tree_distances),'geometry_strategy':'Low-poly trunks and crossed alpha cutout canopies, two distant silhouette cards; no subdivision of room assets.'},indent=2))
