import random, time, math

from enemy import EnemyBulletManager, Enemy

class EnemyManager:
    def __init__(self, spawn_interval, min_radius, max_radius, game_manager):
        self.enemies = []

        self.bullet_manager = EnemyBulletManager()

        self.spawn_interval = spawn_interval
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.game_manager = game_manager

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
            Enemy(pos, interval, hp=50)
        )

    def check_bullet_collision(self, bullet_manager):
        remove_bullets = []

        for bullet in bullet_manager.bullets:
            bx,by,bz = bullet.position

            for enemy in self.enemies:
                if enemy.dead:
                    continue

                ex,ey,ez = enemy.position

                dx = bx - ex
                dy = by - ey
                dz = bz - ez

                dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                if dist < bullet.radius + enemy.radius:
                    dead = enemy.take_damage(bullet.damage)

                    remove_bullets.append(bullet)

                    if dead:
                        enemy.dead = True
                        self.game_manager.earn_score(1)

                    break

        for b in remove_bullets:
            if b in bullet_manager.bullets:
                bullet_manager.bullets.remove(b)

    def update(self, player, bullet_manager, item_manager, dt):
        now = time.time()

        if now - self.last_spawn > self.spawn_interval:
            self.spawn(player)
            self.last_spawn = now

        remove_enemies = []

        for e in self.enemies:
            e.update(player, self.bullet_manager, dt)

            if e.dead:
                e.death_timer += dt

                if e.death_timer > 1.5:
                    print("Enemy killed")
                    if not e.drop_item:
                        print("Spawning item")
                        item_manager.random_spawn([e.position[0], 0.6, e.position[2]])
                        e.drop_item = True

                    remove_enemies.append(e)

        for e in remove_enemies:
            self.enemies.remove(e)

        self.bullet_manager.update(player, dt)
        self.check_bullet_collision(bullet_manager)

    def draw(self, player):
        for e in self.enemies:
            e.draw(player)

        self.bullet_manager.draw()