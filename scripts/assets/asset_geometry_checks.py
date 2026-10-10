"""Assembly intersection checks and hard triangle budgets, before export."""
from collections import Counter
def find(part):return [o for o in bpy.context.scene.objects if o.type=='MESH' and part in o.name]
body=find('CanvasSatchel');flap=find('ConformingSatchelFlap');strap=find('BagShoulderStrap')
assert len(body)==len(flap)==len(strap)==1
assert not any('Jacket' in o.name or 'Coat' in o.name or 'Sleeve' in o.name for o in bpy.context.scene.objects), 'A garment remains in the scene'
bpy.context.view_layer.update()
bag_checks={
    'body_flap_intersections':len(world_bvh(body).overlap(world_bvh(flap))),
    'body_strap_intersections':len(world_bvh(body).overlap(world_bvh(strap))),
    'flap_strap_intersections':len(world_bvh(flap).overlap(world_bvh(strap)))
}
assert not any(bag_checks.values()),bag_checks
min_z=min((o.matrix_world@v.co).z for o in body+flap+strap for v in o.data.vertices)
assert min_z>=.0001,('Bag penetrates floor',min_z)
keys=[o for o in bpy.context.scene.objects if o.get('hero_family')=='keyboard' and 'IndividualKey' in o.name]
key_bvhs=[world_bvh([o]) for o in keys]
key_intersections=sum(len(a.overlap(b)) for i,a in enumerate(key_bvhs) for b in key_bvhs[i+1:])
assert key_intersections==0,('Keycaps intersect each other',key_intersections)
groups=Counter();roles=Counter();objects=[]
for o in bpy.context.scene.objects:
    if o.type!='MESH':continue
    o.data.calc_loop_triangles();count=len(o.data.loop_triangles)
    family=o.get('hero_family','');role=o.get('group','Detail')
    if family:groups[family]+=count
    roles[role]+=count;objects.append({'name':o.name,'triangles':count,'family':family,'role':role})
caps={'chair':160,'keyboard':820,'mug':150,'bag':260}
total=sum(roles.values())
report={'triangle_budget':8000,'total_triangles':total,'asset_budgets':caps,'asset_triangles':dict(groups),'role_triangles':dict(roles),'bag_checks':bag_checks,'bag_min_z_m':min_z,'individual_key_intersections':key_intersections,'jacket_removed':True,'objects':sorted(objects,key=lambda o:-o['triangles'])}
(ROOT/'verification/geometry_budget.json').write_text(json.dumps(report,indent=2))
print('BAG CHECKS',bag_checks,'floor clearance',min_z,flush=True)
print('TRIANGLE BUDGET',total,'/ 8000;',dict(groups),flush=True)
report['runtime_rain_triangles']=720
report['total_with_rain_triangles']=total+720
(ROOT/'verification/geometry_budget.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert total+720<=8000,('Scene plus rain exceeds budget',total+720)
for family,cap in caps.items():assert groups[family]<=cap,(family,groups[family],cap)
