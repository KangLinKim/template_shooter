from bullet import Bullet


import time
import os
from bullet import Bullet
from constants import WEAPON_DATA

class BulletManager:
    def __init__(self, weapon_path):
        self.bullets = []
        self.set_weapon(weapon_path)
        self.last_shot_time = 0

    def set_weapon(self, weapon_path):
        weapon_type = os.path.basename(weapon_path)
        weapon_type = weapon_type.split("_")[0]

        data = WEAPON_DATA[weapon_type]
        self.weapon_path = weapon_path
        self.ammo = data["ammo"]
        self.max_ammo = data["ammo"]
        self.bullet_size = data.get("bullet_size", [0.01, 0.01, 0.02])
        self.bullet_damage = data.get("bullet_damage", 0)
        self.fire_rate = data.get("fire_rate", 5.0)

    def shoot(self, position, direction):
        now = time.time()
        if now - self.last_shot_time < self.fire_rate:
            return
        
        if self.ammo <= 0:
            print("Out of ammo")
            return

        bullet = Bullet(position, direction, self.bullet_size, self.bullet_damage)
        self.bullets.append(bullet)
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

    def draw(self):
        for b in self.bullets:
            b.draw()