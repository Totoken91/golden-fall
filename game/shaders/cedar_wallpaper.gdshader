shader_type canvas_item;
// "Morrow Ridge" — original Cedar 03 wallpaper: dusk over forested hills, amber sky, valley fog.
uniform vec2 rect_size = vec2(640.0, 448.0);

float hash(float n) { return fract(sin(n * 127.1) * 43758.5453); }
float hash2(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(float x) { float i = floor(x); float f = fract(x); f = f * f * (3.0 - 2.0 * f); return mix(hash(i), hash(i + 1.0), f); }
float noise2(vec2 p) {
	vec2 i = floor(p); vec2 f = fract(p); f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash2(i), hash2(i + vec2(1, 0)), f.x), mix(hash2(i + vec2(0, 1)), hash2(i + vec2(1, 1)), f.x), f.y);
}
float fbm(vec2 p) { float v = 0.0; float a = 0.5; for (int i = 0; i < 4; i++) { v += a * noise2(p); p *= 2.03; a *= 0.5; } return v; }

// Height of a ridge (0 = top of image) with optional conifer crowns.
float ridge(float x, float base, float amp, float freq, float seed, float trees, float tree_h) {
	float h = base - amp * (noise(x * freq + seed) * 0.7 + noise(x * freq * 2.7 + seed * 3.1) * 0.3);
	if (trees > 0.0) {
		float cell = floor(x * trees);
		float local = fract(x * trees);
		float height = tree_h * (0.55 + 0.45 * hash(cell + seed));
		float crown = height * (1.0 - abs(local - 0.5) * 2.0);
		h -= max(crown, 0.0) * step(0.18, hash(cell * 1.7 + seed));
	}
	return h;
}

void fragment() {
	vec2 uv = UV;
	float aspect = rect_size.x / rect_size.y;
	float x = uv.x * aspect;
	// Sky: deep teal dusk down to an amber horizon.
	vec3 sky = mix(vec3(0.11, 0.21, 0.26), vec3(0.36, 0.45, 0.45), smoothstep(0.0, 0.42, uv.y));
	sky = mix(sky, vec3(0.86, 0.60, 0.32), smoothstep(0.30, 0.60, uv.y));
	vec2 sun = vec2(0.70 * aspect, 0.50);
	float glow = exp(-length((vec2(x, uv.y) - sun) * vec2(1.0, 1.9)) * 4.2);
	sky += vec3(0.95, 0.62, 0.30) * glow * 0.55;
	// Long overcast streaks.
	float clouds = fbm(vec2(x * 1.6 + TIME * 0.004, uv.y * 7.5));
	sky = mix(sky, sky * 0.78 + vec3(0.06, 0.05, 0.05), smoothstep(0.48, 0.78, clouds) * (1.0 - smoothstep(0.35, 0.6, uv.y)) * 0.8);
	sky = mix(sky, vec3(0.98, 0.78, 0.50), smoothstep(0.55, 0.85, clouds) * smoothstep(0.30, 0.52, uv.y) * 0.35);
	vec3 color = sky;
	vec3 fog = vec3(0.80, 0.66, 0.48);
	// Far blue ridge.
	float h1 = ridge(x, 0.56, 0.10, 2.2, 3.0, 70.0, 0.018);
	color = mix(color, mix(vec3(0.36, 0.43, 0.45), fog, 0.45), step(h1, uv.y));
	// Middle conifer line.
	float h2 = ridge(x, 0.66, 0.09, 3.1, 11.0, 48.0, 0.05);
	vec3 mid = mix(vec3(0.17, 0.25, 0.22), fog, 0.28 * (1.0 - smoothstep(h2, h2 + 0.12, uv.y)));
	color = mix(color, mid, step(h2, uv.y));
	// Valley fog sitting in front of the conifers.
	float mist = smoothstep(0.62, 0.74, uv.y) * (1.0 - smoothstep(0.76, 0.88, uv.y));
	color = mix(color, fog * 0.92, mist * (0.35 + 0.25 * fbm(vec2(x * 3.0 + TIME * 0.01, uv.y * 12.0))));
	// Near autumn meadow.
	float h3 = 0.80 - 0.05 * sin(x * 2.2 + 0.6) - 0.025 * noise(x * 6.0);
	vec3 meadow = mix(vec3(0.62, 0.45, 0.20), vec3(0.30, 0.22, 0.11), smoothstep(h3, 1.0, uv.y));
	meadow *= 0.86 + 0.18 * fbm(vec2(x * 40.0, uv.y * 90.0));
	meadow += vec3(0.20, 0.12, 0.04) * glow * 0.6;
	color = mix(color, meadow, step(h3, uv.y));
	// Slight vignette so icons stay readable on the left.
	color *= 1.0 - 0.18 * smoothstep(0.3, 0.0, uv.x) * (1.0 - smoothstep(0.7, 1.0, uv.y));
	color *= 1.0 - 0.25 * pow(length(uv * 2.0 - 1.0) * 0.72, 3.0);
	COLOR = vec4(color, 1.0);
}
