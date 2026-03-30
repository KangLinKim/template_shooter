import math
from OpenGL.GL import *


class Bullet:
    def __init__(self, position, direction, size, damage, color):
        self.position = list(position)
        self.direction = direction

        self.speed = 0.8
        self.life = 3.0

        self.size = size
        self.damage = damage
        self.color = color

        self.radius = size

    def update(self, dt):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.position[2] += self.direction[2] * self.speed

        self.life -= dt

    def draw(self):
        x, y, z = self.position

        glPushMatrix()

        glTranslatef(x, y, z)
        glScalef(self.size, self.size, self.size)

        glColor3f(*self.color)

        glBegin(GL_QUADS)

        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)

        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)

        glEnd()

        glPopMatrix()