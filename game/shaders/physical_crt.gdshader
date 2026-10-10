shader_type spatial;
render_mode unshaded, cull_disabled;
uniform sampler2D desktop_tex : source_color, filter_nearest, repeat_disable;
// 1 while the native-resolution view sits on top: the tube shows only dark glass behind it.
uniform float covered = 0.0;

void fragment() {
	vec3 image = texture(desktop_tex, UV).rgb;
	float scanline = mix(.94,1.0,step(.5,fract(UV.y*240.0)));
	vec2 edge = abs(UV*2.0-1.0);
	float glass = 1.0-.06*pow(max(edge.x,edge.y),4.0);
	// V0.20: slightly brighter tube so the screen reads as the light source of the desk.
	ALBEDO = mix(image*scanline*glass*.97, vec3(.025,.03,.03), covered);
}
