shader_type spatial;
// Wet-air bloom around a lamp head: a camera-facing additive disc with a hot core and a wide soft
// skirt, gently breathing with the rain. Fog applied by hand (additive).
render_mode unshaded, cull_disabled, blend_add, depth_draw_never, shadows_disabled, fog_disabled;
uniform vec3 colour : source_color = vec3(1.0, 0.62, 0.26);
uniform float intensity = 1.4;
uniform float fog_density = 0.036;

void vertex() {
	// Billboard: keep the quad facing the camera.
	MODELVIEW_MATRIX = VIEW_MATRIX * mat4(INV_VIEW_MATRIX[0], INV_VIEW_MATRIX[1], INV_VIEW_MATRIX[2], MODEL_MATRIX[3]);
}

void fragment() {
	float r = length(UV * 2.0 - 1.0);
	float core = exp(-r * r * 30.0);
	float skirt = exp(-r * r * 4.0) * 0.35;
	float breathe = 0.92 + 0.08 * sin(TIME * 2.3 + VERTEX.x);
	float fog = exp(-length(VERTEX) * fog_density * 0.7);
	ALBEDO = colour * intensity * (core + skirt) * breathe * fog * smoothstep(1.0, 0.85, r);
}
