import random, time, math

from enemy import EnemyBulletManager, Enemy

class EnemyManager:
    def __init__(self, spawn_interval, min_radius, max_radius):

        self.enemies = []

        self.bullet_manager = EnemyBulletManager()

        self.spawn_interval = spawn_interval
        self.min_radius = min_radius
        self.max_radius = max_radius

        self.last_spawn = time.time()

    def spawn(self, player):

        angle = random.uniform(0, math.pi*2)
        radius = random.uniform(self.min_radius, self.max_radius)

        px, py, pz = player.position

        x = px + math.cos(angle)*radius
        z = pz + math.sin(angle)*radius

        pos = [x, 0.6, z]

        interval = random.uniform(1.0, 2.5)

        self.enemies.append(
            Enemy(pos, interval)
        )

    def update(self, player, dt):

        now = time.time()

        # spawn enemy
        if now - self.last_spawn > self.spawn_interval:
            self.spawn(player)
            self.last_spawn = now

        for e in self.enemies:
            e.update(player, self.bullet_manager)

        self.bullet_manager.update(dt)

    def draw(self):
        for e in self.enemies:
            e.draw()

        self.bullet_manager.draw()