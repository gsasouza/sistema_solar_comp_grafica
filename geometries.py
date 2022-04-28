import math
import numpy as np
from OpenGL.GL import *
import random
from transform_matrices import apply_transformations, translate, scale


class Sphere:
    def __init__(self, texture_id):
        self.offset = 0
        self.stride = 0
        self.texture_id = texture_id
        self.position = None
        self.vertices = self.create()
        self.vao = None
        self.buffer = None
        self.matrix = np.identity(4);

    def set_matrix(self, matrix):
        self.matrix = matrix

    def get_sphere_coordinates_by_angle(self, u, v, r, s, t):
        x = r * math.sin(v) * math.cos(u)
        y = r * math.sin(v) * math.sin(u)
        z = r * math.cos(v)

        return x, y, z, s, t

    def create(self):
        r = 1
        resolution = 150  # qtd de sectors (longitude)

        sector_step = (math.pi * 2) / resolution  # variar de 0 até 2π
        stack_step = math.pi / resolution  # variar de 0 até π

        vertices_list = []
        for i in range(0, resolution):  # para cada sector (longitude)
            s = i / (resolution - 1)
            for j in range(0, resolution):  # para cada stack (latitude)
                t = j / (resolution - 1)
                u = i * sector_step  # angulo setor
                v = j * stack_step  # angulo stack

                un = 0  # angulo do proximo sector
                if i + 1 == resolution:
                    un = math.pi * 2
                else:
                    un = (i + 1) * sector_step

                vn = 0  # angulo do proximo stack
                if j + 1 == resolution:
                    vn = math.pi
                else:
                    vn = (j + 1) * stack_step

                # verticies do poligono
                p0 = self.get_sphere_coordinates_by_angle(u, v, r, s, t)
                p1 = self.get_sphere_coordinates_by_angle(u, vn, r, s, t)
                p2 = self.get_sphere_coordinates_by_angle(un, v, r, s, t)
                p3 = self.get_sphere_coordinates_by_angle(un, vn, r, s, t)

                # triangulo 1 (primeira parte do poligono)
                vertices_list.append(p0)
                vertices_list.append(p2)
                vertices_list.append(p1)

                # triangulo 2 (segunda e ultima parte do poligono)
                vertices_list.append(p3)
                vertices_list.append(p1)
                vertices_list.append(p2)

        total_vertices = len(vertices_list)

        vertices = np.zeros(total_vertices, [("position", np.float32, 5)])

        vertices['position'] = np.array(vertices_list)

        return vertices

    def prepare(self, program_id):

        # Create VAO
        self.vao = glGenVertexArrays(1)
        self.buffer = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        # Enable vertex attributes
        stride = self.vertices.strides[0]

        position = glGetAttribLocation(program_id, "position")
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))

        uv = glGetAttribLocation(program_id, "in_uv")
        glEnableVertexAttribArray(uv)
        glVertexAttribPointer(uv, 2, GL_FLOAT, False, stride, ctypes.c_void_p(12))
        glBindVertexArray(0)

    def draw(self, program_id, t_mat):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBindVertexArray(self.vao)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUniformMatrix4fv(glGetUniformLocation(program_id, "mat_transformation"), 1, GL_TRUE,
                           apply_transformations([self.matrix, t_mat, ]))
        texture_sampler = glGetUniformLocation(program_id, "texture_sampler")

        glUniform1i(texture_sampler, 0)

        for triangle in range(0, len(self.vertices), 3):
            glDrawArrays(GL_TRIANGLES, triangle, 5)

        glBindVertexArray(0);


class Cube:
    def __init__(self):
        self.offset = 0
        self.stride = 0
        self.position = None
        self.vertices = self.create()
        self.buffer = None
        self.vao = None
        self.matrix = apply_transformations([
            translate(-1 + 2 * np.random.rand(), -1 + 2 * np.random.rand(), -1),
            scale(0.02, 0.02, 0.02)
        ])

    def create(self):
        vertices = np.zeros(24, [("position", np.float32, 3)])
        vertices['position'] = [
            # Face 1 do Cubo (vértices do quadrado)
            (-0.5, -0.5, +0.5),
            (+0.5, -0.5, +0.5),
            (-0.5, +0.5, +0.5),
            (+0.5, +0.5, +0.5),

            # Face 2 do Cubo
            (+0.5, -0.5, +0.5),
            (+0.5, -0.5, -0.5),
            (+0.5, +0.5, +0.5),
            (+0.5, +0.5, -0.5),

            # Face 3 do Cubo
            (+0.5, -0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (+0.5, +0.5, -0.5),
            (-0.5, +0.5, -0.5),

            # Face 4 do Cubo
            (-0.5, -0.5, -0.5),
            (-0.5, -0.5, +0.5),
            (-0.5, +0.5, -0.5),
            (-0.5, +0.5, +0.5),

            # Face 5 do Cubo
            (-0.5, -0.5, -0.5),
            (+0.5, -0.5, -0.5),
            (-0.5, -0.5, +0.5),
            (+0.5, -0.5, +0.5),

            # Face 6 do Cubo
            (-0.5, +0.5, +0.5),
            (+0.5, +0.5, +0.5),
            (-0.5, +0.5, -0.5),
            (+0.5, +0.5, -0.5)
        ]
        return vertices

    def prepare(self, program_id):
        # Create VAO
        self.vao = glGenVertexArrays(1)
        self.buffer = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

        stride = self.vertices.strides[0]

        position = glGetAttribLocation(program_id, "position")
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))
        glBindVertexArray(0)

    def draw(self, program_id, t_mat=np.identity(4)):
        glBindVertexArray(self.vao)

        glUniformMatrix4fv(glGetUniformLocation(program_id, "mat_transformation"), 1, GL_TRUE,
                           apply_transformations([self.matrix, t_mat]))

        glUniform4f(glGetUniformLocation(program_id, "color"), 1, 1, 1, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glUniform4f(glGetUniformLocation(program_id, "color"), 0.851, 0.957, 1.0, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
        glUniform4f(glGetUniformLocation(program_id, "color"), 0.816, 1.0, 1.0, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glUniform4f(glGetUniformLocation(program_id, "color"), 0.8, 0.8, 0.8, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glUniform4f(glGetUniformLocation(program_id, "color"), 0.569, 0.678, 0.714, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        glUniform4f(glGetUniformLocation(program_id, "color"), 0.8, 0.9, 0.9, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)
        glBindVertexArray(0)


class Cylinder:
    def __init__(self):
        self.offset = 0
        self.stride = 0
        self.color = None
        self.texture_id = None
        self.position = None
        self.vao = None
        self.vertices = self.create()

    def get_cylinder_coordinates_by_angle(self, u, h, r):
        x = r * math.cos(u)
        y = r * math.sin(u)
        z = h
        return x, y, z

    def create(self):
        r = 0.08
        num_sectors = 20
        num_stacks = 10
        h = 0.4

        sector_step = (math.pi * 2) / num_sectors
        stack_step = h / num_stacks

        vertices_list = []
        for j in range(num_stacks):
            for i in range(num_sectors):
                sector_angle = i * sector_step
                stack_height = j * stack_step

                next_sector_angle = 0
                if i + 1 == num_sectors:
                    next_sector_angle = math.pi * 2
                else:
                    next_sector_angle = (i + 1) * sector_step

                next_stack_height = 0
                if j + 1 == num_stacks:
                    next_stack_height = h
                else:
                    next_stack_height = (j + 1) * stack_step

                # vertices do poligono
                p0 = self.get_cylinder_coordinates_by_angle(sector_angle, stack_height, r)
                p1 = self.get_cylinder_coordinates_by_angle(sector_angle, next_stack_height, r)
                p2 = self.get_cylinder_coordinates_by_angle(next_sector_angle, stack_height, r)
                p3 = self.get_cylinder_coordinates_by_angle(next_sector_angle, next_stack_height, r)

                # triangulo 1 (primeira parte do poligono)
                vertices_list.append(p0)
                vertices_list.append(p2)
                vertices_list.append(p1)

                # triangulo 2 (segunda e ultima parte do poligono)
                vertices_list.append(p3)
                vertices_list.append(p1)
                vertices_list.append(p2)

                if stack_height == 0:
                    vertices_list.append(p0)
                    vertices_list.append(p2)
                    vertices_list.append(self.get_cylinder_coordinates_by_angle(0, stack_height, 0))

                if next_stack_height == h:
                    # faz um triangulo a partir do mesmo angulo u, mas com as alturas em h = vn
                    vertices_list.append(p1)
                    vertices_list.append(p3)
                    vertices_list.append(self.get_cylinder_coordinates_by_angle(0, next_stack_height, 0))

        total_vertices = len(vertices_list)
        vertices = np.zeros(total_vertices, [("position", np.float32, 3)])
        vertices['position'] = np.array(vertices_list)

        return vertices

    def prepare(self, program_id):
        buffer = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        stride = self.vertices.strides[0]
        self.offset = ctypes.c_void_p(0)

        self.position = glGetAttribLocation(program_id, "position")
        self.color = glGetUniformLocation(program_id, "color")

        glEnableVertexAttribArray(self.position)
        glVertexAttribPointer(self.position, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))
        glBindVertexArray(0)

    def draw(self, program_id, t_mat):
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(program_id, "mat_transformation"), 1, GL_TRUE, t_mat)

        for triangle in range(0, len(self.vertices), 3):
            glUniform4f(self.color, 0.2, 0.2, 0.2, 1.0)
            glDrawArrays(GL_TRIANGLES, triangle, 3)
