import numpy as np
import pyassimp
import os

from OpenGL.GL import *
from OpenGL.arrays import vbo


class MeshVBO:
    def __init__(self, vertices, normals):
        self.vertex_count = len(vertices)

        self.vbo_vertices = vbo.VBO(
            np.array(vertices, dtype=np.float32)
        )

        self.vbo_normals = vbo.VBO(
            np.array(normals, dtype=np.float32)
        )

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        self.vbo_vertices.bind()
        glVertexPointer(3, GL_FLOAT, 0, self.vbo_vertices)

        self.vbo_normals.bind()
        glNormalPointer(GL_FLOAT, 0, self.vbo_normals)

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        self.vbo_vertices.unbind()
        self.vbo_normals.unbind()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)


class Model:
    def __init__(self, path):
        self.meshes = []

        vertices, normals = self.load_obj(path)
        self.meshes = [
            MeshVBO(vertices, normals)
        ]

    def load_obj(self, path):
        vertices_raw = []
        normals_raw = []

        vertices = []
        normals = []

        with open(path, "r", encoding="latin1") as f:
            for line in f:
                if line.startswith("v "):
                    x, y, z = map(float, line.split()[1:4])
                    vertices_raw.append([x, y, z])

                elif line.startswith("vn "):
                    x, y, z = map(float, line.split()[1:4])
                    normals_raw.append([x, y, z])

                elif line.startswith("f "):
                    parts = line.split()[1:]

                    triangles = []
                    for i in range(1, len(parts)-1):
                        triangles.append(parts[0])
                        triangles.append(parts[i])
                        triangles.append(parts[i+1])

                    for p in triangles:
                        vals = p.split("/")

                        v_idx = int(vals[0])
                        if v_idx < 0:
                            v_idx = len(vertices_raw) + v_idx

                        else:
                            v_idx -= 1

                        vertices.append(vertices_raw[v_idx])

                        if len(vals) >= 3 and vals[2] != "" and normals_raw:
                            n_idx = int(vals[2])
                            if n_idx < 0:
                                n_idx = len(normals_raw) + n_idx
                                
                            else:
                                n_idx -= 1

                            normals.append(normals_raw[n_idx])

                        else:
                            normals.append([0,1,0])

        return vertices, normals
    

    def draw(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
        glMaterialfv(GL_FRONT, GL_SHININESS, 32)

        glColor3f(0.7, 0.8, 1.0)

        for mesh in self.meshes:
            mesh.draw()