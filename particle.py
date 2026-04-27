import random
from OpenGL.GL import *


class Particle:
    def __init__(self, position, direction, split_range=0.3):
        self.position = list(position)

        """
        2.1. self.direction변수를 아래와 같이 작성해주세요.
            direction은 길이가 3인 list입니다.
            direction의 각 요소에 -split_range와 split_range 사이의 랜덤한 값을 더해, self.direction에 할당해주세요.
        2.2. self.speed, self.life, self.size변수를 아래와 같이 작성해주세요.
            self.speed는 0.2와 0.6 사이의 랜덤한 값입니다.
            self.life는 0.1과 0.25 사이의 랜덤한 값입니다.
            self.size는 0.02와 0.05 사이의 랜덤한 값입니다.
        
        2.3. self.position, self.direction, self.camera_direction의 길이가 같은지 확인해야합니다.
            아래의 지시를 따라 코드를 작성해주세요.
            2.3.1 if문을 사용하여, 다르다면 오류를 발생시켜주세요.
            2.3.2. assert문을 사용하여, 다르다면 오류를 발생시켜주세요.
        """

        self.speed = random.uniform(0.2, 0.6)
        self.life = random.uniform(0.1, 0.25)
        self.size = random.uniform(0.02, 0.05)

        self.camera_direction = [-1, -1, -1]

    def update(self, dt):
        self.life -= dt

        """
        2.4. self.position의 각 요소에 self.direction의 각 요소 * self.speed를 곱한 값을 할당해주세요.
            2.4.1. 이러한 코드는 map함수를 사용해야합니다.
            2.4.2. map 함수와 lambda 함수를 사용해야합니다.
        
        2.5. 카메라가 오브젝트를 바라보는 방향을 알아야합니다.
            아래의 지시를 따라 방향을 계산해주세요.
            카메라의 방향은 0, 0, 0입니다.
            self.camera_direction의 각 요소에 self.position의 각 요소에서 카메라의 방향의 각 요소를 뺀 값을 할당해주세요.
        """

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