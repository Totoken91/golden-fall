shader_type canvas_item;
// Native-resolution view of the physical CRT once the camera has zoomed in.
// Kept subtle on purpose: the text must stay readable, the glass only adds mood.
uniform float curvature = 0.022;
uniform float scan_strength = 0.10;
uniform float glow_strength = 0.16;
uniform float flicker = 0.006;
uniform vec2 source_size = vec2(640.0, 480.0);

vec2 barrel(vec2 uv) {
	vec2 c = uv * 2.0 - 1.0;
	c *= 1.0 + curvature * dot(c, c);
	return c * 0.5 + 0.5;
}

void fragment() {
	vec2 uv = barrel(UV);
	vec2 inside = step(vec2(0.0), uv) * step(uv, vec2(1.0));
	vec2 texel = 1.0 / source_size;
	vec3 base = texture(TEXTURE, uv).rgb;
	// Cheap phosphor bloom: wide taps, mostly lifts bright windows and text halos.
	vec3 bloom = vec3(0.0);
	for (int i = 0; i < 8; i++) {
		float a = float(i) * 0.785398;
		bloom += texture(TEXTURE, uv + vec2(cos(a), sin(a)) * texel * 2.6).rgb;
	}
	bloom /= 8.0;
	vec3 color = base + bloom * bloom * glow_strength;
	// Scanlines locked to the 480 desktop lines, soft enough to avoid moiré.
	float line = 0.5 + 0.5 * cos(uv.y * source_size.y * 6.2831853);
	color *= 1.0 - scan_strength * line * (1.0 - dot(base, vec3(0.33)) * 0.6);
	// Faint aperture grille.
	float column = mod(FRAGCOORD.x, 3.0);
	color *= vec3(column < 1.0 ? 1.03 : 0.985, column >= 1.0 && column < 2.0 ? 1.03 : 0.985, column >= 2.0 ? 1.03 : 0.985);
	// Slow rolling hum bar and mains flicker.
	float roll = fract(uv.y * 0.6 - TIME * 0.045);
	color *= 1.0 + 0.022 * smoothstep(0.0, 0.08, roll) * (1.0 - smoothstep(0.08, 0.22, roll));
	color *= 1.0 + flicker * sin(TIME * 59.0);
	// Glass: vignette, warm phosphor, cool reflection of the window in the top-left.
	vec2 e = uv * 2.0 - 1.0;
	color *= 1.0 - 0.28 * pow(length(e * vec2(0.82, 0.9)), 3.2);
	color *= vec3(1.02, 1.0, 0.965);
	float sheen = smoothstep(0.55, 0.0, length((UV - vec2(0.18, 0.12)) * vec2(1.0, 1.6)));
	color += vec3(0.55, 0.62, 0.66) * sheen * 0.045;
	// Rounded tube corners.
	vec2 q = abs(e) - vec2(0.94);
	float corner = length(max(q, 0.0)) / 0.06;
	float mask = inside.x * inside.y * (1.0 - smoothstep(0.85, 1.0, corner));
	// Outside the curved picture is opaque dark glass, so the low-res in-world screen never shows through.
	vec2 o = abs(UV * 2.0 - 1.0) - vec2(0.97);
	float outer = 1.0 - smoothstep(0.0, 0.03, length(max(o, 0.0)));
	vec3 glass = vec3(0.025, 0.03, 0.03) + vec3(0.04) * sheen;
	// COLOR.a carries the node modulate, used to cross-fade with the in-world screen.
	COLOR = vec4(mix(glass, color, mask), COLOR.a * outer);
}
