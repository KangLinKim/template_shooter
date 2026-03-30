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

default_weapon = "assets/player/Pistol_K.obj"


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
    ui = UI(WIDTH, HEIGHT,
                    "assets/UI/Heart.png",
                    "assets/UI/Ammo.png",
                    "assets/UI/Cross.png",)

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

        ui.draw(
            player.health,
            bullet_manager.ammo,
            100 - bullet_manager.ammo
        )


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()