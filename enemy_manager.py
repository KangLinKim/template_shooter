import random, time, math

from enemy import EnemyBulletManager, Enemy

class EnemyManager:
    def __init__(self, spawn_interval, min_radius, max_radius):
        self.enemies = []

        self.bullet_manager = EnemyBulletManager()
        
        if len(spawn_interval) > 2:
            raise "1.1번 문제를 틀렸습니다"

        self.spawn_interval = random.randrange(spawn_interval[0], spawn_interval[1])
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
        """
        2.1. pos라는 변수를 [x]로 할당해주세요.
        2.2. pos라는 list에 24번 줄에서 생성한 변수 z를 넣어주세요.
        2.3. pos라는 list의 1번 인덱스에 0.6을 넣어주세요.
            그러면 pos라는 list는 길이 3의 list가 되어야합니다.
        """
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