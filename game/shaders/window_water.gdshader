shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never, shadows_disabled;
uniform sampler2D grime_tex : source_color, filter_nearest;
uniform float weather_time = 0.0;
float hash(vec2 p) {return fract(sin(dot(p,vec2(93.7,157.3)))*15381.31);}
void fragment() {
    vec4 grime=texture(grime_tex,UV);
    // Sparse meandering rivulets, rather than evenly spaced straight lines.
    float column=floor(UV.x*17.0);
    float seed=hash(vec2(column,2.0));
    float centre=.2+.6*seed+sin(UV.y*19.0+seed*31.0)*.075;
    float dx=fract(UV.x*17.0)-centre;
    float head=fract(UV.y*1.6-weather_time*(.07+seed*.09)+seed);
    float run=(1.0-smoothstep(0.0,.24,head))*(1.0-smoothstep(.008,.027,abs(dx)))*step(.36,seed);
    vec2 p=UV*vec2(39.0,31.0);vec2 cell=floor(p);
    vec2 offset=vec2(.18+.64*hash(cell),.18+.64*hash(cell+13.0));
    vec2 bead_delta=(fract(p)-offset)*vec2(1.0,1.35);
    float radius=.055+.045*hash(cell+7.0);
    float bead=1.0-smoothstep(radius,radius+.04,length(bead_delta));
    float glint=1.0-smoothstep(.018,.052,length(bead_delta+vec2(.025,.035)));
    float lifetime=sin(weather_time*(.12+hash(cell)*.15)+hash(cell+17.0)*6.283)*.5+.5;
    float present=step(.66,hash(cell+31.0))*smoothstep(.12,.3,lifetime);
    ALBEDO=mix(vec3(.25,.33,.32),vec3(.67,.72,.66),clamp(glint+run*.8,0.0,1.0));
    ALPHA=clamp(grime.a+run*.16+(bead*.11+glint*.13)*present,0.0,.31);
}
