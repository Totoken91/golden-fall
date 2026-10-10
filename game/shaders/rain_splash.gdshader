shader_type spatial;
// Splash crowns around the player: every instance re-rolls its spot on each short cycle (no CPU
// work), sits on the town ground (road 0, sidewalks/lawns 0.14-0.15) and skips the diner interior.
render_mode cull_disabled, blend_mix, depth_draw_never, shadows_disabled, specular_disabled;
uniform vec3 town_origin = vec3(200.0, 0.0, 0.0);
uniform float box = 22.0;
uniform vec3 tint : source_color = vec3(0.62, 0.60, 0.56);
varying float life;
varying float seen;

float hash(float n) { return fract(sin(n * 127.1) * 43758.5453); }

float ground(vec2 p) {
	float ax = abs(p.x);
	if (ax < 4.0) return 0.0;
	if (ax < 6.5) return 0.15;
	return 0.14;   // lawns and the alley ground
}

void vertex() {
	float period = mix(0.35, 0.6, INSTANCE_CUSTOM.r);
	float t = TIME / period + INSTANCE_CUSTOM.g * 17.0;
	float cycle = floor(t);
	life = fract(t);
	float seed = INSTANCE_CUSTOM.b * 1000.0 + cycle * 3.17;
	vec3 centre = (MODEL_MATRIX * vec4(0.0, 0.0, 0.0, 1.0)).xyz;
	vec3 p = centre + vec3((hash(seed) - 0.5) * box, 0.0, (hash(seed + 1.7) - 0.5) * box);
	vec2 local = p.xz - town_origin.xz;
	p.y = town_origin.y + ground(local) + 0.005;
	// Diner interior (TownZone.DINER) and the space under the houses' roofs stay dry.
	bool diner = local.x > -14.5 && local.x < -6.5 && local.y > -62.0 && local.y < -50.0;
	bool alley = local.x > -22.5 && local.x < -6.5 && local.y > -65.5 && local.y < -62.0;
	bool dry = diner || (abs(local.x) > 7.6 && !alley);
	seen = dry ? 0.0 : 1.0;
	vec3 to_camera = CAMERA_POSITION_WORLD - p;
	to_camera.y = 0.0;
	vec3 side = normalize(cross(vec3(0.0, 1.0, 0.0), normalize(to_camera + vec3(0.0001))));
	float size = mix(0.06, 0.2, life) * mix(0.7, 1.2, INSTANCE_CUSTOM.r);
	vec3 world_vertex = p + side * VERTEX.x * size + vec3(0.0, (VERTEX.y + 0.5) * size * 0.8, 0.0);
	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * vec4(world_vertex, 1.0);
	NORMAL = (VIEW_MATRIX * vec4(normalize(to_camera + vec3(0.0001)), 0.0)).xyz;
}

void fragment() {
	// Crown: a thin bowl rim opening upward, plus two flung droplets.
	vec2 q = UV * 2.0 - 1.0;
	q.y = -q.y;
	float rim = smoothstep(0.22, 0.0, abs(length(vec2(q.x, (q.y + 1.0) * 1.6)) - 0.8)) * step(q.y, 0.1);
	float drops = smoothstep(0.16, 0.0, length(q - vec2(0.55, 0.55 * (1.0 - life)))) + smoothstep(0.16, 0.0, length(q - vec2(-0.5, 0.45 * (1.0 - life))));
	ALBEDO = tint;
	ALPHA = clamp(rim + drops, 0.0, 1.0) * (1.0 - life) * 0.55 * seen;
}

void light() {
	DIFFUSE_LIGHT += LIGHT_COLOR * ATTENUATION * 0.8;
}
