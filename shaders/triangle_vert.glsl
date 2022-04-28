
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 in_uv;

uniform mat4 mat_transformation;

out vec2 uv;

void main()
{
    gl_Position = mat_transformation * vec4(position.x, position.y, position.z, 1.0);
    uv = in_uv;
}