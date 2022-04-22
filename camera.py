import numpy as np


class Camera:

    def __init__(self):
        self.location = np.array([0.0, 0.0, 10.0])
        self.direction = np.array([0.0, 0.0, -1.0])

        self.up = np.array([0.0, 1.0, 0.0])
        self.speed = 1.0
        self.sensivity = 0.1

        self.field_of_view = np.radians(45)
        self.aspect_ration = 19 / 9
        self.near = 0.01
        self.far = 1000.0

    def move_forward(self, amount):
        result_matrix = np.dot(self.location, amount * self.speed)
        self.location = np.sum(self.location, result_matrix)

    def move_right(self, anmout):
