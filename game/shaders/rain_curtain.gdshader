shader_type spatial;
// Distant rain sheets: an open cylinder around the player drawing scrolling streak columns.
// Buildings occlude it (depth test), the fog thins it with distance, so the downpour reads
// as a wall of rain down the street at almost no cost. Gusts sweep brighter bands across it.
render_mode unshaded, cull_disabled, blend_mix, depth_draw_never, shadows_disabled;
uniform vec3 tint : source_color = vec3(0.58, 0.55, 0.50);
uniform float columns = 520.0;
uniform float speed = 2.6;
uniform float strength = 0.16;

float hash(float n) { return fract(sin(n * 91.345) * 47453.5453); }

void fragment() {
	float col = floor(UV.x * columns);
	float h = hash(col);
	float v = UV.y * mix(5.0, 9.0, h) - TIME * speed * mix(0.8, 1.3, hash(col + 7.0)) + h * 13.0;
	float streak = smoothstep(0.72, 1.0, fract(v)) * step(0.35, hash(col + 3.0));
	float edge = 1.0 - abs(fract(UV.x * columns) - 0.5) * 2.0;
	// Slow gust bands sweeping around the street.
	float gust = 0.55 + 0.45 * sin(UV.x * 18.0 - TIME * 0.7 + sin(UV.y * 3.0 + TIME * 0.3));
	float fade_v = smoothstep(0.0, 0.15, UV.y) * smoothstep(1.0, 0.7, UV.y);
	ALBEDO = tint;
	ALPHA = streak * edge * gust * fade_v * strength;
}
