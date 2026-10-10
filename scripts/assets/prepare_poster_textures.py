"""Technical downsampling of the preserved imagegen artwork, no repainting."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
POSTERS = {
    'poster': 'morrow_creek.png',
    'poster2': 'the_long_way_home.png',
}

def prepare():
    out = ROOT/'game/assets/room/textures'
    for material, filename in POSTERS.items():
        source = ROOT/'assets/art/posters'/filename
        with Image.open(source) as image:
            # Wall planes already have a 3:4 portrait aspect and full 0..1 UVs.
            # Do not crop generated typography or introduce upscaled source art.
            image.convert('RGB').resize((192,256),Image.Resampling.LANCZOS).save(out/(material+'.png'))
        print(f'{material}: {source.name} -> 192x256 RGB PNG')

if __name__ == '__main__':
    prepare()
