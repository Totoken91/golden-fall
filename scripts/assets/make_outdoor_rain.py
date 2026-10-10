"""Outdoor rain loop for the street (procedural, reproducible): soft broadband wash, gentle
low rumble on wet asphalt, sparse drops on leaves/metal. 22.05 kHz mono 16-bit, 8 s seamless loop.
The user's indoor recording (rain.wav) stays the bedroom sound."""
from pathlib import Path
import math, random, struct, wave

RATE, SECONDS, FADE = 22050, 8.0, 0.5
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'game/assets/audio/rain_outdoor.wav'
rng = random.Random(151003)
n = int(RATE*(SECONDS+FADE))

# Pink-ish noise (Voss-McCartney-like with three one-pole stages) for the wash.
samples = [0.0]*n
b0 = b1 = b2 = 0.0
low = 0.0
for i in range(n):
	white = rng.uniform(-1, 1)
	b0 = .99765*b0 + white*.0990460
	b1 = .96300*b1 + white*.2965164
	b2 = .57000*b2 + white*1.0526913
	pink = (b0+b1+b2+white*.1848)*.11
	low = low + .02*(white-low)          # rumble of water on the road
	samples[i] = pink*.55 + low*.9

# Drops: short decaying ticks, a few heavier drips from gutters.
for _ in range(int(SECONDS*55)):
	start = rng.randrange(0, n-600)
	heavy = rng.random() < .08
	length = rng.randint(220, 520) if heavy else rng.randint(60, 180)
	freq = rng.uniform(900, 1800) if heavy else rng.uniform(2500, 5200)
	amp = rng.uniform(.12, .22) if heavy else rng.uniform(.03, .09)
	for k in range(length):
		t = k/RATE
		samples[start+k] += amp*math.exp(-k/(length*.25))*math.sin(2*math.pi*freq*t)*(1 if heavy else rng.uniform(.6, 1))

# Seamless loop: crossfade the tail into the head, keep SECONDS.
loop = int(RATE*SECONDS); fade = int(RATE*FADE)
out = samples[:loop]
for k in range(fade):
	w = k/fade
	out[k] = out[k]*w + samples[loop+k]*(1-w)
peak = max(abs(s) for s in out)
gain = .6/peak
OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), 'wb') as f:
	f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE)
	f.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, s*gain))*32767)) for s in out))
print('rain_outdoor.wav', loop, 'samples, peak gain', round(gain, 3))
