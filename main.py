import pygame
import random
import time

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from game_manger import GameManager
from enemy_manager import EnemyManager
from player import Player
from constants import *

from item_manager import ItemManager
from bullet_manager import BulletManager
from ui import UI


WIDTH = 1280
HEIGHT = 720

SPAWN_INTERVAL = 5
MAP_RANGE = 15

default_weapon = "assets/player/Pistol_K.obj"

"""
문제

1. GamaManager를 통해 점수를 관리하려 합니다.
    아래의 요건에 맞춰 game_manger.py에서 클래스를 완성해주세요.
    - 초기 score는 0점
    - earn_score 함수를 통해 점수를 획득할 수 있습니다.
        해당 함수는 획득한 점수만큼 score에 더해주는 역할을 합니다.

2. Particle 시스템을 구현하려 합니다.
    아래의 요건에 맞춰 particle.py에서 클래스를 완성해주세요.

3. 이제 프로젝트를 마무리 할 차례입니다.
    summary함수를 아래와 같은 요소를 반환하도록 작성해주세요.
    - 총 플레이 시간
    - 최종 점수
    - 플레이어 생존 여부

    score가 100점 이상이라면 "You Win!", 아니라면 "Game Over!"를 출력해주세요.
    summary함수를 코드 종료 시 호출해주세요.
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
    item_manager = ItemManager(item_pool=WEAPON_POOL)
    bullet_manager = BulletManager(default_weapon)
    ui = UI(WIDTH, HEIGHT,
                    "assets/UI/Heart.png",
                    "assets/UI/Ammo.png",
                    "assets/UI/Cross.png",)

    game_manager = GameManager()
    enemy_manager = EnemyManager(
        spawn_interval=6,
        min_radius=8,
        max_radius=18,
        game_manager=game_manager,
    )

    clock = pygame.time.Clock()

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    last_spawn = time.time()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        now = time.time()

        if now - last_spawn > SPAWN_INTERVAL:
            x = random.uniform(-MAP_RANGE, MAP_RANGE)
            z = random.uniform(-MAP_RANGE, MAP_RANGE)

            item_manager.random_spawn([x, 0.6, z])

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
        bullet_manager.draw(player)
        enemy_manager.update(player, bullet_manager, item_manager, dt)
        enemy_manager.draw(player)
        player.draw_weapon()

        player.update(dt)

        ui.draw(
            player,
            bullet_manager.ammo,
            game_manager.score,
        )

        player.draw_hit_effect(WIDTH, HEIGHT)

        pygame.display.flip()

        if player.dead:
            print("GAME OVER")
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()