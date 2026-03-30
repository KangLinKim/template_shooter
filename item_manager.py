import math
import time
import random
from OpenGL.GL import *

from model import Model


class Item:
    def __init__(self, model_path, position):
        self.model = Model(model_path)
        self.weapon_path = model_path

        self.position = list(position)
        self.base_y = position[1]
        self.rotation = 0

        self.start_time = time.time()

        self.pickup_distance = 1.5

    def update(self):
        t = time.time() - self.start_time
        self.position[1] = self.base_y + math.sin(t * 2) * 0.25
        self.rotation += 1.2

    def draw(self):
        glPushMatrix()

        x, y, z = self.position

        glTranslatef(x, y, z)
        glRotatef(self.rotation, 0, 1, 0)
        glScalef(0.4, 0.4, 0.4)

        self.model.draw()

        glPopMatrix()

    def check_pickup(self, player):
        px, py, pz = player.position

        dx = self.position[0] - px
        dz = self.position[2] - pz

        dist = math.sqrt(dx * dx + dz * dz)

        if dist < self.pickup_distance:
            player.change_weapon(self.weapon_path)

            return True

        return False


class ItemManager:
    def __init__(self, item_pool=[]):
        self.items = []
        self.item_pool = item_pool

    def random_spawn(self, position):
        if not self.item_pool:
            return

        model_path = random.choice(self.item_pool)
        self.spawn_item(model_path, position)

    def spawn_item(self, model_path, position):
        item = Item(model_path, position)
        self.items.append(item)

    def update(self, player, bullet_manager = None):
        remove_list = []

        for item in self.items:
            item.update()

            if item.check_pickup(player):
                remove_list.append(item)

                if bullet_manager is not None:
                    bullet_manager.set_weapon(item.weapon_path)

        for item in remove_list:
            if item in self.items:
                self.items.remove(item)

    def draw(self):
        for item in self.items:
            item.draw()