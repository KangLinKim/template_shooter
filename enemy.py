import math
import time
import random
from OpenGL.GL import *

from model import Model
from bullet import Bullet
from particle import DeathParticle

        
class EnemyBulletManager:
    def __init__(self):
        self.bullets = []

    def shoot(self, pos, direction):
        self.bullets.append(
            Bullet(
                position=pos,
                direction=direction,
                size=0.08,
                damage=10,
                color=(1,0,0)
            )
        )

    def update(self, player, dt):
        remove = []

        for b in self.bullets:
            b.update(dt)

            dx = b.position[0] - player.position[0]
            dy = b.position[1] - player.position[1]
            dz = b.position[2] - player.position[2]

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)

            if dist < 0.6:
                player.take_damage(b.damage)
                remove.append(b)
                continue

            if b.life <= 0:
                remove.append(b)

        for b in remove:
            self.bullets.remove(b)

    def draw(self):
        for b in self.bullets:
            b.draw()


class Enemy:
    def __init__(self, position, fire_interval, hp=50):
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

        self.hp = hp
        self.max_hp = hp
        self.radius = 0.6

        self.dead = False
        self.death_timer = 0
        self.death_rot = 0

        self.particles = []

        self.drop_item = False

    def take_damage(self, damage):
        if self.dead:
            return False

        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.dead = True

            for _ in range(20):
                self.particles.append(
                    DeathParticle(self.position)
                )

            return True

        return False

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

    def update(self, player, bullet_manager, dt):
        if self.dead:
            self.death_timer += dt

            if self.death_rot < 90:
                self.death_rot += dt * 160

            self.position[1] -= dt * 0.5

            remove = []

            for p in self.particles:
                p.update(dt)
                if p.life <= 0:
                    remove.append(p)

            for p in remove:
                self.particles.remove(p)

            return
        
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

    def draw(self, player):
        glPushMatrix()

        glTranslatef(
            self.position[0],
            self.position[1],
            self.position[2]
        )

        glRotatef(self.yaw,0,1,0)

        if self.dead:
            glRotatef(self.death_rot,0,0,1)

        glColor3f(1,0,0)
        glScalef(1.2,1.2,1.2)

        self.model.draw()

        glPopMatrix()

        for p in self.particles:
            p.draw(player)

        if not self.dead:
            self.draw_hp_bar(player)

    def draw_hp_bar(self, player):
        x,y,z = self.position

        hp_ratio = self.hp / self.max_hp

        width = 1.2
        height = 0.12

        glPushMatrix()

        glTranslatef(x, y + 1.6, z)
        glRotatef(-player.rotation[1], 0,1,0)

        glDisable(GL_DEPTH_TEST)

        glColor3f(0.2,0.2,0.2)

        glBegin(GL_QUADS)

        glVertex3f(-width/2, 0, 0)
        glVertex3f(width/2, 0, 0)
        glVertex3f(width/2, height, 0)
        glVertex3f(-width/2, height, 0)

        glEnd()

        glColor3f(0,1,0)

        glBegin(GL_QUADS)

        glVertex3f(-width/2, 0, 0.01)
        glVertex3f(-width/2 + width*hp_ratio, 0, 0.01)
        glVertex3f(-width/2 + width*hp_ratio, height, 0.01)
        glVertex3f(-width/2, height, 0.01)

        glEnd()

        glEnable(GL_DEPTH_TEST)

        glPopMatrix()