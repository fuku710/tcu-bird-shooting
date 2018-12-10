import pyxel
import math

def distance(point_a, point_b):
    return math.sqrt((point_b.x - point_a.x)**2 + (point_b.y - point_a.y)**2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
