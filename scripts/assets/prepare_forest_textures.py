"""Original low-resolution cutout foliage; deterministic, no network generation."""
from pathlib import Path
from PIL import Image, ImageDraw
import random, math

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'game/assets/room/textures'

def prepare_forest():
    for index,base in enumerate([(108,70,33),(67,79,47),(129,83,38)]):
        rng=random.Random(13000+index)
        im=Image.new('RGBA',(256,256));d=ImageDraw.Draw(im)
        # Asymmetric spreading branch, with separate overlapping clumps and sky gaps.
        centres=[(127,175),(77,129),(166,115),(105,75),(186,165),(51,181),(153,48)]
        d.line((132,255,125,179,119,117,148,55),fill=(45,43,30,255),width=5)
        for cx,cy in centres:
            d.line((126,192,cx,cy),fill=(49,44,31,255),width=3)
            for leaf in range(220):
                angle=rng.random()*math.tau;radius=math.sqrt(rng.random())
                x=int(cx+math.cos(angle)*radius*rng.uniform(27,45))
                y=int(cy+math.sin(angle)*radius*rng.uniform(23,37))
                w=rng.randrange(2,7);h=rng.randrange(2,6)
                shade=rng.choice([-.40,-.20,-.06,.06,.17,.27])
                c=tuple(max(0,min(255,round(v*(1+shade)))) for v in base)+(255,)
                d.polygon([(x-w,y),(x-1,y-h),(x+w,y-1),(x+2,y+h)],fill=c)
                if leaf%7==0:d.point((x,y-h),fill=tuple(min(255,v+13) for v in c[:3])+(255,))
        im.save(OUT/f'canopy{index}.png')
    rng=random.Random(13137)
    im=Image.new('RGBA',(256,128));d=ImageDraw.Draw(im)
    for plant in range(34):
        x=rng.randrange(5,251);height=rng.randrange(18,100)
        d.line((x,127,x+rng.randrange(-10,11),127-height),fill=(45,48,32,255),width=2)
        for leaf in range(18):
            y=127-rng.randrange(2,height);span=int((y-(127-height))/height*17)+3
            xx=x+rng.randrange(-span,span+1);w=rng.randrange(2,7)
            c=rng.choice([(49,61,38,255),(66,74,42,255),(85,77,39,255),(102,73,34,255)])
            d.polygon([(xx-w,y),(xx,y-3),(xx+w,y+1),(xx+1,y+4)],fill=c)
    im.save(OUT/'underbrush.png')
    for layer in range(2):
        rng=random.Random(13300+layer)
        im=Image.new('RGBA',(512,128));d=ImageDraw.Draw(im)
        # A distant forest mass with an irregular skyline and visible internal trunks.
        for j in range(85):
            x=int(j*6+rng.uniform(-4,4));top=rng.randrange(8,47);w=rng.randrange(7,18)
            trunk=(39+layer*7,49+layer*6,40+layer*6,255)
            d.line((x,127,x+1,top+8),fill=trunk,width=2)
            c=(46+layer*8+rng.randrange(-5,6),57+layer*7+rng.randrange(-4,5),46+layer*6,255)
            if j%3==0:
                for y in range(top,118,7):
                    span=max(2,int((y-top)/110*w))
                    d.polygon([(x,y-6),(x-span,y+10),(x+span,y+11)],fill=c)
            else:
                for k in range(20):
                    xx=x+rng.randrange(-w,w+1);yy=top+rng.randrange(0,46)
                    r=rng.randrange(3,9)
                    d.polygon([(xx-r,yy),(xx-r//2,yy-r),(xx+r//2,yy-r+1),(xx+r,yy+2),(xx,yy+r)],fill=c)
        d.rectangle((0,108,511,127),fill=(43+layer*7,54+layer*7,43+layer*7,255))
        im.save(OUT/f'treeline{layer}.png')
    rng=random.Random(13400)
    im=Image.open(OUT/'soil.png').convert('RGB');d=ImageDraw.Draw(im)
    for j in range(240):
        x=rng.randrange(im.width);y=rng.randrange(im.height)
        d.line((x,y,x+rng.randrange(1,4),y+rng.randrange(-1,2)),fill=rng.choice([(68,58,35),(80,64,35),(46,53,36),(43,45,34)]),width=1)
    im.save(OUT/'wetsoil.png')
    print('Forest: 3 canopy cards, underbrush, 2 treelines, wet soil.')

if __name__=='__main__':prepare_forest()
