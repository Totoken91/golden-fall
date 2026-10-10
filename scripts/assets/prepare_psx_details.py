"""Bake tiny book rules and pillow stitches into two small original textures."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'game/assets/room/textures'
BOOK_COLORS=['denim','darkwood','fabric','wood','paper','metal']

def prepare_details():
    # Six columns, each has its own existing material appearance; no new palette.
    atlas=Image.new('RGB',(192,128))
    for index,name in enumerate(BOOK_COLORS):
        source=Image.open(OUT/(name+'.png')).convert('RGB')
        tile=source.resize((32,128),Image.Resampling.NEAREST)
        draw=ImageDraw.Draw(tile)
        for y in [12,115]:
            draw.line((4,y,27,y),fill=(184,171,132),width=2)
        # A few tiny editorial marks, painted rather than geometry.
        for y,width in [(45,18),(50,13),(55,16)]:
            draw.line((7,y,7+width,y),fill=(145,136,111))
        atlas.paste(tile,(32*index,0))
    atlas.save(OUT/'bookspines.png')
    pillow=Image.open(OUT/'linen.png').convert('RGB')
    draw=ImageDraw.Draw(pillow)
    for i in range(6,123,5):
        draw.line((i,5,i+2,5),fill=(133,123,98))
        draw.line((i,122,i+2,122),fill=(133,123,98))
        draw.line((5,i,5,i+2),fill=(133,123,98))
        draw.line((122,i,122,i+2),fill=(133,123,98))
    pillow.save(OUT/'pillow_linen.png')
    print('PSX details baked: bookspines 192x128, pillow_linen 128x128')

if __name__=='__main__':prepare_details()
