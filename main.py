import math

import numpy as np
from OpenGL.GL import *
import glfw
from window import create_glfw_window
from shaders import load_shaders
from planets import *

from geometries import *


def read_file(filename):
    data = ''
    with open(filename, 'r') as file:
        data = file.read()
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = create_glfw_window(720, 720)

    program_id = load_shaders(read_file('shaders/triangle_vert.glsl'), read_file('shaders/triangle_frag.glsl'))

    glUseProgram(program_id)

    sun = Sun()
    sun.prepare(program_id)

    mars = Mars()
    mars.prepare(program_id)

    earth = Earth()
    earth.prepare(program_id)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)

    angle = 0

    while not glfw.window_should_close(window):
        glClearColor(0.055, 0.11, 0.271, 1.0)
        glfw.poll_events()

        angle += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # cylinder.draw(program_id, np.identity(4))
        #
        earth.draw_planet(program_id, angle)
        sun.draw_planet(program_id, angle)

        mars.draw_planet(program_id, angle)

        glfw.swap_buffers(window)

    glfw.terminate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
