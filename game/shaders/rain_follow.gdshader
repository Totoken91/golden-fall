shader_type spatial;
// Outdoor rain around the player (TownZone): each streak falls through a column and wraps, turned
// toward the camera around the vertical axis. Drops are dark against the overcast sky and catch the
// sodium lamps (custom light: no N.L, a drop near a lamp glows from any side). Wind gusts slant them.
render_mode cull_disabled, blend_mix, depth_draw_never, shadows_disabled, specular_disabled;
uniform float height = 12.0;
uniform float speed = 9.0;
uniform vec3 tint : source_color = vec3(0.50, 0.49, 0.46);
uniform vec2 wind = vec2(0.9, 0.35);
varying float opacity;
varying float gust;

void vertex() {
	gust = 0.65 + 0.35 * sin(TIME * 0.55) + 0.2 * sin(TIME * 1.7 + 1.3);
	float fall = fract(INSTANCE_CUSTOM.r + TIME * speed * INSTANCE_CUSTOM.g / height);
	vec3 drift = vec3(wind.x, 0.0, wind.y) * gust * (1.0 - fall) * 1.6;
	vec3 origin = (MODEL_MATRIX * vec4(0.0, height * (1.0 - fall) - 1.0, 0.0, 1.0)).xyz + drift;
	vec3 to_camera = CAMERA_POSITION_WORLD - origin;
	to_camera.y = 0.0;
	vec3 dir = normalize(to_camera + vec3(0.0001));
	vec3 side = normalize(cross(vec3(0.0, 1.0, 0.0), dir));
	// Streak length varies per drop; the slant follows the wind.
	float len = mix(0.75, 1.6, INSTANCE_CUSTOM.b);
	vec3 slant = vec3(wind.x, 0.0, wind.y) * gust * 0.11 * VERTEX.y * len;
	vec3 world_vertex = origin + side * VERTEX.x + vec3(0.0, VERTEX.y * len, 0.0) + slant;
	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * vec4(world_vertex, 1.0);
	NORMAL = (VIEW_MATRIX * vec4(dir, 0.0)).xyz;
	// Drops right in front of the eye would fill whole world pixels: fade them out under ~3 m.
	opacity = INSTANCE_CUSTOM.b * smoothstep(1.5, 3.5, length(CAMERA_POSITION_WORLD - origin));
}

void fragment() {
	ALBEDO = tint;
	ROUGHNESS = 1.0;
	ALPHA = opacity * 0.45 * smoothstep(0.0, 0.45, UV.y) * smoothstep(1.0, 0.85, UV.y);
}

void light() {
	DIFFUSE_LIGHT += LIGHT_COLOR * ATTENUATION * 0.35;
}
