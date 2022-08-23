import pygame as pg

from conf.settings import TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = self.game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    # to get rid of linting annoyance
    def fuck_off(self):
        ...


class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.floor
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.floor_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
