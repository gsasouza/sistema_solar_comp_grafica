import math
import numpy as np
from OpenGL.GL import *
import random


class Sphere:
    def __init__(self, texture_id):
        self.offset = 0
        self.stride = 0
        self.texture_id = texture_id
        self.position = None
        self.vertices = self.create()

    def get_sphere_coordinates_by_angle(self, u, v, r, s, t):
        x = r * math.sin(v) * math.cos(u)
        y = r * math.sin(v) * math.sin(u)
        z = r * math.cos(v)

        return x, y, z,  s,  t


    def create(self):
        r = 1
        resolution = 150  # qtd de sectors (longitude)

        # grid sectos vs stacks (longitude vs latitude)
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
        buffer = glGenBuffers(1)
        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        stride = self.vertices.strides[0]

        self.position = glGetAttribLocation(program_id, "position")

        glEnableVertexAttribArray(self.position)
        glVertexAttribPointer(self.position, 3, GL_FLOAT, False, stride,ctypes.c_void_p(0))

        uv = glGetAttribLocation(program_id, "in_uv")

        glEnableVertexAttribArray(uv)

        glVertexAttribPointer(uv, 2, GL_FLOAT, False, stride, ctypes.c_void_p(12))


    def draw(self, program_id, t_mat):
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, self.texture_id);
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

        glUniformMatrix4fv(glGetUniformLocation(program_id, "mat_transformation"), 1, GL_TRUE, t_mat)
        texture_sampler = glGetUniformLocation(program_id, "texture_sampler")
        glUniform1i(texture_sampler, 0);



        for triangle in range(0, len(self.vertices), 3):
            glDrawArrays(GL_TRIANGLES, triangle, 5)







