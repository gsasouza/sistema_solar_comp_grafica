from glfw.GLFW import *
from transform_matrices import *


def rotate_planet(planet, key):
    if key == GLFW_KEY_A:
        new_matrix = apply_transformations([rotate_x(1), planet.matrix])
    else:
        new_matrix = apply_transformations([rotate_x(-1), planet.matrix])
    planet.set_matrix(new_matrix)


def scale_planet(planet, key):
    if key == GLFW_KEY_W:
        new_matrix = apply_transformations([scale(1.1, 1.1, 1.1), planet.matrix])
    else:
        new_matrix = apply_transformations([scale(0.9, 0.9, 0.9), planet.matrix])
    planet.set_matrix(new_matrix)


def translate_rocket(rocket, key):
    if key == GLFW_KEY_UP:
        new_matrix = apply_transformations([translate(0.0,  0.1, 0), rocket.matrix])
    elif key == GLFW_KEY_DOWN:
        new_matrix = apply_transformations([translate(0.0, -0.1, 0.0), rocket.matrix])
    elif key == GLFW_KEY_LEFT:
        new_matrix = apply_transformations([translate(-0.1, 0.0, 0.0), rocket.matrix])
    else:
        new_matrix = apply_transformations([translate(0.1, 0.0, 0.0), rocket.matrix])

    rocket.set_matrix(new_matrix)


def create_callback(mars, sun, earth, blackhole):

    def callback_handler(window, key, scancode, action, mods):
        if key == GLFW_KEY_R:
            blackhole.start = False
            sun.matrix = np.identity(4)
        elif key == GLFW_KEY_A or key == GLFW_KEY_D:
            rotate_planet(mars, key)
        elif key == GLFW_KEY_W or key == GLFW_KEY_S:
            scale_planet(sun, key)
        elif key == GLFW_KEY_UP or key == GLFW_KEY_DOWN or key == GLFW_KEY_LEFT or key == GLFW_KEY_RIGHT:
            translate_rocket(earth, key)

        if sun.matrix[0][0] < 0.2:
            blackhole.start = True

    return callback_handler
