#version 460 core

in vec2 uv;

uniform sampler2D texture_sampler;

out vec4 out_color;

void main()
{
	vec3 texture_color = texture(texture_sampler, uv).rgb;
	out_color = vec4(texture_color, 1.0);
}