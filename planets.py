from geometries import Sphere
from textures import load_texture
from transform_matrices import *


class Earth(Sphere):
    def __init__(self):
        super().__init__(load_texture('textures/earth_2k.jpg'))

    def draw_planet(self, program_id, angle):
        Sphere.draw(self, program_id, apply_transformations([
            rotate_z(angle),
            translate(0.6, 0, 0),
            scale(0.15, 0.15, 0.15),
            rotate_y(270),
            rotate_x(angle)
        ]))


class Sun(Sphere):
    def __init__(self):
        super().__init__(load_texture('textures/2k_sun.jpg'))

    def draw_planet(self, program_id, angle):
        Sphere.draw(self, program_id, apply_transformations([
            scale(0.35, 0.35, 0.35),
            rotate_y(270)
        ]))
