import math
import numpy as np


def transform(m, v):
    return np.asarray(m * np.asmatrix(v).T)[:, 0]


def magnitude(v):
    return math.sqrt(np.sum(v ** 2))


def normalize(v):
    m = magnitude(v)
    if m == 0:
        return v
    return v / m


def ortho(l, r, b, t, n, f):
    dx = r - l
    dy = t - b
    dz = f - n
    rx = -(r + l) / (r - l)
    ry = -(t + b) / (t - b)
    rz = -(f + n) / (f - n)


def translate(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def scale(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])


def rotate_z(angle):
    return np.array([
        [math.cos(np.radians(angle)), -math.sin(np.radians(angle)), 0, 0],
        [math.sin(np.radians(angle)), math.cos(np.radians(angle)), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def rotate_x(angle):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(np.radians(angle)), -math.sin(np.radians(angle)), 0],
        [0, math.sin(np.radians(angle)), math.cos(np.radians(angle)), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(angle):
    return np.array([
        [math.cos(np.radians(angle)), 0, math.sin(np.radians(angle)), 0],
        [0, 1, 0, 0],
        [-math.sin(np.radians(angle)), 0, math.cos(np.radians(angle)), 0],
        [0, 0, 0, 1]
    ])


def apply_transformations(matrices):
    result = np.identity(4);
    for matrix in matrices:
        result = np.dot(result, matrix)

    return result
