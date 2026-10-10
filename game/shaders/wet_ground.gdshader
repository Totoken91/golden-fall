shader_type spatial;
// Rain-soaked ground (asphalt, sidewalk): the real Poly Haven maps, darkened and glossed by water,
// with puddles from a world-space noise mask and rain-drop ripple rings in their normals.
// GL Compatibility has no screen-space reflections, so puddles fake the sky with a fresnel term and
// let the sodium lamps' specular stretch across them. Ripple technique after Zavie's Shadertoy
// "Ripples" (rings in jittered cells), as used by godotshaders.com "Rain puddles with ripples".
render_mode specular_schlick_ggx;
uniform sampler2D albedo_tex : source_color, filter_nearest_mipmap, repeat_enable;
uniform sampler2D normal_tex : hint_normal, filter_nearest_mipmap, repeat_enable;
uniform vec3 tint : source_color = vec3(1.0);
uniform vec2 uv_scale = vec2(1.0);
uniform float puddles = 0.5;          // 0 = damp only, 1 = flooded
uniform float puddle_scale = 0.16;    // noise frequency per metre
uniform vec3 sky_reflection : source_color = vec3(0.30, 0.285, 0.26);
uniform float ripple_rate = 1.4;
varying vec3 world_pos;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
	vec2 i = floor(p), f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
}

// Sum of expanding rings from jittered drops in 0.45 m cells; returns the height gradient.
vec2 ripples(vec2 p) {
	vec2 grad = vec2(0.0);
	vec2 cell = floor(p / 0.45);
	for (int j = -1; j <= 1; j++) {
		for (int i = -1; i <= 1; i++) {
			vec2 c = cell + vec2(float(i), float(j));
			float h = hash(c);
			vec2 centre = (c + vec2(hash(c + 3.1), hash(c + 5.7))) * 0.45;
			float t = fract(TIME * ripple_rate * mix(0.7, 1.3, h) + h * 9.0);
			vec2 d = p - centre;
			float r = length(d);
			float ring = r - t * 0.32;
			float wave = sin(ring * 60.0) * exp(-ring * ring * 900.0) * (1.0 - t) * (1.0 - t);
			grad += (r > 0.0001 ? d / r : vec2(0.0)) * wave;
		}
	}
	return grad;
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	vec2 uv = UV * uv_scale;
	vec3 base = texture(albedo_tex, uv).rgb * tint;
	float n = noise(world_pos.xz * puddle_scale) * 0.65 + noise(world_pos.xz * puddle_scale * 3.1) * 0.35;
	float puddle = smoothstep(0.62 - puddles * 0.25, 0.70 - puddles * 0.25, n);
	vec2 rip = ripples(world_pos.xz) * mix(0.25, 1.0, puddle);
	vec3 tex_n = texture(normal_tex, uv).rgb * 2.0 - 1.0;
	tex_n.xy *= mix(0.6, 0.05, puddle);                // standing water flattens the grain
	tex_n.xy += rip * 0.45;
	NORMAL_MAP = normalize(tex_n) * 0.5 + 0.5;
	// Wet surfaces darken; puddles darken more and turn glossy.
	ALBEDO = base * mix(0.82, 0.5, puddle);
	ROUGHNESS = mix(0.42, 0.12, puddle);
	SPECULAR = 0.55;
	float fresnel = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0);
	EMISSION = sky_reflection * fresnel * mix(0.18, 1.1, puddle);
}
