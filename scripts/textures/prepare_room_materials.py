"""Reproducible 128px room materials from official cached maps and existing identity textures.
No network: acquire sources with pipeline.py first. Never overwrite authored textures.
"""
from pathlib import Path
import hashlib,json,math,sys
from PIL import Image,ImageStat
from integration import prepare_texture_import
ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(root=ROOT):
 manifest=json.loads((root/'assets/textures/manifest.json').read_text(encoding='utf-8'))
 assets=manifest['assets']
 selected={v['id']:(k,v) for k,v in assets.items() if v['transformation']['profile_name']=='psx_faceted'}
 for k,v in assets.items():
  if v['transformation']['profile_name']=='furniture_psx':selected[v['id']]=(k,v)
 originals=root/'game/assets/room/textures'
 derived={}
 # Each original texture is an identity layer (colour, seams, patchwork). Material grain is real.
 # UV spans are authored physical estimates for the unique cloth shapes, not new geometry.
 plans={
  'curtain':('rough_linen',[.42,.75],.70),
  'linen':('cotton_jersey',[.7,.7],.65),
  'pillow_linen':('cotton_jersey',[.57,.44],.65),
  'quilt':('cotton_jersey',[1.48,2.32],.48),
  'canvas':('Fabric061',[1.05,.46],.70),
  'bag_flap':('Fabric061',[.34,.18],.55),
  'shade':('rough_linen',[.95,.5],.55),
  'fabric':('Fabric061',[.2,.2],.55),
  'ceiling':('Plaster007',[1.5,1.5],.22),
 }
 for name,(asset_id,span,strength) in plans.items():
  key,entry=selected[asset_id]
  dest=root/'game/assets/textures/room'/name
  dest.mkdir(parents=True,exist_ok=True)
  original=Image.open(originals/(name+'.png')).convert('RGB').resize((128,128),Image.Resampling.LANCZOS)
  tile=entry['tile_m']
  maps={}
  for role,info in entry['optimized_maps'].items():
   source=Image.open(root/info['path']).convert('RGB')
   # Bake physical repetition to a 128px atlas. Downsample only once, with antialiasing.
   repeats=[span[i]/tile[i] for i in range(2)]
   big=Image.new('RGB',(512,512))
   sw,sh=[max(1,round(512/r)) for r in repeats]
   patch=source.resize((sw,sh),Image.Resampling.BICUBIC)
   for y in range(0,512,sh):
    for x in range(0,512,sw):big.paste(patch,(x,y))
   texture=big.resize((128,128),Image.Resampling.LANCZOS)
   if role=='albedo':
    # Neutralize source hue, preserve palette and visible authored stitching/buckles.
    lum=texture.convert('L'); mean=ImageStat.Stat(lum).mean[0]
    pixels=[]
    for old,grain in zip(original.getdata(),lum.getdata()):
     factor=1+strength*(grain/max(mean,1)-1)
     pixels.append(tuple(max(0,min(255,round(c*factor))) for c in old))
    texture=Image.new('RGB',(128,128));texture.putdata(pixels)
   elif role=='normal':
    pixels=[]
    for p in texture.getdata():
     v=[c/127.5-1 for c in p];length=math.sqrt(sum(c*c for c in v)) or 1
     pixels.append(tuple(round((c/length+1)*127.5) for c in v))
    texture.putdata(pixels)
   elif role=='roughness':
    # Cloth and old plaster stay matte. Do not import the gloss of a source blindly.
    texture=texture.convert('L').point(lambda p:max(190,p))
   output=dest/(role+'.png');texture.save(output,optimize=True)
   res='res://'+output.relative_to(root/'game').as_posix()
   prepare_texture_import(output,res,role)
   maps[role]={'path':output.relative_to(root).as_posix(),'sha256':sha(output)}
  refs=[f'[ext_resource type="Texture2D" path="res://{v["path"].removeprefix("game/")}" id="{role}"]' for role,v in maps.items()]
  properties=['resource_name = "'+name+'"','texture_filter = 2','texture_repeat = true',
   'albedo_texture = ExtResource("albedo")','roughness = 1.0','metallic_specular = 0.1',
   'roughness_texture = ExtResource("roughness")','roughness_texture_channel = 0',
   'normal_enabled = true','normal_scale = '+str(.10 if name=='ceiling' else .16),'normal_texture = ExtResource("normal")']
  if 'ao' in maps:properties+=['ao_enabled = true','ao_texture = ExtResource("ao")','ao_texture_channel = 0','ao_light_affect = 0.1']
  path=dest/'material.tres'
  path.write_text('[gd_resource type="StandardMaterial3D" load_steps='+str(len(refs)+1)+' format=3]\n\n'+'\n'.join(refs)+'\n\n[resource]\n'+'\n'.join(properties)+'\n',encoding='utf-8')
  derived[name]={'source_key':key,'source_page':entry['source_page'],'downloaded_component_license':entry['license'],
   'identity_component_license':'Project-authored identity; no new redistribution license asserted',
   'identity_texture':{'path':(originals/(name+'.png')).relative_to(root).as_posix(),'sha256':sha(originals/(name+'.png'))},
   'transformations':{'size':[128,128],'uv_span_estimate_m':span,'source_tile_m':tile,
    'albedo':'source luminance modulates existing palette and identity; source hue neutralized',
   'grain_strength':strength,'normal':'resampled, renormalized','roughness':'clamped to at least 190/255','filter':'nearest with real mipmaps'},
   'maps':maps,'material':{'path':path.relative_to(root).as_posix(),'sha256':sha(path)},'status':'pending_engine_review'}
 bindings=json.loads((root/'game/data/room_materials.json').read_text(encoding='utf-8'))
 rules=[]
 for node in ['Detail_wood','I_desk_wood']:
  rules.append({'node':node,'material_name':'wood','key':selected['wood_table_worn'][0],'metric_wood_uv':True,'tint':[.95,.92,.85],'normal_scale':.12})
 for node in ['C_static_wood','I_bed_wood','Detail_darkwood','I_door_darkwood','I_desk_darkwood','C_static_darkwood','I_bed_darkwood','I_door_door']:
  rules.append({'node':node,'material_name':'door' if node=='I_door_door' else ('darkwood' if 'darkwood' in node else 'wood'),
   'key':selected['wood_table_001'][0],'metric_wood_uv':True,'grain_axis':'v',
   'tint':[.32,.32,.30] if 'darkwood' in node else [.95,.95,.92],'normal_scale':.10})
 for name,node in [('curtain','Detail_curtain'),('linen','I_bed_linen'),('pillow_linen','I_bed_pillow_linen'),('quilt','I_bed_quilt'),('canvas','C_static_canvas'),('bag_flap','Detail_bag_flap'),('shade','Shade_shade'),('fabric','Detail_fabric.001'),('ceiling','C_static_ceiling')]:
  rules.append({'node':node,'material_name':name,'material':'res://assets/textures/room/'+name+'/material.tres','uv_period_m':[1,1],'keep_emission':name=='shade','double_sided':name in ['curtain','shade']})
 rules.append({'node':'C_static_metal','material_name':'metal','key':selected['Metal046B'][0],'uv_period_m':[1,.34],'metallic':.18,'normal_scale':.12,'tint':[.68,.73,.67]})
 bindings['surfaces']=rules
 (root/'game/data/room_materials.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 output={'schema_version':1,'purpose':'128px downloaded material grain, preserving authored identity layers','derivations':derived}
 (root/'assets/textures/room_derived_manifest.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Prepared',len(derived),'identity-preserving material atlases and',len(rules),'targeted surface rules; approved floor binding unchanged.')
def verify(root=ROOT):
 document=json.loads((root/'assets/textures/room_derived_manifest.json').read_text(encoding='utf-8'))
 official=json.loads((root/'assets/textures/manifest.json').read_text(encoding='utf-8'))
 for name,entry in document['derivations'].items():
  assert entry['source_key'] in official['assets'],name
  for item in [entry['identity_texture'],entry['material'],*entry['maps'].values()]:
   path=root/item['path']
   assert path.is_file() and sha(path)==item['sha256'],str(path)
  for item in entry['maps'].values():
   with Image.open(root/item['path']) as image:assert image.size==(128,128),name
 print('Verified',len(document['derivations']),'derived materials: input identities, source references and output hashes.')
if __name__=='__main__':
 if '--verify' in sys.argv:verify()
 else:run()
