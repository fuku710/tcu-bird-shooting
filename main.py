import pyxel
import math
import copy
from random import randrange
from enum import Enum

from player import PlayerManager
from enemy import EnemyManager
from common import Point


class Scene(Enum):
    TITLE = 0
    GAME = 1
    GAME_BOSS = 2
    GAMEOVER = 3


# ウインドウサイズ
WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120

# 背景速度
BACKGROUND_SPEED = 4


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption='TCU BIRD SHOOTING')
        pyxel.load('resource.pyxel')

        self.scene = Scene.TITLE
        self.score = 0
        self.time = 0

        self.background_dot = []
        self.player_manager = PlayerManager()
        self.enemy_manager = EnemyManager(pyxel.width, 0, 1, pyxel.height)

        for i in range(50):
            self.background_dot.append(
                Point(randrange(0, WINDOW_WIDTH), randrange(0, WINDOW_HEIGHT)))

        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_background()
        if self.scene == Scene.TITLE:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.player_manager.reset()
                self.enemy_manager.reset()
                self.score = 0
                self.time = 0
                self.scene = Scene.GAME_BOSS

        elif self.scene == Scene.GAME:
            self.player_manager.update()
            self.enemy_manager.update()
            self.player_manager.check_hit_by_bullet(self.enemy_manager.bullets)
            self.player_manager.check_hit_by_enemy(self.enemy_manager.enemies)
            self.enemy_manager.check_hit_by_bullet(self.player_manager.bullets)
            self.score = self.enemy_manager.score
            if self.player_manager.get_life() <= 0:
                self.scene = Scene.GAMEOVER

        elif self.scene == Scene.GAME_BOSS:
            self.player_manager.update()

        elif self.scene == Scene.GAMEOVER:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.scene = Scene.TITLE

    def update_background(self):
        for dot in self.background_dot:
            dot.x = dot.x - BACKGROUND_SPEED if dot.x > 0 else WINDOW_WIDTH

    def draw(self):
        pyxel.cls(0)
        for dot in self.background_dot:
            pyxel.pix(dot.x, dot.y, 7)
        if self.scene == Scene.TITLE:
            pyxel.text(WINDOW_WIDTH/24 * 7, WINDOW_HEIGHT /
                       4 * 1, 'TCU BIRD SHOOTING', 7)
            pyxel.text(WINDOW_WIDTH/24 * 8, WINDOW_HEIGHT /
                       4 * 3, 'CLICK TO START', 7)
        elif self.scene == Scene.GAME:
            self.player_manager.draw()
            self.enemy_manager.draw()
            pyxel.text(
                0, 0, f'LIFE:{self.player_manager.get_life()} SCORE:{self.score} time:{self.time}', 7)
        elif self.scene == Scene.GAME_BOSS:
            self.player_manager.draw()
        elif self.scene == Scene.GAMEOVER:
            pyxel.text(WINDOW_WIDTH/24 * 9, WINDOW_HEIGHT /
                       4 * 1, 'GAME OVER', 7)
            pyxel.text(WINDOW_WIDTH/24 * 9, WINDOW_HEIGHT /
                       4 * 3, f'SCORE:{self.score}', 7)


App()
