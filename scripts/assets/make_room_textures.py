"""Procedural material textures + V0.11 downsampled original imagegen posters.

Poster source images are preserved in assets/art/posters; no generation at runtime.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'game/assets/room/textures'
OUT.mkdir(parents=True, exist_ok=True)
rng = random.Random(130103)

def noise(name, base, amount=12, size=128, grain=False):
    im = Image.new('RGB', (size, size))
    px = im.load()
    coarse = [[rng.uniform(-1, 1) for _ in range(16)] for _ in range(16)]
    for y in range(size):
        for x in range(size):
            n = rng.gauss(0, .45)*amount + coarse[y*16//size][x*16//size]*amount*.55
            if grain:
                n += math.sin(y*.52 + math.sin(x*.025)*2)*9
                n += math.sin(y*1.9+x*.014)*3
            px[x,y] = tuple(max(0,min(255,int(c+n))) for c in base)
    return im

def save(im, name): im.save(OUT / (name+'.png'))

for name, base, amount, grain in [
    ('wood',(93,64,39),18,True), ('darkwood',(49,35,25),12,True),
    ('paint',(142,133,106),8,False), ('ivory',(170,163,133),8,False),
    ('metal',(45,44,36),8,False), ('brass',(113,77,34),10,False),
    ('fabric',(134,123,99),18,False), ('linen',(172,161,132),12,False),
    ('paper',(184,171,132),10,False), ('door',(92,70,42),15,True),
    ('ceiling',(119,114,94),5,False), ('bark',(65,55,39),15,True),
    ('soil',(54,54,42),7,False), ('shade',(189,137,63),12,False),
    ('denim',(49,55,51),10,False), ('curtain',(100,91,68),12,False)]:
    save(noise(name,base,amount,128,grain),name)

# Worn narrow floorboards, random joints and scratches; tiled at about 1.8m.
im=noise('floor',(96,66,41),20,256,True); d=ImageDraw.Draw(im)
for y in range(0,256,32):
    d.line((0,y,255,y), fill=(37,29,21),width=2)
    off=rng.randint(25,185); d.line((off,y,off,y+32),fill=(42,29,20))
    for j in range(15):
        x=rng.randrange(256); yy=y+rng.randrange(4,28)
        d.line((x,yy,min(x+rng.randrange(3,30),255),yy),fill=(118,83,51))
save(im,'floor')

# Faded tiny botanical wallpaper; stains collect near joins.
im=noise('wall',(137,127,101),9,128); d=ImageDraw.Draw(im)
for y in range(4,128,24):
    for x in range(5+(y//24%2)*12,128,24):
        d.line((x,y,x+3,y+13),fill=(107,108,77))
        d.line((x+1,y+4,x-3,y+1),fill=(114,110,82),width=2)
        d.line((x+2,y+8,x+6,y+5),fill=(114,110,82),width=2)
        d.rectangle((x-1,y+12,x+1,y+14),fill=(131,109,81))
save(im,'wall')

# Antique rug with a border, central medallion and irregular woven flecks.
im=noise('rug',(86,57,42),14,256); d=ImageDraw.Draw(im)
for inset,col,width in [(3,(34,39,32),8),(12,(135,100,62),3),(18,(52,60,49),10),(31,(134,95,57),3),(37,(45,48,36),2)]:
    d.rectangle((inset,inset,255-inset,255-inset),outline=col,width=width)
for y in range(47,210,20):
    for x in range(46,210,20):
        c=[(125,89,52),(53,66,53),(165,129,80)][rng.randrange(3)]
        d.polygon([(x,y-5),(x+5,y),(x,y+5),(x-5,y)],fill=c)
        d.point((x,y),fill=(52,38,26))
for r,c in [(45,(38,45,35)),(36,(152,111,65)),(29,(77,52,39)),(19,(47,64,52)),(9,(170,131,80))]:
    d.polygon([(128,128-r),(128+r,128),(128,128+r),(128-r,128)],fill=c)
for i in range(7000):
    x=rng.randrange(256); y=rng.randrange(256)
    c=im.getpixel((x,y)); d.point((x,y), fill=tuple(int(v*.78) for v in c))
save(im,'rug')

im=Image.new('RGB',(256,256)); d=ImageDraw.Draw(im)
colors=[(107,65,42),(45,57,51),(151,119,75),(65,65,49),(134,121,96),(65,47,36)]
for y in range(0,256,16):
    for x in range(0,256,16):
        c=colors[rng.randrange(len(colors))]
        d.rectangle((x,y,x+15,y+15),fill=c)
        d.line((x,y,x+15,y),fill=tuple(int(v*.72) for v in c))
        for k in range(40):
            xx=x+rng.randrange(16); yy=y+rng.randrange(16); n=rng.randint(-14,14)
            d.point((xx,yy),fill=tuple(max(0,min(255,v+n)) for v in c))
save(im,'quilt')

# Rain-streaked old window: gray-blue translucent pane, sparse water trails.
im=Image.new('RGBA',(128,128),(92,106,108,20)); d=ImageDraw.Draw(im)
for i in range(75):
    x=rng.randrange(128); y=rng.randrange(128); length=rng.randrange(2,17)
    d.line((x,y,x-1,y+length),fill=(175,190,184,rng.randint(35,85)))
    d.point((x+1,y),fill=(199,207,196,90))
save(im,'glass')

# Alpha-cut leaf cards, drawn from individual leaves and branching twigs.
for index,base in enumerate([(118,75,31),(143,88,36),(85,91,51)]):
    im=Image.new('RGBA',(128,128),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((64,127,60,30,67,6),fill=(57,48,32,255),width=3)
    for branch in range(17):
        y=20+branch*5; side=-1 if branch%2 else 1
        x=63+side*rng.randint(18,49); yy=max(4,y-rng.randint(5,18))
        d.line((62,y+16,x,yy),fill=(64,51,33,255),width=2)
        for leaf in range(13):
            t=rng.random(); lx=int(62+(x-62)*t)+rng.randint(-10,10); ly=int(y+16+(yy-y-16)*t)+rng.randint(-10,10)
            c=tuple(max(0,min(255,v+rng.randint(-23,23))) for v in base)+(255,)
            w=rng.randint(3,6); h=rng.randint(3,7)
            d.polygon([(lx,ly-h),(lx+w,ly-1),(lx+1,ly+h),(lx-w,ly+1)],fill=c)
            d.line((lx,ly-h+1,lx+1,ly+h-1),fill=(c[0]//2,c[1]//2,c[2]//2,255))
    save(im,'leaves'+str(index))

im=noise('crt',(33,45,42),5,128); d=ImageDraw.Draw(im)
for y in range(128):
    c=int(10+22*y/128); d.line((0,y,127,y),fill=(27+c//2,39+c,40+c))
for j in range(5):
    pts=[(x,95+j*5-int(14*math.sin(x*.06+j)+7*math.sin(x*.17))) for x in range(128)]
    d.polygon(pts+[(127,127),(0,127)],fill=(23+j*3,34+j*3,30+j*3))
d.rectangle((8,8,15,15),fill=(136,145,112)); d.rectangle((9,9,14,13),fill=(75,96,83))
d.rectangle((0,121,127,127),fill=(106,116,97)); d.rectangle((2,122,23,126),fill=(58,80,62))
for y in range(0,128,2):
    for x in range(128):
        c=im.getpixel((x,y)); im.putpixel((x,y),tuple(int(v*.88) for v in c))
save(im,'screen')

im=noise('keyboard',(137,132,111),5,128); d=ImageDraw.Draw(im)
for y in range(8,104,19):
    for x in range(5,104,9):
        d.rectangle((x,y,x+6,y+14),fill=(190,184,155),outline=(67,66,55))
        d.point((x+2,y+2),fill=(75,75,65))
d.rectangle((29,105,76,120),fill=(184,176,147),outline=(64,63,51))
for y in range(8,121,19):
    for x in range(108,127,9): d.rectangle((x,y,x+6,y+14),fill=(178,172,143),outline=(66,66,52))
save(im,'keys')

font=ImageFont.truetype('C:/Windows/Fonts/courbd.ttf',12)
small=ImageFont.truetype('C:/Windows/Fonts/cour.ttf',9)
for name, heading,sub,palette in [
    ('poster','MORROW CREEK','OCTOBER / 2003',[(158,132,85),(48,58,45),(108,76,42)]),
    ('poster2','THE LONG WAY','HOME',[(164,151,116),(70,66,49),(107,87,61)]),
    ('book','FIELD NOTES','NORTHWEST',[(120,105,73),(47,61,49),(136,105,67)])]:
    im=noise(name,palette[0],10,128); d=ImageDraw.Draw(im)
    d.rectangle((6,6,121,121),outline=palette[1],width=2)
    d.text((10,12),heading,font=small,fill=palette[1])
    d.text((10,108),sub,font=small,fill=palette[1])
    d.ellipse((36,31,91,82),fill=palette[2])
    for x in range(10,120,13):
        h=rng.randint(20,44); d.polygon([(x,96-h),(x-9,97),(x+9,97)],fill=palette[1])
    save(im,name)

im=noise('notebook',(192,179,146),6,128); d=ImageDraw.Draw(im)
for y in range(20,121,9): d.line((10,y,120,y),fill=(143,151,134))
d.line((23,0,23,127),fill=(163,110,86)); d.text((29,12),'OCT 13',font=font,fill=(70,69,58))
for y in [38,47,65,83]:
    for x in range(29,rng.randrange(75,116),5): d.line((x,y,x+3,y-rng.randrange(3)),fill=(78,78,65))
save(im,'notebook')

# V0.8 material pass: every surface has its own spatial frequency and wear.
rng=random.Random(80803)
for name,base in [('wood',(96,65,38)),('darkwood',(52,37,24)),('door',(91,69,42))]:
    im=Image.new('RGB',(128,128)); px=im.load()
    for y in range(128):
        for x in range(128):
            warp=3.5*math.sin(x*.042)+1.8*math.sin(x*.13)
            grain=math.sin(y*.49+warp)*5+math.sin(y*1.76+warp*.45)*2
            n=grain+rng.uniform(-3,3)
            px[x,y]=tuple(max(0,int(v+n)) for v in base)
    d=ImageDraw.Draw(im)
    for j in range(22):
        x=rng.randrange(128); y=rng.randrange(128)
        d.line((x,y,min(x+rng.randrange(5,30),127),y),fill=tuple(int(v*.73) for v in base))
    save(im,name)

for name,base,kind in [('linen',(170,158,130),'linen'),('fabric',(126,114,86),'weave'),('curtain',(104,92,65),'weave'),('denim',(49,57,53),'twill'),('wool',(67,70,51),'twill')]:
    im=Image.new('RGB',(128,128)); px=im.load()
    for y in range(128):
        for x in range(128):
            n=rng.uniform(-2,2)
            if kind=='twill': n+=4 if (x+y)%6<2 else -2
            else: n+=(3 if x%3==0 else -1)+(2 if y%4==0 else -1)
            px[x,y]=tuple(max(0,min(255,int(v+n))) for v in base)
    save(im,name)

for name,base in [('ivory',(166,160,134)),('metal',(40,43,39)),('brass',(112,80,35)),('paint',(140,132,106))]:
    im=noise(name,base,2,128); d=ImageDraw.Draw(im)
    for j in range(18 if name in ('metal','brass') else 6):
        x=rng.randrange(128); y=rng.randrange(128)
        d.line((x,y,min(x+rng.randrange(3,14),127),y+1),fill=tuple(int(v*.8) for v in base))
    save(im,name)

# Stitching and weave within the existing golden-brown patchwork palette.
im=Image.new('RGB',(256,256)); d=ImageDraw.Draw(im)
for y in range(0,256,32):
    for x in range(0,256,32):
        c=colors[rng.randrange(len(colors))]
        d.rectangle((x,y,x+31,y+31),fill=c)
        for yy in range(y,y+32):
            for xx in range(x,x+32):
                n=rng.randrange(-3,4)+(2 if (xx+yy)%4==0 else 0)
                d.point((xx,yy),fill=tuple(max(0,min(255,v+n)) for v in c))
        d.line((x,y,x+31,y),fill=tuple(int(v*.65) for v in c))
        for xx in range(x+3,x+31,5): d.line((xx,y+2,xx+2,y+2),fill=(152,132,93))
        for yy in range(y+3,y+31,5): d.line((x+2,yy,x+2,yy+2),fill=(152,132,93))
save(im,'quilt')

# Glass contains only faint grime; falling rain and running droplets are animated in 3D.
im=Image.new('RGBA',(128,128),(95,106,106,6)); d=ImageDraw.Draw(im)
for j in range(45):
    x=rng.randrange(128); y=rng.randrange(128)
    d.rectangle((x,y,x+1,y+2),fill=(136,145,137,rng.randrange(5,20)))
save(im,'glass')

# Uneven pine branches, with transparent gaps: no solid geometric cones.
im=Image.new('RGBA',(256,256),(0,0,0,0)); d=ImageDraw.Draw(im)
d.line((128,15,126,255),fill=(53,50,38,255),width=3)
for y in range(26,247,7):
    span=int((y/256)**.8*88)+rng.randrange(-10,11)
    for side in [-1,1]:
        endx=128+side*span; endy=y+rng.randrange(5,18)
        d.line((128,y,endx,endy),fill=(46,56,45,255),width=2)
        for k in range(max(5,span)):
            t=rng.random(); xx=int(128+(endx-128)*t); yy=int(y+(endy-y)*t)
            dx=rng.randrange(-6,7); dy=rng.randrange(0,13)
            c=rng.choice([(39,54,45,255),(52,65,50,255),(64,74,55,255)])
            d.line((xx,yy,xx+dx,yy+dy),fill=c,width=2)
save(im,'pinecard')

# Small personal objects: original lake photograph, handwritten mixtape label and postcard.
im=Image.new('RGB',(128,128),(187,178,151)); d=ImageDraw.Draw(im)
d.rectangle((8,8,119,97),fill=(112,124,118)); d.rectangle((8,61,119,97),fill=(69,83,78))
for j in range(3):
    pts=[(x,50+j*7-int(9*math.sin(x*.07+j))) for x in range(8,120)]
    d.polygon(pts+[(119,74),(8,74)],fill=(66+j*6,76+j*5,57+j*4))
for y in range(75,96,3): d.line((17,y,100,y),fill=(92,103,87))
d.text((13,108),'FALL / 03',font=small,fill=(70,68,53)); save(im,'photo')
im=noise('mixtape',(181,166,127),3,128); d=ImageDraw.Draw(im)
d.text((8,12),'SIDE A',font=font,fill=(50,57,50)); d.text((8,39),'OCT. 03',font=font,fill=(62,62,49))
for y in [67,85,103]: d.line((10,y,115,y),fill=(114,121,101))
d.text((12,74),'late bus',font=small,fill=(65,69,58)); save(im,'mixtape')
# V0.9 hero props: restrained wear follows material construction.
rng=random.Random(90903)
for name,base in [('corduroy',(116,83,47)),('collar',(134,100,60)),('lining',(59,44,35)),('canvas',(82,83,61)),('leather',(75,48,29)),('ceramic',(153,143,109)),('keycaps',(181,174,146)),('stitch',(140,113,74))]:
    im=Image.new('RGB',(128,128)); px=im.load()
    for y in range(128):
        for x in range(128):
            n=rng.uniform(-1.2,1.2)
            if name in ['corduroy','collar']:
                n+=3.5*math.sin(x*math.pi/2)+2*math.sin(y*.055+x*.025)
            elif name=='canvas':n+=(2 if (x+y)%4==0 else -1)+2*math.sin(x*.09)*math.sin(y*.06)
            elif name=='leather':n+=3*math.sin(x*.09+y*.15)+2*math.sin(x*.29-y*.1)
            elif name=='ceramic':n+=2*math.sin(y*.10)+1*math.sin(x*.07)
            px[x,y]=tuple(max(0,min(255,int(c+n))) for c in base)
    if name=='ceramic':
        d=ImageDraw.Draw(im)
        for i in range(45):d.point((rng.randrange(128),rng.randrange(128)),fill=(119,110,81))
    save(im,name)
# Stitches, tabs and buckles are painted on the conforming flap, not floating meshes.
im=Image.open(OUT/'leather.png').convert('RGB');d=ImageDraw.Draw(im)
for x in [10,117]:
    for y in range(7,122,5):d.line((x,y,x,y+2),fill=(133,105,66))
for y in [7,120]:
    for x in range(10,117,5):d.line((x,y,x+2,y),fill=(133,105,66))
for x in [30,97]:
    d.rectangle((x-5,74,x+5,127),fill=(63,40,25))
    d.line((x-4,74,x-4,127),fill=(114,80,46))
    d.rectangle((x-7,89,x+7,104),fill=(139,105,57))
    d.rectangle((x-4,92,x+4,101),fill=(62,43,28))
    d.line((x,90,x,103),fill=(171,134,75))
d.ellipse((92,26,101,35),fill=(154,145,107),outline=(84,81,57))
save(im,'bag_flap')
# Preserve RNG history above for every unchanged material. The two previous
# procedural poster drafts are replaced from the shipped generated originals.
exec(compile((Path(__file__).parent/'prepare_poster_textures.py').read_text(encoding='utf-8'),'prepare_poster_textures.py','exec'))
exec(compile((Path(__file__).parent/'prepare_psx_details.py').read_text(encoding='utf-8'),'prepare_psx_details.py','exec'))
print(f'{len(list(OUT.glob("*.png")))} textures in {OUT}; two imagegen posters, baked PSX details')

exec(compile((Path(__file__).parent/'prepare_forest_textures.py').read_text(encoding='utf-8'),'prepare_forest_textures.py','exec'))
print(f'{len(list(OUT.glob("*.png")))} final PSX textures including forest cutouts')

exec(compile((Path(__file__).parent/'prepare_crt_texture.py').read_text(encoding='utf-8'),'prepare_crt_texture.py','exec'))
