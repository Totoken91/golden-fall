shader_type spatial;
render_mode unshaded, cull_disabled, shadows_disabled, fog_disabled;
uniform float weather_time=0.0;
varying vec3 world_pos;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p);vec2 f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1)),f.x),f.y);}
void vertex(){world_pos=(MODEL_MATRIX*vec4(VERTEX,1)).xyz;}
void fragment(){
    vec2 p=vec2(world_pos.x*.043,world_pos.y*.08)+vec2(weather_time*.003,0.0);
    float cloud=noise(p)*.55+noise(p*2.7+9.0)*.29+noise(p*6.1)*.16;
    cloud=floor(cloud*18.0)/18.0;
    float elevation=smoothstep(0.0,35.0,world_pos.y);
    vec3 low=vec3(.40,.46,.45);vec3 high=vec3(.25,.30,.31);
    ALBEDO=mix(low,high,elevation)+(cloud-.5)*.075;
}
