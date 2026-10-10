from pathlib import Path
import math, random, wave, struct
root = Path(__file__).resolve().parents[2]/'game'/'assets'
portrait = root/'portraits'
portrait.mkdir(parents=True,exist_ok=True)
for expression in ('neutral','soft_smile','worried'):
    mouth = {'neutral':'M 274 318 Q 298 322 318 316','soft_smile':'M 270 314 Q 296 333 321 313','worried':'M 276 322 Q 297 314 318 322'}[expression]
    brow = 'M 253 253 L 277 248 M 309 248 L 333 253' if expression != 'worried' else 'M 251 253 L 277 243 M 309 243 L 334 253'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="640" viewBox="0 0 540 640">
<path fill="#ede0c6" d="M0 0h540v640H0z"/>
<path fill="#d2c4a9" opacity=".7" d="M61 640V214L113 111 244 62 398 117 449 251 478 640z"/>
<path fill="#49382e" stroke="#3d3028" stroke-width="4" d="M159 363L141 222Q139 110 243 91Q347 59 382 173L400 397 332 446 178 409z"/>
<path fill="#ba8e70" d="M244 329l-9 69 67 50 42-45-21-83z"/>
<path fill="#cba585" stroke="#624c3a" stroke-width="3" d="M209 197Q212 153 283 148Q353 156 354 215L347 287Q338 340 301 359Q251 351 224 313z"/>
<path fill="#49382e" d="M181 249Q179 135 269 123L344 140 371 227Q313 206 291 160Q259 211 208 237l-8 99z"/>
<path fill="#584236" opacity=".55" d="M177 229L190 385 218 398 212 228zM358 206l28 181-28 25-11-180z"/>
<path fill="#d4b394" d="M241 254l40-8 47 12-9 47-36 22-34-24z"/>
<g fill="none" stroke="#564235" stroke-width="3.5" stroke-linecap="round"><path d="{brow}"/><path d="M251 269q15-9 29-1M310 269q13-8 26-1"/><path d="M296 271l-6 28 12 3"/><path d="{mouth}"/></g>
<g fill="#39392f"><ellipse cx="268" cy="269" rx="4" ry="5"/><ellipse cx="322" cy="269" rx="4" ry="5"/></g>
<path fill="#657266" stroke="#39473e" stroke-width="4" d="M85 640l31-164 119-84 53 37 55-39 105 91 42 159z"/>
<path fill="#546257" d="M238 393l51 36 54-39-18 63-39 16-42-17z"/>
<path fill="none" stroke="#859080" stroke-width="4" d="M128 486l33 154M426 490l-32 150M227 408l20 49 39 14 39-17 18-47"/>
<path fill="#433c31" d="M360 439l18 10-83 191h-22z"/>
<path fill="#b8b2a0" stroke="#493f34" stroke-width="3" d="M244 542l80-4 7 62-87 3z"/>
<circle cx="281" cy="571" r="20" fill="#534f43"/><circle cx="281" cy="571" r="12" fill="#7a8274"/>
<g stroke="#6e5a43" opacity=".13"><path d="M20 76l481 8M17 192l489-13M40 527l449 18M88 615l344-11"/></g>
</svg>'''
    (portrait/f'hannah_{expression}.svg').write_text(svg,encoding='utf-8')
audio=root/'audio';audio.mkdir(parents=True,exist_ok=True)
for label in ('rain','room'):
    rng=random.Random(2003)
    rate=22050;length=rate*8;low=0.;samples=[]
    for i in range(length):
        t=i/rate
        low=low*.97+rng.uniform(-1,1)*.03
        value=low*.45 + rng.uniform(-1,1)*.06 if label=='rain' else math.sin(t*math.tau*60)*.035+low*.12
        # Seam envelope avoids loop clicks.
        envelope=min(1,i/1000,(length-1-i)/1000)
        samples.append(struct.pack('<h',int(max(-1,min(1,value*envelope))*32767)))
    with wave.open(str(audio/f'{label}.wav'),'wb') as f:
        f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes(b''.join(samples))
print('Original provisional SVG portraits and ambience WAV created.')
