"""Decode the supplied recording, crossfade its ends and peak-normalize a WAV loop."""
from pathlib import Path
import subprocess,sys,json,hashlib,wave,array,math
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'assets/audio_source/freesound_community-rain-from-inside-76646.mp3'
target=ROOT/'game/assets/audio/rain.wav'
rate=22050
result=subprocess.run([sys.argv[1],'-hide_banner','-i',str(source),'-f','f32le','-ac','1','-ar',str(rate),'-'],capture_output=True)
(ROOT/'verification/rain_audio_encode.txt').write_text(result.stderr.decode('utf-8',errors='replace'),encoding='utf-8')
assert result.returncode==0
samples=array.array('f');samples.frombytes(result.stdout)
overlap=2*rate
assert len(samples)>3*overlap
loop=array.array('f',samples[overlap:])
# Crossfade tail into source 0..2. The boundary rejoins adjacent source samples.
for i in range(overlap):
    mix=i/(overlap-1)
    loop[len(loop)-overlap+i]=loop[len(loop)-overlap+i]*math.cos(mix*math.pi/2)+samples[i]*math.sin(mix*math.pi/2)
gain=10**(-3/20)/max(abs(s) for s in loop)
data=array.array('h',(round(s*gain*32767) for s in loop))
with wave.open(str(target),'wb') as stream:
    stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(rate);stream.writeframes(data.tobytes())
peak=max(abs(s) for s in data)/32768
boundary=abs(data[-1]-data[0])/32768
rms=math.sqrt(sum((s/32768)**2 for s in data)/len(data))
expected_boundary=abs(samples[overlap-1]-samples[overlap])*gain
assert peak<.8 and abs(boundary-expected_boundary)<2/32768,(peak,boundary,expected_boundary)
report={'source':'assets/audio_source/'+source.name,'source_provenance':'Recording supplied by the user on 2026-10-09; license not inferred from the filename.',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime':'game/assets/audio/rain.wav',
 'channels':1,'sample_rate':rate,'duration_seconds':len(data)/rate,'sample_width_bits':16,
 'crossfade_seconds':2,'normalization':'Constant gain after equal-power crossfade; peak -3 dBFS',
 'peak_dbfs':20*math.log10(peak),'rms_dbfs':20*math.log10(rms),'loop_boundary_step':boundary,
 'original_adjacent_sample_step_after_gain':expected_boundary,'boundary_matches_original_continuous_recording':True,
 'runtime_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
(ROOT/'verification/rain_audio.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
