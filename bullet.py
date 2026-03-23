import math
from OpenGL.GL import *


class Bullet:
    def __init__(self, position, direction, size, damage):
        self.position = list(position)
        self.direction = direction

        self.speed = 0.8
        self.life = 3.0
        self.size = size
        self.damage = damage

    def update(self, dt):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.position[2] += self.direction[2] * self.speed

        self.life -= dt

    def draw(self):
        x, y, z = self.position

        glPushMatrix()

        glTranslatef(x, y, z)
        glScalef(0.08, 0.08, 0.2)

        glColor3f(1, 0.8, 0.2)

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