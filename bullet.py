import pyxel
import math
from common import Point

OFFSET = 10


class Bullet:
    def __init__(self, x, y, damage, speed, deg):
        self.pos = Point(x, y)
        self.damage = damage
        self.rad = math.pi * 2 / 360 * deg
        self.speed = speed
        self.is_alive = True

    def update(self):
        self.pos.x += self.speed * math.sin(self.rad)
        self.pos.y += self.speed * math.cos(self.rad)
        if self.pos.x <= 0 - OFFSET or self.pos.x >= pyxel.width + OFFSET or self.pos.y <= 0 - OFFSET or self.pos.y >= pyxel.height + OFFSET:
            self.is_alive = False
