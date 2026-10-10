"""Measured support contacts, clearances and disjoint assemblies before joining."""
bpy.context.view_layer.update()
def one(name):
    matches=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.endswith('_'+name)]
    assert len(matches)==1,(name,len(matches))
    return matches[0]
def bounds(objects):
    points=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
    return [min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]
def selected(token):return [o for o in bpy.context.scene.objects if o.type=='MESH' and token in o.name]
contacts=[]
def support(name,items,surface,tolerance=.001,overhang=False):
    lo,hi=bounds(items);a,b=bounds([surface]);gap=lo[2]-b[2]
    within=all(lo[i]>=a[i]-.001 and hi[i]<=b[i]+.001 for i in [0,1])
    if overhang:within=all(a[i]<(lo[i]+hi[i])/2<b[i] for i in [0,1])
    contacts.append({'object':name,'support':surface.name,'gap_m':gap,'footprint_inside_support':within})
    assert abs(gap)<=tolerance,(name,'support gap',gap)
    assert within,(name,'overhangs support',lo,hi,a,b)
desk=one('DeskTop');bedside=one('BedsideTop');dresser=one('DresserTop');floor=one('Floor')
for name,items,surface in [
    ('CRT stand',[one('CRTStand')],desk),('Tower',[one('Tower')],desk),
    ('Keyboard',hero_families['keyboard'],desk),('Mousepad',[one('MousePad')],desk),
    ('Mouse',[one('Mouse')],one('MousePad')),('Mug',hero_families['mug'],desk),
    ('Notebook',[one('Notebook')],desk),('Mixtape',[one('MixtapeOnDesk')],one('Notebook')),
    ('Pencil',[one('Pencil')],desk),('Lamp foot',[one('LampFoot')],bedside),
    ('Photo frame',[one('PhotoFrame')],bedside),('Frame stand',[one('PhotoStandFoot')],bedside),
    ('Radio',[one('Radio')],dresser),('Chair',chair_parts,floor),
    ('Bag',hero_families['bag'],floor),('Cassette',[one('Cassette')],floor),
    ('Rug',[one('Rug')],floor),('Drawer pedestal',[one('DrawerPedestal')],floor),
    ('Desk legs',selected('DeskLeg'),floor),
    ('Dresser',[one('Dresser')],floor),('Bed legs',selected('BedLeg'),floor),
    ('Bed posts',selected('BedPost'),floor),('Bedside cabinet',[one('BedsideCabinet')],floor),
    ('Wastebasket',[one('Wastebasket')],floor)]:support(name,items,surface)
for paper in selected('DiscardedPaper'):support(paper.name,[paper],one('WastebasketDark'))
for book in selected('BookSpine'):
    shelves=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.split('_')[-1].split('.')[0]=='Shelf']
    z=bounds([book])[0][2]
    shelf=min(shelves,key=lambda o:abs(bounds([o])[1][2]-z))
    support(book.name,[book],shelf,overhang=True)
def seated_on(name,upper,lower):
    lo,hi=bounds([upper]);a,b=bounds([lower]);gap=lo[2]-b[2]
    assert abs(gap)<.001,(name,'assembly support gap',gap)
    assert all(min(hi[i],b[i])-max(lo[i],a[i])>0 for i in [0,1]),name
    contacts.append({'object':name,'support':lower.name,'gap_m':gap,'support_area_overlaps':True})
for name,upper,lower in [('Desktop / pedestal',desk,one('DrawerPedestal')),('Bedside lid',bedside,one('BedsideCabinet')),('Dresser lid',dresser,one('Dresser')),('Mattress / bed frame',mattress,one('BedFrame'))]:seated_on(name,upper,lower)
for leg in selected('DeskLeg'):seated_on('Desktop / '+leg.name,desk,leg)
for stack,base in zip(book_stacks,[desk,bedside,dresser]):
    support(stack[0].name,[stack[0]],base)
    for lower,upper in zip(stack,stack[1:]):support(upper.name,[upper],lower,overhang=True)
for cup in selected('HeadphoneCushion'):support(cup.name,[cup],book_stacks[0][-1])
cases=sorted(selected('CDCase'),key=lambda o:o.location.z)
support('CD stack',[cases[0]],desk)
for lower,upper in zip(cases,cases[1:]):support(upper.name,[upper],lower)
clearances=[]
def disjoint(name,a,b):
    count=len(world_bvh(a).overlap(world_bvh(b)));clearances.append({'pair':name,'triangle_intersections':count});assert count==0,(name,count)
curtain=selected('Curtain');wood=selected('Sill')+selected('WindowJamb')+selected('WindowRail')+selected('Mullion')+selected('Crossbar')
disjoint('Curtains / window woodwork',curtain,wood)
disjoint('Curtains / desk',curtain,[o for o in bpy.context.scene.objects if o.get('group')=='I_desk'])
disjoint('Curtains / bedside lamp',curtain,selected('LampFoot')+selected('LampStem')+selected('PleatedShade')+selected('ShadeRim'))
disjoint('Headphone cable / books',selected('HeadphoneCable'),[o for stack in book_stacks for o in stack])
disjoint('Shelf books / shelf sides',selected('BookSpine'),selected('ShelfSide'))
disjoint('Wastebasket paper / basket wall',selected('DiscardedPaper'),[one('Wastebasket')])
disjoint('Bed / bedside', [o for o in bpy.context.scene.objects if o.get('group')=='I_bed'], selected('Bedside'))
disjoint('Lamp / frame',selected('LampFoot')+selected('LampStem')+selected('PleatedShade')+selected('ShadeRim'),selected('PhotoFrame')+selected('PhotoImage')+selected('PhotoRearStand')+selected('PhotoStandFoot'))
disjoint('Headphone cushions / books',selected('HeadphoneCushion'),book_stacks[0][:-1])
disjoint('Pillows / mattress',selected('SoftPillow'),[mattress])
disjoint('Pillows / quilt',selected('SoftPillow'),[quilt])
disjoint('Pillows / headboard',selected('SoftPillow'),selected('Headboard')+selected('BedPost'))
disjoint('Bed / walls',selected('BedPost')+[quilt,mattress],selected('WindowWallRight')+selected('SideWall')+selected('Skirting'))
assert not selected('CRTVent'),'Separate vent slats remain'
assert case.data.polygons[1].material_index==1 and case.data.materials[1].name=='crt_side'
rear={'headboard_post_to_rear_skirting_m':2.7625-bounds(selected('BedPost'))[1][1],'bedside_top_to_rear_wall_m':2.825-bounds([bedside])[1][1]}
assert 0<=rear['headboard_post_to_rear_skirting_m']<=.025,rear
assert 0<=rear['bedside_top_to_rear_wall_m']<=.08,rear
report={'contacts':contacts,'disjoint_checks':clearances,'rear_clearances':rear,'crt_vents':'baked into the existing right shell face; no separate slat geometry','note':'Intentional structural joins and cloth seams are not treated as collisions. Flat contacts allow 1 mm tolerance. Varied book sizes may overhang their support, with the center still supported.'}
(ROOT/'verification/contact_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('CONTACT CHECKS',len(contacts),'supports;',len(clearances),'disjoint assemblies;',rear,flush=True)
