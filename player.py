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

        self.hit_timer = 0
        self.hit_duration = 0.25
        """
        dead라는 이름의 self변수를 만들고, 초기값을 False로 할당해주세요.
        health라는 이름의 self변수를 만들고, 초기값을 100으로 할당해주세요.
        """

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
    
    def take_damage(self, damage):
        """
        2.2. self.dead 변수가 True라면 함수를 바로 종료해주세요.
        """

        self.health -= damage
        self.hit_timer = 0.25

        # print("player hit:", self.health)
            
        """
        2.3. self.health가 0보다 작을 경우, 아래의 코드를 작성해주세요.
            - self.health를 0으로 초기화해주세요.
            - self.dead를 True로 수정해주세요.
            - 플레이어가 사망했다는 문구를 출력해주세요.
        """

    def update(self, dt):
        if self.hit_timer > 0:
            self.hit_timer -= dt

    def draw_hit_effect(self, width, height):
        """
        2.4. 클래스의 hit_timer 변수가 0 이하라면, 함수를 종료해주세요.
        """

        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        """
        2.5. glColor4f라는 함수를 사용해, 화면을 붉게 만드려 합니다.
            아래의 요구사항을 따라 코드를 작성해주세요.
            
            glColor4f는 R, G, B, A라는 4개의 매개변수를 순서대로 받습니다.
            R, G, B에 원하는 색상을 0~1사이로 하나씩 넣어주세요.
            
            해당 클래스에는 피격 시간을 측정하는 변수와, 피격 효과를 유지하는 변수 2가지가 있습니다.
            (시간 측정 변수 / 유지 변수) * 0.35를 A에 넣어주세요.
            - 힌트: "hit"이라는 이름으로 시작하는 변수임        
        """

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