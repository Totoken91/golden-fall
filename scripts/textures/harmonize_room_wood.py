"""Harmonize cached wood materials in 128px, without downloading or changing lighting.
Run after prepare_room_materials.py; settings live in game/data/room_materials.json.
"""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageStat
from integration import publish
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def harmonize(root=ROOT):
 path=root/'game/data/room_materials.json';config=json.loads(path.read_text(encoding='utf-8'))
 settings=config['cohesion'];manifest=json.loads((root/'assets/textures/manifest.json').read_text(encoding='utf-8'))
 recipes={}
 for rule in config['surfaces']:
  if not rule.get('metric_wood_uv'):continue
  # Preserve source provenance and make reruns idempotent.
  source_key=rule.get('cohesion_source_key',rule.get('key'))
  entry=manifest['assets'][source_key]
  asset_id=entry['id']
  if source_key not in recipes:
   dest=root/'assets/textures/optimized/room_cohesion'/asset_id;dest.mkdir(parents=True,exist_ok=True)
   albedo=Image.open(root/entry['optimized_maps']['albedo']['path']).convert('RGB')
   assert albedo.size==(128,128)
   mean=ImageStat.Stat(albedo).mean
   contrast=float(settings['albedo_contrast']);exposure=float(settings['albedo_exposure'])
   channels=albedo.split()
   albedo=Image.merge('RGB',tuple(c.point([max(0,min(255,round((m+(v-m)*contrast)*exposure))) for v in range(256)]) for c,m in zip(channels,mean)))
   target=dest/'albedo.png';albedo.save(target,optimize=True)
   maps={role:{**info,'path':root/info['path']} for role,info in entry['optimized_maps'].items()}
   maps['albedo']={'path':target,'sha256':sha(target)}
   recipe={'source_key':source_key,'source_page':entry['source_page'],'license':entry['license'],
    'source_tile_m':entry['tile_m'],'source_albedo_sha256':entry['optimized_maps']['albedo']['sha256'],
    'transformations':{'size':[128,128],'contrast_around_each_channel_mean':contrast,'exposure':exposure,
     'target_texels_per_m':settings['wood_target_texels_per_m'],'rendered_tile_m':128/settings['wood_target_texels_per_m'],
     'notes':'All four maps share the same UV scale. No new source, resolution, geometry or baked lighting.'}}
   sig=hashlib.sha256(json.dumps(recipe,sort_keys=True).encode()).hexdigest()[:8]
   key='room_cohesion/'+asset_id+'/'+sig
   profile={'filter_enum':2,'normal_scale':.10}
   output=publish(root,key,maps,entry['tile_m'],entry['tile_m'],profile)
   recipe['godot']=output
   recipe['status']='pending_engine_review'
   recipes[source_key]=recipe
  recipe=recipes[source_key]
  rule['cohesion_source_key']=source_key
  rule.pop('key',None)
  rule['material']='res://'+recipe['godot']['material'].removeprefix('game/')
  rule['texels_per_m']=settings['wood_target_texels_per_m']
  if rule['material_name']=='darkwood':rule['tint']=settings['dark_wood_tint']
 path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 output={'schema_version':1,'purpose':'Wood cohesion pass, original official sources cached, 0 network requests','settings':settings,'materials':recipes}
 (root/'assets/textures/cohesion_manifest.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Harmonized',len(recipes),'wood sources across',sum(bool(r.get('metric_wood_uv')) for r in config['surfaces']),'surfaces at',settings['wood_target_texels_per_m'],'texels/m; all maps remain 128px.')
def verify(root=ROOT):
 manifest=json.loads((root/'assets/textures/cohesion_manifest.json').read_text(encoding='utf-8'))
 official=json.loads((root/'assets/textures/manifest.json').read_text(encoding='utf-8'))
 for key,entry in manifest['materials'].items():
  source=official['assets'][key]
  assert entry['source_albedo_sha256']==source['optimized_maps']['albedo']['sha256']
  for role,info in entry['godot']['maps'].items():
   path=root/info['path'];assert sha(path)==info['sha256']
   assert Image.open(path).size==(128,128)
   if role!='albedo':assert info['sha256']==source['optimized_maps'][role]['sha256']
  assert sha(root/entry['godot']['material'])==entry['godot']['sha256']
 print('Cohesion hashes verified; original normal/roughness/AO unchanged, 128px maps aligned.')
if __name__=='__main__':
 if '--verify' in sys.argv:verify()
 else:harmonize()
