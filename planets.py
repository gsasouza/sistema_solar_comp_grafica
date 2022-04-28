from geometries import Sphere
from textures import load_texture
from transform_matrices import *


class Earth(Sphere):
    def __init__(self):
        super().__init__(load_texture('textures/earth_2k.jpg'))

    def get_base_matrix(self, angle):
        return apply_transformations([
            rotate_z(angle),
            translate(0.6, 0, 0),
            scale(0.15, 0.15, 0.15),
            rotate_y(270),
            rotate_x(angle)
        ])


class Mars(Sphere):
    def __init__(self):
        super().__init__(load_texture('textures/2k_mars.jpg'))

    def get_base_matrix(self, angle):
        return apply_transformations([
            rotate_z(angle),
            translate(-0.8, 0, 0),
            scale(0.08, 0.08, 0.08),
            rotate_y(270)
        ])


class Sun(Sphere):
    def __init__(self):
        super().__init__(load_texture('textures/2k_sun.jpg'))

    def get_base_matrix(self):
        return apply_transformations([
            scale(0.35, 0.35, 0.35),
            rotate_y(270)
        ])


class Blackhole(Sphere):
    def __init__(self):
        self.size = 0.01
        self.start = False
        self.matrix = translate(0, 0, -1)
        super().__init__(load_texture('textures/black.jpg'))

    def get_base_matrix(self):
        if self.matrix[0][0] < 25:
            self.matrix = apply_transformations([self.matrix, scale(1.2, 1.2, 1.2)])

        return apply_transformations([scale(self.size, self.size, self.size)])
