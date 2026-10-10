shader_type spatial;
render_mode diffuse_lambert, cull_disabled;
uniform sampler2D albedo_tex : source_color, hint_default_white, filter_nearest, repeat_enable;
uniform vec4 base_color : source_color = vec4(1.0);
uniform bool foliage = false;
uniform bool wet_ground = false;
uniform float weather_time = 0.0;
uniform float wind_amount = 0.04;
uniform vec3 mist_color : source_color = vec3(0.34,0.39,0.39);
varying vec3 world_pos;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p);vec2 f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1)),f.x),f.y);}
void vertex() {
    world_pos = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz;
    if (foliage) {
        float breeze=sin(weather_time*.75+world_pos.x*.37+world_pos.z*.12)+.35*sin(weather_time*1.31+world_pos.z*.41);
        VERTEX.x+=breeze*wind_amount*UV.y;
    }
}
void fragment() {
    vec4 tex = texture(albedo_tex,UV)*base_color;
    float depth = max(-world_pos.z-8.0,0.0);
    // Low wet mist is deeper between trunks, without bleaching the nearer foliage.
    float low_mist=exp(-max(world_pos.y,0.0)*.32)*.11;
    float haze=clamp(1.0-exp(-depth*.024)+low_mist*smoothstep(10.0,35.0,depth),0.0,.91);
    vec3 surface=tex.rgb;
    float puddle=0.0;float ripple=0.0;
    if(wet_ground){
        puddle=smoothstep(.63,.77,noise(world_pos.xz*.55)+noise(world_pos.xz*1.7)*.17);
        vec2 cells=world_pos.xz*1.7;vec2 id=floor(cells);
        vec2 centre=vec2(.2+.6*hash(id),.2+.6*hash(id+13.0));
        float phase=fract(weather_time*(.75+hash(id)*.4)+hash(id+7.0));
        float radius=length(fract(cells)-centre);
        ripple=(1.0-smoothstep(.012,.035,abs(radius-phase*.45)))*(1.0-phase)*step(.55,hash(id));
        surface=mix(surface,mist_color*.65,puddle*.48);
    }
    ALBEDO=surface*(1.0-haze);
    EMISSION=mist_color*haze+mist_color*puddle*(.055+ripple*.10)*(1.0-haze);
    ROUGHNESS=mix(1.0,.4,puddle);
    SPECULAR=0.0;
    ALPHA=tex.a;
    ALPHA_SCISSOR_THRESHOLD=.45;
}
