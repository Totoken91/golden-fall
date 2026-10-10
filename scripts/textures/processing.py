"""Deterministic map-specific conversion. No baked lighting or displacement geometry."""
import math
from pathlib import Path, PurePosixPath
import re
import zipfile
from PIL import Image, ImageChops, ImageEnhance, ImageStat
from net import PipelineError, digest

PROCESSOR_VERSION = 1


def image_info(path):
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.width < 64 or image.height < 64:
                raise PipelineError('Texture too small; preview suspected: ' + str(path))
            return {'width': image.width, 'height': image.height, 'mode': image.mode}
    except (OSError, ValueError) as exc:
        raise PipelineError('Invalid image: ' + str(path)) from exc


def extract_maps(archive, dest, ao=True):
    """Read only chosen image members, never extract paths from the ZIP to disk."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    roles = {'albedo': ('_color', '_albedo', '_basecolor'),
             'normal': ('_normalgl', '_normalopengl', '_normaldx'),
             'roughness': ('_roughness',), 'ao': ('_ambientocclusion', '_ao')}
    selected = {}
    with zipfile.ZipFile(archive) as z:
        if len(z.infolist()) > 256:
            raise PipelineError('Archive contains too many members')
        for member in z.infolist():
            name = PurePosixPath(member.filename.replace('\\', '/'))
            if name.is_absolute() or '..' in name.parts:
                raise PipelineError('Unsafe ZIP member path')
            if member.file_size > 48 * 1024 * 1024:
                raise PipelineError('Archive member too large')
        for role, endings in roles.items():
            if role == 'ao' and not ao:
                continue
            candidates = []
            for member in z.infolist():
                path = PurePosixPath(member.filename)
                if path.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
                    continue
                stem = path.stem.lower()
                for priority, ending in enumerate(endings):
                    if stem.endswith(ending):
                        candidates.append((priority, member.filename, member))
            if not candidates:
                if role == 'ao':
                    continue
                raise PipelineError('Required map missing from archive: ' + role)
            member = min(candidates, key=lambda x: (x[0], x[1]))[2]
            target = dest / (role + PurePosixPath(member.filename).suffix.lower())
            body = z.read(member)  # zipfile validates member CRC here
            if not target.exists() or target.read_bytes() != body:
                target.write_bytes(body)
            image_info(target)
            selected[role] = {'path': target, 'archive_member': member.filename,
                              'sha256': digest(target), 'normal_convention':
                              ('DirectX' if '_normaldx' in member.filename.lower() else 'OpenGL') if role == 'normal' else None}
    return selected


def normalize_normal(image, directx=False):
    pixels = []
    rgb = image.convert('RGB')
    data = rgb.get_flattened_data() if hasattr(rgb, 'get_flattened_data') else rgb.getdata()
    for r, g, b in data:
        x, y, z = r / 127.5 - 1, g / 127.5 - 1, b / 127.5 - 1
        if directx:
            y = -y
        length = math.sqrt(x*x + y*y + z*z)
        if length < 1e-6:
            x, y, z, length = 0, 0, 1, 1
        pixels.append(tuple(max(0, min(255, round((v / length + 1) * 127.5))) for v in (x, y, z)))
    out = Image.new('RGB', image.size)
    out.putdata(pixels)
    return out


def seam_metrics(image):
    """Diagnostic, not a claim of seamless certification; compare to inner jumps."""
    image = image.convert('RGB')
    w, h = image.size
    def delta(a, b):
        return round(sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / (3 * 255), 6)
    return {'edge_x_mean_abs': delta(image.crop((0, 0, 1, h)), image.crop((w-1, 0, w, h))),
            'edge_y_mean_abs': delta(image.crop((0, 0, w, 1)), image.crop((0, h-1, w, h))),
            'inner_x_mean_abs': delta(image.crop((w//2-1, 0, w//2, h)), image.crop((w//2, 0, w//2+1, h))),
            'inner_y_mean_abs': delta(image.crop((0, h//2-1, w, h//2)), image.crop((0, h//2, w, h//2+1))),
            'visual_review_required': True}


def convert_maps(sources, dest, profile, side):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    converted = {}
    albedo = None
    for role, source in sources.items():
        info = image_info(source['path'])
        with Image.open(source['path']) as raw:
            image = raw.convert('RGB' if role in ('albedo', 'normal') else 'L')
            ratio = min(1.0, side / max(image.size))
            size = tuple(max(1, round(v * ratio)) for v in image.size)
            image = image.resize(size, Image.Resampling.LANCZOS if role == 'albedo' else Image.Resampling.BILINEAR)
            steps = ['resize keeping aspect ratio; no upscaling']
            if role == 'albedo':
                image = ImageEnhance.Color(image).enhance(profile['saturation'])
                channels = image.split()
                image = Image.merge('RGB', tuple(channel.point([min(255, round(i * gain)) for i in range(256)])
                                                 for channel, gain in zip(channels, profile['rgb_gain'])))
                steps += ['sRGB albedo only: mild saturation and RGB gains; no baked light']
                albedo = image.copy()
            elif role == 'normal':
                image = normalize_normal(image, source.get('normal_convention') == 'DirectX')
                steps += ['linear vector map; DirectX Y flipped if needed; renormalized after resize']
            else:
                steps += ['linear grayscale; no palette or gamma adjustment']
            target = dest / (role + '.png')
            image.save(target, optimize=True)
        converted[role] = {'path': target, 'sha256': digest(target), 'bytes': target.stat().st_size,
                           'source_dimensions': [info['width'], info['height']], 'output_dimensions': list(size),
                           'color_space': 'sRGB' if role == 'albedo' else 'linear', 'steps': steps}
    sizes = {tuple(value['source_dimensions']) for value in converted.values()}
    if len(sizes) != 1:
        raise PipelineError('PBR maps have inconsistent source dimensions; alignment must be resolved')
    # These are review boards of real file maps, never used as a material texture.
    tiling = Image.new('RGB', (albedo.width * 2, albedo.height * 2))
    for x in range(2):
        for y in range(2):
            tiling.paste(albedo, (x * albedo.width, y * albedo.height))
    tiling.save(dest / 'review_tiling_2x2.png')
    return converted, seam_metrics(albedo)
