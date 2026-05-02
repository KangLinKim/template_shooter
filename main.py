import pygame
import random
import time

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from player import Player
from constants import *

from item_manager import ItemManager
from bullet_manager import BulletManager
from ui import UI


WIDTH = 1280
HEIGHT = 720

SPAWN_INTERVAL = 5
MAP_RANGE = 15

default_weapon = "assets/player/Pistol_K.fbx"

"""
문제
1. UIs라는 이름의 list를 생성하고, assets/UI폴더에 저장된 이미지들의 경로를 넣어주세요.
1.1. 생성과 동시에 넣어주세요.
1.2. 추가하는 함수를 사용해 하나씩 넣어주세요.
1.3. for문을 사용해서 UIs에 있는 모든 이미지 경로를 출력해주세요.

2. UIs라는 이름의 Dictionary를 생성하고, 아래의 key와 이미지를 하나의 쌍으로 작성해주세요.
    - "Heart"
    - "Ammo"
    - "Cross"
2.1. 생성과 동시에 넣어주세요.
2.2. 추가하는 함수를 사용해 하나씩 넣어주세요.
2.3. for문을 사용해서 UIs에 있는 모든 key와 value를 출력해주세요.

3. 이제 UI를 그려야합니다. 아래의 지시를 따라 ui클래스를 작성해주세요.(122 ~ 124번 줄)
    - ui파일의 UI클래스를 가져와주세요.
    - ui라는 변수로 UI클래스의 인스턴스를 생성해주세요.
    - UI클래스의 생성자에는 화면의 너비, 높이, 그리고 UIs에 저장된 이미지 경로들을 넣어주세요.

    - ui클래스의 생성사는 ui.py에 서술되어 있습니다.

4. UI클래스의 draw함수를 사용해서 화면에 UI를 그려주세요.(206 ~ 208번 줄)
    - draw함수의 매개변수로 플레이어의 체력, 총알 수, 그리고 점수를 넣어주세요.
    - player의 체력은 player클래스의 health변수로 작성되어 있습니다.
    - 총알 수는 bullet_manager의 ammo변수로 작성되어 있습니다.
    - 점수는 100점으로 작성해주세요.
    
"""


def init_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, WIDTH / HEIGHT, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])


def draw_ground():
    glDisable(GL_LIGHTING)
    glColor3f(0.3, 0.3, 0.3)

    size = 20

    glBegin(GL_LINES)

    for i in range(-size, size):
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)

        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)

    glEnd()

    glEnable(GL_LIGHTING)


def main():
    pygame.init()

    pygame.display.set_mode(
        (WIDTH, HEIGHT),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption(CAPTION)

    init_opengl()

    player = Player(default_weapon)
    item_manager = ItemManager()
    bullet_manager = BulletManager(default_weapon)
    """
    3번 문제
    """

    clock = pygame.time.Clock()

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    last_spawn = time.time()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        now = time.time()

        if now - last_spawn > SPAWN_INTERVAL:
            weapon = random.choice(WEAPON_POOL)

            x = random.uniform(-MAP_RANGE, MAP_RANGE)
            z = random.uniform(-MAP_RANGE, MAP_RANGE)

            item_manager.spawn_item(
                weapon,
                [x, 0.6, z]
            )

            last_spawn = now

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEMOTION:
                mx, my = event.rel

                player.rotate_yaw(mx * 0.2)
                player.rotate_pitch(my * 0.2)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos, direction = player.get_muzzle()

                    bullet_manager.shoot(pos, direction)

        keys = pygame.key.get_pressed()

        speed = 0.1

        forward = 0
        right = 0

        if keys[K_w]:
            forward += 1

        if keys[K_s]:
            forward -= 1

        if keys[K_a]:
            right -= 1

        if keys[K_d]:
            right += 1

        player.move(forward, right, speed)

        if keys[K_ESCAPE]:
            running = False

        item_manager.update(player, bullet_manager)
        bullet_manager.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        player.apply_camera()

        draw_ground()

        item_manager.draw()
        bullet_manager.draw()
        player.draw_weapon()
        
        """
        4번 문제
        """

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()