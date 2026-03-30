import random
from OpenGL.GL import *


class Particle:
    def __init__(self, position, direction, split_range=0.3):
        self.position = list(position)

        self.direction = [
            direction[0] + random.uniform(-split_range, split_range),
            direction[1] + random.uniform(-split_range, split_range),
            direction[2] + random.uniform(-split_range, split_range)
        ]

        self.speed = random.uniform(0.2, 0.6)
        self.life = random.uniform(0.1, 0.25)
        self.size = random.uniform(0.02, 0.05)

    def update(self, dt):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.position[2] += self.direction[2] * self.speed

        self.life -= dt

    def draw(self, player):
        x, y, z = self.position

        pitch, yaw = player.rotation

        glPushMatrix()

        glTranslatef(x, y, z)

        glRotatef(-yaw, 0, 1, 0)
        glRotatef(-pitch, 1, 0, 0)

        glScalef(self.size, self.size, self.size)

        glColor3f(1, 0.7, 0.1)

        glBegin(GL_QUADS)

        glVertex3f(-1, -1, 0)
        glVertex3f( 1, -1, 0)
        glVertex3f( 1,  1, 0)
        glVertex3f(-1,  1, 0)

        glEnd()

        glPopMatrix()


class DeathParticle:
    def __init__(self, position):
        self.pos = list(position)

        self.vel = [
            random.uniform(-2,2),
            random.uniform(1,4),
            random.uniform(-2,2)
        ]

        self.life = random.uniform(0.5,1.2)

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.pos[2] += self.vel[2] * dt

        self.vel[1] -= 6 * dt

        self.life -= dt

    def draw(self, player):
        if self.life <= 0:
            return

        glPushMatrix()

        glTranslatef(self.pos[0], self.pos[1], self.pos[2])

        glRotatef(-player.rotation[1], 0,1,0)
        glRotatef(player.rotation[0], 1,0,0)

        s = 0.05

        glColor3f(1, random.uniform(0.2,0.8), 0)

        glBegin(GL_QUADS)

        glVertex3f(-s,-s,0)
        glVertex3f(s,-s,0)
        glVertex3f(s,s,0)
        glVertex3f(-s,s,0)

        glEnd()

        glPopMatrix()