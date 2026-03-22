from OpenGL.GL import *
from model import Model


class Player:
    def __init__(self, fbx_path):
        self.weapon_model = Model(fbx_path)

        self.rotation = [0.0, 0.0]
        self.position = [0.0, 1.7, 0.0]

        self.weapon_offset = [0.4, -0.3, -0.6]
        self.weapon_scale = 1.4

    def apply_camera(self):
        pitch, yaw = self.rotation
        x, y, z = self.position

        glRotatef(-pitch, 1, 0, 0)
        glRotatef(-yaw, 0, 1, 0)

        glTranslatef(-x, -y, -z)

    def rotate_yaw(self, amount):
        self.rotation[1] += amount

    def rotate_pitch(self, amount):
        self.rotation[0] += amount

        if self.rotation[0] > 89:
            self.rotation[0] = 89

        if self.rotation[0] < -89:
            self.rotation[0] = -89

    def draw_weapon(self):
        glPushMatrix()
        glLoadIdentity()

        glTranslatef(
            self.weapon_offset[0],
            self.weapon_offset[1],
            self.weapon_offset[2]
        )

        glRotatef(-180, 0, 1, 0)
        glRotatef(-10, 0, 1, 0)

        glScalef(
            self.weapon_scale,
            self.weapon_scale,
            self.weapon_scale
        )

        self.weapon_model.draw()

        glPopMatrix()