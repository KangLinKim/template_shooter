import time
import os
from bullet import Bullet
from particle import Particle
from constants import WEAPON_DATA


class BulletManager:
    def __init__(self, weapon_path):
        self.bullets = []
        self.particles = []
        self.set_weapon(weapon_path)
        self.last_shot_time = 0

    def set_weapon(self, weapon_path):
        weapon_type = os.path.basename(weapon_path)
        self.weapon_type = weapon_type.split("_")[0]

        data = WEAPON_DATA[self.weapon_type]
        self.weapon_path = weapon_path
        self.ammo = data["ammo"]
        self.max_ammo = data["ammo"]
        self.bullet_size = data["bullet_size"]
        self.bullet_damage = data["bullet_damage"]
        self.fire_rate = data["fire_rate"]

    def shoot(self, position, direction):
        now = time.time()
        if now - self.last_shot_time < self.fire_rate:
            return
        
        if self.ammo <= 0:
            print("Out of ammo")
            return

        bullet = Bullet(position, direction, self.bullet_size, self.bullet_damage, (1, 0.8, 0.2))
        self.bullets.append(bullet)

        if self.weapon_type == "Pistol":
            particle_range = 0.2
        elif self.weapon_type == "SMG":
            particle_range = 0.1
        else:
            particle_range = 0.3

        for _ in range(12):
            self.particles.append(
                Particle(position, direction, split_range=particle_range)
            )

        self.ammo -= 1
        self.last_shot_time = now

    def update(self, dt):
        remove = []
        for b in self.bullets:
            b.update(dt)
            if b.life <= 0:
                remove.append(b)
        for b in remove:
            self.bullets.remove(b)

        remove = []
        for p in self.particles:
            p.update(dt)
            if p.life <= 0:
                remove.append(p)

        for p in remove:
            self.particles.remove(p)

    def draw(self, player):
        for b in self.bullets:
            b.draw()

        for p in self.particles:
            p.draw(player)