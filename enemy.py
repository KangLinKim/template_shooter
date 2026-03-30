import math
import time
import random
from OpenGL.GL import *

from model import Model
from bullet import Bullet

        
class EnemyBulletManager:
    def __init__(self):
        self.bullets = []

    def shoot(self, pos, direction):
        self.bullets.append(
            Bullet(
                position=pos,
                direction=direction,
                size=0.08,
                damage=5,
                color=(1,0,0)
            )
        )

    def update(self, dt):
        for b in self.bullets:
            b.update(dt)

    def draw(self):
        for b in self.bullets:
            b.draw()


class Enemy:
    def __init__(self, position, fire_interval):
        self.position = position
        self.model = Model("assets/player/enemy_cube.obj")

        self.detect_radius = 12

        self.last_fire = 0
        self.fire_interval = fire_interval

        self.yaw = 0
        self.state = "patrol"

        self.patrol_dir = [
            random.uniform(-1,1),
            0,
            random.uniform(-1,1)
        ]

    def distance(self, player):
        dx = player.position[0] - self.position[0]
        dz = player.position[2] - self.position[2]

        return math.sqrt(dx*dx + dz*dz)

    def get_direction(self, player):
        dx = player.position[0] - self.position[0]
        dy = player.position[1] - self.position[1]
        dz = player.position[2] - self.position[2]

        l = math.sqrt(dx*dx + dy*dy + dz*dz)

        return [dx/l, dy/l, dz/l]
    
    def get_yaw_to_player(self, player):

        dx = player.position[0] - self.position[0]
        dz = player.position[2] - self.position[2]

        return math.degrees(math.atan2(dx, -dz))

    def new_patrol_target(self):

        angle = random.uniform(0, math.pi*2)
        radius = random.uniform(2,6)

        x = self.position[0] + math.cos(angle)*radius
        z = self.position[2] + math.sin(angle)*radius

        self.patrol_target = [x, z]

    def patrol(self):

        if self.patrol_target is None:
            self.new_patrol_target()

        tx, tz = self.patrol_target

        dx = tx - self.position[0]
        dz = tz - self.position[2]

        dist = math.sqrt(dx*dx + dz*dz)

        if dist < 0.3:
            self.new_patrol_target()
            return

        dx /= dist
        dz /= dist

        self.position[0] += dx * self.patrol_speed
        self.position[2] += dz * self.patrol_speed

    def update(self, player, bullet_manager):
        dist = self.distance(player)

        if dist < self.detect_radius:
            self.state = "attack"
        else:
            self.state = "patrol"

        if self.state == "attack":

            self.yaw = self.get_yaw_to_player(player)

            now = time.time()

            if now - self.last_fire > self.fire_interval:

                direction = self.get_direction(player)

                muzzle = [
                    self.position[0],
                    self.position[1],
                    self.position[2]
                ]

                bullet_manager.shoot(muzzle, direction)

                self.last_fire = now

        else:
            speed = 0.02

            self.position[0] += self.patrol_dir[0] * speed
            self.position[2] += self.patrol_dir[2] * speed

            self.yaw = math.degrees(
                math.atan2(self.patrol_dir[0], -self.patrol_dir[2])
            )

    def draw(self):
        glPushMatrix()

        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2]
        )

        glRotatef(self.yaw, 0,1,0)

        glColor3f(1,0,0)

        glScalef(1.2,1.2,1.2)

        self.model.draw()

        glPopMatrix()