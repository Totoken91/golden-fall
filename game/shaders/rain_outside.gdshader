shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;
uniform float opacity = 0.5;
varying vec2 variation;
void vertex() { variation=INSTANCE_CUSTOM.rg; }
void fragment() {
    // One world-space drop per quad; no tiled pattern.
    float taper=mix(.25,1.0,sin(UV.y*3.14159));
    float edge=1.0-smoothstep(.15*taper,.49*taper,abs(UV.x-.5));
    float ends=smoothstep(0.0,.15,UV.y)*(1.0-smoothstep(.70,1.0,UV.y));
    ALBEDO=mix(vec3(.40,.47,.46),vec3(.68,.74,.69),variation.g);
    ALPHA=edge*ends*opacity*variation.r;
}
