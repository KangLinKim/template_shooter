from OpenGL.GL import *
from model import Model

import math

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

        glRotatef(pitch, 1, 0, 0)
        glRotatef(yaw, 0, 1, 0)

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
    
    def change_weapon(self, fbx_path):

        print("weapon changed:", fbx_path)

        self.weapon_model = Model(fbx_path)

    def get_forward_vector(self):

        yaw = math.radians(self.rotation[1])

        x = math.sin(yaw)
        z = -math.cos(yaw)

        return [x, 0, z]

    def get_right_vector(self):

        yaw = math.radians(self.rotation[1])

        x = math.cos(yaw)
        z = math.sin(yaw)

        return [x, 0, z]

    def move(self, forward, right, speed):

        f = self.get_forward_vector()
        r = self.get_right_vector()

        self.position[0] += (f[0] * forward + r[0] * right) * speed
        self.position[2] += (f[2] * forward + r[2] * right) * speed

    def get_muzzle(self):

        yaw = math.radians(self.rotation[1])
        pitch = math.radians(self.rotation[0])

        direction = [
            math.sin(yaw) * math.cos(pitch),
            -math.sin(pitch),
            -math.cos(yaw) * math.cos(pitch)
        ]

        muzzle_distance = 1.0

        position = [
            self.position[0] + direction[0] * muzzle_distance,
            self.position[1] + direction[1] * muzzle_distance - 0.3,
            self.position[2] + direction[2] * muzzle_distance
        ]

        return position, direction