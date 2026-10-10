"""Before/after slider gallery from two town_views.gd capture folders (same cameras required).

python scripts/qa/town_gallery.py BEFORE_DIR AFTER_DIR OUT_DIR "Title" "Intro paragraph (HTML)" [notes.json]
notes.json maps view name -> one-line caption (French, for the project owner).
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image

TITLES = {'01_porch_to_street': 'Depuis le porche', '02_street_north': 'La rue vers le nord', '03_diner_storefront': 'Façade du diner',
	'04_diner_inside': 'Intérieur du diner', '05_hannah_booth_view': 'La banquette de Hannah', '06_alley_approach': 'La ruelle',
	'07_service_door': 'Porte de service', '08_street_south': 'Retour vers la maison', '09_curb_close': 'Bordure de près',
	'10_house_facade': 'Maison voisine de près', '11_records_brick': 'Devanture du disquaire', '12_home_roofline': 'Ta maison', '13_maple_close': 'Érable de près', '14_fir_wall': 'Mur de sapins'}

before, after, out = (Path(a) for a in sys.argv[1:4])
title, intro = sys.argv[4], sys.argv[5]
notes = json.loads(Path(sys.argv[6]).read_text(encoding='utf-8')) if len(sys.argv) > 6 else {}
cb, ca = (json.loads((d/'cameras.json').read_text()) for d in (before, after))
if cb != ca: sys.exit('Camera transforms differ between before and after: not a fair comparison')
out.mkdir(parents=True, exist_ok=True)
def pair(v):
	a, b = Image.open(before/f'{v}.png'), Image.open(after/f'{v}.png')
	s = Image.new('RGB', (a.width*2+8, a.height), (20, 18, 14)); s.paste(a, (0, 0)); s.paste(b, (a.width+8, 0)); return s
secs, nav = [], []
for v in sorted(ca):
	t = TITLES.get(v, v)
	shutil.copy(before/f'{v}.png', out/f'avant_{v}.png'); shutil.copy(after/f'{v}.png', out/f'apres_{v}.png')
	pair(v).save(out/f'avant_apres_{v}.png')
	nav.append(f'<a href="#{v}">{t}</a>')
	secs.append(f'''<section id="{v}"><h2>{t}</h2><p>{notes.get(v, '')}</p><button onclick="setView('{v}',100)">Avant</button><button onclick="setView('{v}',50)">Comparer</button><button onclick="setView('{v}',0)">Après</button><div class="compare"><img alt="{t} avant" src="avant_{v}.png"><img class="after" id="image_{v}" alt="{t} après" src="apres_{v}.png"></div><input id="slider_{v}" aria-label="Comparaison {t}" type="range" value="50" min="0" max="100" oninput="setView('{v}',this.value)"><p><a href="avant_apres_{v}.png">Voir côte à côte</a></p></section>''')
pair(notes.get('_hero', sorted(ca)[1])).save(out/'comparatif.png')
style = ('body{max-width:1280px;margin:28px auto;padding:0 16px;background:#211e18;color:#dfd1b6;font:17px/1.5 system-ui}h1,h2{color:#d9b881}'
	'.compare{position:relative;aspect-ratio:16/9;overflow:hidden}.compare img{position:absolute;inset:0;width:100%;height:100%}.after{clip-path:inset(0 0 0 50%)}'
	'input{width:100%;accent-color:#b99456}a{color:#dfbf85}nav a{display:inline-block;margin:4px 12px 4px 0}'
	'button{background:#564832;color:#f1e2c7;border:1px solid #b3915d;padding:6px 14px;margin:0 8px 8px 0;cursor:pointer}')
html = (f'<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title><style>{style}</style>'
	f'<h1>{title}</h1>{intro}'
	+ ('<section id="video"><h2>Vidéo : parcours réel dans le moteur</h2><video controls src="town_walk.mp4" style="width:100%"></video></section>' if (out/'town_walk.mp4').exists() else '')
	+ f'<nav>{" · ".join(nav)}</nav>{"".join(secs)}'
	"<script>function setView(n,v){document.getElementById('slider_'+n).value=v;document.getElementById('image_'+n).style.clipPath='inset(0 0 0 '+v+'%)'}</script></html>")
(out/'index.html').write_text(html, encoding='utf-8')
print('gallery', out/'index.html', len(secs), 'views')
