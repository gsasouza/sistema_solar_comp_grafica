import math

import numpy as np
from OpenGL.GL import *
import glfw
from window import create_glfw_window
from shaders import load_shaders
from planets import *
from callbacks import create_callback
from geometries import *


def read_file(filename):
    data = ''
    with open(filename, 'r') as file:
        data = file.read()
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = create_glfw_window(720, 720)

    texture_program_id = load_shaders(read_file('shaders/texture_vert.glsl'), read_file('shaders/texture_frag.glsl'))
    color_program_id = load_shaders(read_file('shaders/color_vert.glsl'), read_file('shaders/color_frag.glsl'))

    sun = Sun()
    sun.prepare(texture_program_id)

    mars = Mars()
    mars.prepare(texture_program_id)

    earth = Earth()
    earth.prepare(texture_program_id)

    blackhole = Blackhole()
    blackhole.prepare(texture_program_id)

    cubes = []
    for _ in range(20):
        cube = Cube()
        cube.prepare(color_program_id)
        cubes.append(cube)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)

    angle = 0

    callback_handler = create_callback(mars, sun, earth, blackhole)
    glfw.set_key_callback(window, callback_handler)

    while not glfw.window_should_close(window):
        glClearColor(0.055, 0.11, 0.271, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfw.poll_events()

        angle += 1
        glUseProgram(color_program_id)
        for cube in cubes:
            cube_mat = apply_transformations([
                rotate_x(angle),
                rotate_z(angle),
            ])

            if blackhole.start:
                cube.matrix = drag_to_center(cube.matrix, 0.1)

            cube.draw(color_program_id, cube_mat)

        glUseProgram(texture_program_id)

        if blackhole.start:
            blackhole.draw(texture_program_id, blackhole.get_base_matrix())
        else:
            earth.draw(texture_program_id, earth.get_base_matrix(angle))
            sun.draw(texture_program_id, sun.get_base_matrix())
            mars.draw(texture_program_id, mars.get_base_matrix(angle))

        glfw.swap_buffers(window)

    glfw.terminate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
