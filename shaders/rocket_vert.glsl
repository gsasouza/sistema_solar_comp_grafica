#version 460 core

attribute vec3 position;
uniform mat4 mat_transformation;

void main(){
    gl_Position = mat_transformation * vec4(position, 1.0);
}