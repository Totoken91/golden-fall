shader_type canvas_item;
render_mode unshaded;
uniform float levels = 31.0;
uniform float strength = 1.0;
float threshold(ivec2 p) {
 int b[16] = int[16](0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5);
 return (float(b[(p.y % 4)*4 + (p.x % 4)])+.5)/16.0-.5;
}
void fragment() {
 vec4 c=texture(TEXTURE,UV);
 float d=threshold(ivec2(floor(UV*vec2(textureSize(TEXTURE,0)))));
 c.rgb=clamp(floor(c.rgb*levels+.5+d*strength)/levels,0.0,1.0);
 COLOR=c;
}
