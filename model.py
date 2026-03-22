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

        file_type = os.path.basename(path)
        if file_type.startswith("SMG"):
            unload_index = 4
        elif file_type.startswith("ShotGun"):
            unload_index = None
        elif file_type.startswith("Pistol"):
            unload_index = 2

        with pyassimp.load(path) as scene:

            for mesh_idx, mesh in enumerate(scene.meshes):
                    
                if mesh_idx != unload_index:
                    vertices = []
                    normals = []

                    for face in mesh.faces:

                        if len(face) != 3:
                            continue

                        for index in face:

                            v = mesh.vertices[index]
                            vertices.append(v)

                            if mesh.normals is not None:
                                normals.append(mesh.normals[index])
                            else:
                                normals.append([0, 1, 0])

                    self.meshes.append(
                        MeshVBO(vertices, normals)
                    )

    def draw(self):

        glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
        glMaterialfv(GL_FRONT, GL_SHININESS, 32)

        glColor3f(0.7, 0.8, 1.0)

        for mesh in self.meshes:
            mesh.draw()