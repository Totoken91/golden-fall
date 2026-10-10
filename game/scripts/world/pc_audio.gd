class_name PcAudio
extends Node

# Small synthesized PC sounds (no asset files, deterministic): CRT hum, mouse clicks,
# keyboard clacks and the tray notification chime.
const RATE := 22050

var hum: AudioStreamPlayer
var click: AudioStreamPlayer
var key: AudioStreamPlayer
var chime: AudioStreamPlayer
var rng := RandomNumberGenerator.new()

func _ready() -> void:
	rng.seed = 2003
	hum = player(make_hum(),-25.0)
	click = player(make_burst(0.022,0.0,3400.0),-14.0)
	key = player(make_burst(0.045,180.0,2200.0),-17.0)
	chime = player(make_chime(),-15.0)

func player(stream: AudioStreamWAV, volume: float) -> AudioStreamPlayer:
	var result := AudioStreamPlayer.new()
	result.stream = stream
	result.volume_db = volume
	result.max_polyphony = 4
	add_child(result)
	return result

func wav(samples: PackedFloat32Array, looped := false) -> AudioStreamWAV:
	var data := PackedByteArray()
	data.resize(samples.size()*2)
	for i in samples.size():
		data.encode_s16(i*2,int(clampf(samples[i],-1.0,1.0)*32767.0))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = RATE
	stream.data = data
	if looped:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_end = samples.size()
	return stream

func make_hum() -> AudioStreamWAV:
	# Two seconds = whole cycles of 60/120/180 Hz, so the loop is seamless.
	var samples := PackedFloat32Array()
	samples.resize(RATE*2)
	for i in samples.size():
		var t := float(i)/RATE
		samples[i] = .30*sin(TAU*60.0*t)+.16*sin(TAU*120.0*t)+.05*sin(TAU*180.0*t)+.03*(rng.randf()*2.0-1.0)
	return wav(samples,true)

func make_burst(length: float, body_hz: float, bright_hz: float) -> AudioStreamWAV:
	var samples := PackedFloat32Array()
	samples.resize(int(RATE*length))
	var previous := 0.0
	for i in samples.size():
		var t := float(i)/RATE
		var envelope := exp(-t/(length*.22))
		var noise := rng.randf()*2.0-1.0
		var bright := noise-previous*.85
		previous = noise
		samples[i] = envelope*(.55*bright+.25*sin(TAU*bright_hz*t)+(.6*sin(TAU*body_hz*t) if body_hz > 0.0 else 0.0))
	return wav(samples)

func make_chime() -> AudioStreamWAV:
	var samples := PackedFloat32Array()
	samples.resize(int(RATE*.75))
	for i in samples.size():
		var t := float(i)/RATE
		var first := sin(TAU*659.25*t)*exp(-t*7.0)
		var second := sin(TAU*987.77*maxf(t-.12,0.0))*exp(-maxf(t-.12,0.0)*5.0)*(1.0 if t > .12 else 0.0)
		samples[i] = .45*(first+second)+.08*sin(TAU*1975.5*t)*exp(-t*9.0)
	return wav(samples)

func enabled() -> bool:
	return bool(get_parent().game.get("sound_enabled")) and DisplayServer.get_name() != "headless"

func power(on: bool) -> void:
	if on and enabled(): hum.play()
	else: hum.stop()

func play_click() -> void:
	if enabled():
		click.pitch_scale = rng.randf_range(.92,1.08)
		click.play()

func play_key() -> void:
	if enabled():
		key.pitch_scale = rng.randf_range(.88,1.1)
		key.play()

func play_chime() -> void:
	if enabled(): chime.play()
