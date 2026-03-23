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


WIDTH = 1280
HEIGHT = 720

SPAWN_INTERVAL = 5
MAP_RANGE = 15

default_weapon = "assets/player/Pistol_K.fbx"


"""
문제

1. constants.py에는 WEAPON_POOL이라는 list가 선언되어 있습니다.
    assets/player 폴더에 있는 파일들을 list를 수정하지 않고 WEAPON_POOL에 추가해주세요.

2. WEAPON_POOL에 있는 무기 중 랜덤으로 하나를 선택해, default_weapon으로 설정해주세요.

3. WEAPON_DATA에는 각 무기의 정보가 담긴 dictionary가 선언되어 있습니다.
    이제 데미지와 쿨타임 정보를 입력해야하는데,
    각 무기마다 bullet_damage와 fire_rate정보를 원하는대로 추가해주세요.

4. 캐릭터를 움직이는 함수를 작성해야합니다.
    다음의 함수를 완성해주세요.
    keys에 맞춰 앞방향, 또는 옆방향을 -1, 또는 1로 설정해주세요.
    앞방향과 옆방향을 동시에 반환해주세요.

def Character_move(keys):
    앞방향 = 0
    옆방향 = 0

    if keys[K_w]:
        pass
    
    if keys[K_s]:
        pass
    
    if keys[K_a]:
        pass
        
    if keys[K_d]:
        pass
    
    return

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

    player = Player(default_weapon)
    item_manager = ItemManager()
    bullet_manager = BulletManager(default_weapon)

    clock = pygame.time.Clock()

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    last_spawn = time.time()

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

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos, direction = player.get_muzzle()

                    bullet_manager.shoot(pos, direction)

        keys = pygame.key.get_pressed()

        speed = 0.1

        forward, right = Character_move(keys)

        player.move(forward, right, speed)

        if keys[K_ESCAPE]:
            running = False

        item_manager.update(player, bullet_manager)
        bullet_manager.update(dt)

        item_manager.update(player, bullet_manager)
        bullet_manager.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        player.apply_camera()


        draw_ground()

        item_manager.draw()
        bullet_manager.draw()

        item_manager.draw()
        bullet_manager.draw()
        player.draw_weapon()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()