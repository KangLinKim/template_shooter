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
        self.health = 100

        self.hit_timer = 0
        self.hit_duration = 0.25
        self.dead = False

        self.walk_time = 0.0
        self.walk_bob = 0.0
        self.walking = False

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

        bob = self.walk_bob

        glTranslatef(
            self.weapon_offset[0],
            self.weapon_offset[1] + bob,
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

        move_x = (f[0] * forward + r[0] * right) * speed
        move_z = (f[2] * forward + r[2] * right) * speed

        self.position[0] += move_x
        self.position[2] += move_z

        if abs(move_x) > 0.0001 or abs(move_z) > 0.0001:
            self.walking = True
        else:
            self.walking = False

    def get_muzzle(self):
        yaw = math.radians(self.rotation[1])
        pitch = math.radians(self.rotation[0])

        direction = [
            math.sin(yaw) * math.cos(pitch),
            -math.sin(pitch),
            -math.cos(yaw) * math.cos(pitch)
        ]

        muzzle_distance = 0.2

        ox, oy, oz = self.weapon_offset

        offset_x = ox * math.cos(yaw) - oz * math.sin(yaw)
        offset_z = ox * math.sin(yaw) + oz * math.cos(yaw)

        position = [
            self.position[0] + direction[0] * muzzle_distance + offset_x,
            self.position[1] + direction[1] * muzzle_distance + oy,
            self.position[2] + direction[2] * muzzle_distance + offset_z
        ]

        return position, direction
    
    def take_damage(self, damage):
        if self.dead:
            return

        self.health -= damage
        self.hit_timer = 0.25

        # print("player hit:", self.health)

        if self.health <= 0:
            self.health = 0
            self.dead = True
            print("PLAYER DEAD")

    def update(self, dt):
        if self.hit_timer > 0:
            self.hit_timer -= dt

        if self.walking:
            self.walk_time += dt * 8
            self.walk_bob = math.sin(self.walk_time) * 0.03
        else:
            self.walk_bob *= 0.8

    def draw_hit_effect(self, width, height):
        if self.hit_timer <= 0:
            return

        alpha = self.hit_timer / self.hit_duration

        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(1, 0, 0, 0.35 * alpha)

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(width, 0)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)