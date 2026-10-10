shader_type spatial;
// Outdoor rain around the player (TownZone): each streak falls through a 12 m column and wraps,
// turned toward the camera around the vertical axis. Timing only, no per-frame CPU work.
render_mode unshaded, cull_disabled, blend_mix, depth_draw_never, shadows_disabled;
uniform float height = 12.0;
uniform float speed = 7.5;
uniform vec3 tint : source_color = vec3(0.62, 0.60, 0.55);
varying float opacity;

void vertex() {
	float fall = fract(INSTANCE_CUSTOM.r + TIME * speed * INSTANCE_CUSTOM.g / height);
	vec3 origin = (MODEL_MATRIX * vec4(0.0, height * (1.0 - fall) - 1.0, 0.0, 1.0)).xyz;
	vec3 to_camera = CAMERA_POSITION_WORLD - origin;
	to_camera.y = 0.0;
	vec3 side = normalize(cross(vec3(0.0, 1.0, 0.0), normalize(to_camera + vec3(0.0001))));
	vec3 world_vertex = origin + side * VERTEX.x + vec3(0.0, VERTEX.y, 0.0);
	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * vec4(world_vertex, 1.0);
	opacity = INSTANCE_CUSTOM.b;
}

void fragment() {
	ALBEDO = tint;
	ALPHA = opacity * 0.42 * smoothstep(0.0, 0.35, UV.y);
}
