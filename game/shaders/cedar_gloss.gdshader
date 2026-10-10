shader_type canvas_item;
// Glossy mid-2000s surface for Cedar 03: vertical gradient, top highlight band, rounded corners.
uniform vec4 top_color : source_color = vec4(0.30, 0.52, 0.55, 1.0);
uniform vec4 bottom_color : source_color = vec4(0.12, 0.26, 0.29, 1.0);
uniform vec4 border_color : source_color = vec4(0.07, 0.15, 0.17, 1.0);
uniform vec2 rect_size = vec2(100.0, 28.0);
uniform float radius = 6.0;
uniform float border_width = 1.0;
uniform float gloss = 1.0;
uniform bool round_bottom = false;

void fragment() {
	vec2 p = UV * rect_size;
	vec2 half_size = rect_size * 0.5;
	float r = (!round_bottom && p.y > half_size.y) ? 0.0 : radius;
	vec2 q = abs(p - half_size) - (half_size - vec2(r));
	float d = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
	float coverage = clamp(0.5 - d, 0.0, 1.0);
	float t = UV.y;
	vec3 c = mix(top_color.rgb, bottom_color.rgb, smoothstep(0.0, 1.0, t));
	// Glass band across the upper half, brighter lip on the first pixel row.
	c = mix(c, c + vec3(0.16), gloss * (1.0 - smoothstep(0.38, 0.5, t)) * (0.55 + 0.45 * (1.0 - t * 2.0)));
	c += gloss * vec3(0.20) * (1.0 - smoothstep(0.0, 1.6, p.y - border_width));
	c += gloss * vec3(0.05) * smoothstep(0.75, 1.0, t);
	float edge = clamp(0.5 - (d + border_width), 0.0, 1.0);
	c = mix(border_color.rgb, c, edge);
	COLOR = vec4(c, coverage * mix(top_color.a, bottom_color.a, t));
}
