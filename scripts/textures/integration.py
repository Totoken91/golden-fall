"""Publish genuine optimized maps as opt-in Godot resources, without editing scenes."""
import shutil
import re
from pathlib import Path
from net import PipelineError, digest, write_json


def prepare_texture_import(target, resource_path, role):
    """Enable real mip levels, including before an asset's first Godot import."""
    settings = {'compress/mode': '0', 'mipmaps/generate': 'true',
                'compress/normal_map': '1' if role == 'normal' else '2',
                'detect_3d/compress_to': '0'}
    path = target.with_name(target.name + '.import')
    if path.exists():
        text = path.read_text(encoding='utf-8')
    else:
        text = ('[remap]\nimporter="texture"\ntype="CompressedTexture2D"\n\n'
                '[deps]\nsource_file="' + resource_path + '"\n\n[params]\n')
    for name, value in settings.items():
        pattern = r'^' + re.escape(name) + r'=.*$'
        if re.search(pattern, text, flags=re.M):
            text = re.sub(pattern, name + '=' + value, text, flags=re.M)
        else:
            text += name + '=' + value + '\n'
    path.write_text(text, encoding='utf-8')


def publish_catalog(root, assets):
    catalog = {key: {'provider': value['provider'], 'id': value['id'], 'tile_m': value['tile_m'],
                    'material': 'res://' + value['godot']['material'].removeprefix('game/'),
                    'status': value['status']} for key, value in assets.items()}
    write_json(root / 'game/assets/textures/library/catalog.json', catalog)


def publish(root, key, maps, tile_m, surface_m, profile):
    runtime = root / 'game/assets/textures/library' / key
    runtime.mkdir(parents=True, exist_ok=True)
    refs = []
    outputs = {}
    for role, item in maps.items():
        target = runtime / (role + '.png')
        if not target.exists() or digest(target) != item['sha256']:
            shutil.copyfile(item['path'], target)
        res_path = 'res://' + target.relative_to(root / 'game').as_posix()
        prepare_texture_import(target, res_path, role)
        refs.append(f'[ext_resource type="Texture2D" path="{res_path}" id="{role}"]')
        outputs[role] = {'path': target.relative_to(root).as_posix(), 'sha256': digest(target)}
    sx, sy = (surface_m[i] / tile_m[i] for i in range(2))
    properties = [f'resource_name = "{key}"', f'texture_filter = {profile["filter_enum"]}',
                  'texture_repeat = true', f'uv1_scale = Vector3({sx:.9f}, {sy:.9f}, 1)',
                  'albedo_texture = ExtResource("albedo")', 'metallic = 0.0',
                  'metallic_specular = 0.25', 'roughness = 1.0',
                  'roughness_texture = ExtResource("roughness")', 'roughness_texture_channel = 0',
                  'normal_enabled = true', f'normal_scale = {profile["normal_scale"]}',
                  'normal_texture = ExtResource("normal")']
    if 'ao' in maps:
        properties += ['ao_enabled = true', 'ao_texture = ExtResource("ao")',
                       'ao_texture_channel = 0', 'ao_light_affect = 0.15']
    material = runtime / 'material.tres'
    material.write_text('[gd_resource type="StandardMaterial3D" load_steps=' + str(len(refs) + 1)
                        + ' format=3]\n\n' + '\n'.join(refs) + '\n\n[resource]\n'
                        + '\n'.join(properties) + '\n', encoding='utf-8')
    return {'material': material.relative_to(root).as_posix(), 'sha256': digest(material),
            'maps': outputs, 'tile_m': tile_m, 'surface_m': surface_m,
            'uv_scale': [sx, sy], 'uv_contract': 'UV 0..1 spans surface_m; change scale per target surface',
            'applied_to_game_scene': False}
