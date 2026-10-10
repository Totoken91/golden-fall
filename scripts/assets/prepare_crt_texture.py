"""Bake ventilation into the existing tapered shell, rather than floating slats."""
from PIL import Image, ImageDraw
image=Image.open(OUT/'ivory.png').convert('RGB').resize((128,128),Image.Resampling.NEAREST)
draw=ImageDraw.Draw(image)
for i in range(10):
    y=31+i*6
    draw.rectangle((27,y,86,y+1),fill=(40,42,35))
    draw.line((28,y+2,85,y+2),fill=(148,141,111))
image.save(OUT/'crt_side.png')
