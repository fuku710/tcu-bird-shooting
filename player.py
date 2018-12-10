import pyxel
from common import Point, distance
from bullet import Bullet

# プレイヤー
# 残機
PLAYER_LIFE = 3
# 弾ダメージ
PLAYER_BULLET_DAMAGE = 10
# 弾速度
PLAYER_BULLET_SPEED = 4
# 弾発射間隔
PLAYER_BULLET_INTERVAL = 2
# 無敵時間
PLAYER_INVINCIBLE_TIME = 45


class PlayerManager:
    def __init__(self, life=PLAYER_LIFE):
        self.player = Player(life)
        self.bullets = []
        self.default_life = life

    def update(self):
        # 自機弾発射
        if pyxel.frame_count % PLAYER_BULLET_INTERVAL == 0:
            self.bullets.append(PlayerBullet(
                self.player.pos.x + 2, self.player.pos.y))

        # 自機弾削除
        self.bullets = [bullet for bullet in self.bullets if bullet.is_alive]

        # 自機更新
        self.player.update()
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()

    def reset(self):
        self.player.life = self.default_life
        self.player.invincible_time = 0
        self.bullets = []
        self.score = 0

    def get_life(self):
        return self.player.life

    def check_hit_by_bullet(self, bullets):
        for bullet in bullets:
            if distance(self.player.pos, bullet.pos) < 4 and not self.player.invincible_time > 0:
                self.player.life -= 1
                self.player.invincible_time = PLAYER_INVINCIBLE_TIME
                bullet.is_alive = False

    def check_hit_by_enemy(self, enemies):
        for enemy in enemies:
            if distance(self.player.pos, enemy.pos) < 4 and not self.player.invincible_time > 0:
                self.player.life -= 1
                self.player.invincible_time = PLAYER_INVINCIBLE_TIME


class Player:
    def __init__(self, life):
        self.pos = Point(pyxel.mouse_x - 8, pyxel.mouse_y - 8)
        self.life = life
        self.invincible_time = 0
        self.bullets = []

    def update(self):
        self.pos.x = pyxel.mouse_x - 8
        self.pos.y = pyxel.mouse_y - 8
        if self.invincible_time > 0:
            self.invincible_time -= 1
        else:
            self.invincible_time = 0

    def draw(self):
        if self.invincible_time <= 0:
            pyxel.blt(self.pos.x, self.pos.y, 0,
                      0, 0, 16, 16, 0)
        elif pyxel.frame_count % 2 == 0:
            pyxel.blt(self.pos.x, self.pos.y, 0,
                      0, 0, 16, 16, 0)


class PlayerBullet(Bullet):
    def __init__(self, x, y, damage=PLAYER_BULLET_DAMAGE, speed=PLAYER_BULLET_SPEED, deg=90):
        super().__init__(x, y, damage, speed, deg)

    def draw(self):
        pyxel.blt(self.pos.x, self.pos.y, 0, 0, 16, 16, 16, 0)
