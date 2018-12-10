import pyxel
from random import randrange
from common import Point, distance
from bullet import Bullet


# 敵
# HP
ENEMY_HP = 100
# 速度
ENEMY_SPEED = 2
# 発生間隔
ENEMY_INTERVAL = 20
# 弾速度
ENEMY_BULLET_SPEED = 4
# 弾発射間隔
ENEMY_BULLET_INTERVAL = 40


class EnemyManager:
    def __init__(self, x, y, w, h, hp=ENEMY_HP, speed=ENEMY_SPEED, spawn_interval=ENEMY_INTERVAL, bullet_damage=1, bullet_speed=ENEMY_BULLET_SPEED, shoot_interval=ENEMY_BULLET_INTERVAL):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.speed = speed
        self.spawn_interval = spawn_interval
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.shoot_interval = shoot_interval

        self.enemies = []
        self.bullets = []

        self.score = 0

    def update(self):
        # 敵発生
        if pyxel.frame_count % self.spawn_interval == 0:
            x = randrange(self.x, self.x + self.w)
            y = randrange(self.y, self.y + self.h)
            self.enemies.append(
                Enemy(x, y, self.hp, self.speed, self.shoot_interval))

        # 敵削除
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]
        # 敵弾削除
        self.bullets = [bullet for bullet in self.bullets if bullet.is_alive]

        # 敵弾発射＆更新
        for enemy in self.enemies:
            if enemy.frame_count % enemy.shoot_interval == 0:
                self.bullets.append(EnemyBullet(
                    enemy.pos.x, enemy.pos.y))
            enemy.update()

        # 敵弾更新
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()

    def reset(self):
        self.enemies = []
        self.bullets = []

        self.score = 0

    def check_hit_by_bullet(self, bullets):
        for enemy in self.enemies:
            for bullet in bullets:
                if distance(enemy.pos, bullet.pos) < 4:
                    enemy.hp -= bullet.damage
                    bullet.is_alive = False
                    self.score += 10 if enemy.hp <= 0 else 0


class Enemy:
    def __init__(self, x, y, hp, speed, shoot_interval):
        self.pos = Point(x, y)
        self.hp = hp
        self.speed = speed
        self.shoot_interval = shoot_interval
        self.frame_count = 0
        self.is_alive = True

    def update(self):
        self.pos.x -= self.speed
        self.frame_count += 1
        if self.hp <= 0 or self.pos.x < 0:
            self.is_alive = False
        else:
            self.is_alive = True

    def draw(self):
        pyxel.blt(self.pos.x, self.pos.y, 0, 16, 0, 16, 16, 0)


class EnemyBullet(Bullet):
    def __init__(self, x, y, damage=1, speed=ENEMY_BULLET_SPEED, deg=-90):
        super().__init__(x, y, damage, speed, deg)

    def draw(self):
        pyxel.blt(self.pos.x, self.pos.y, 0, 16, 16, 16, 16, 0)
