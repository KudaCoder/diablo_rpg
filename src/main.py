import pygame as pg
import sys
import os

from conf.settings import (
    RED,
    FPS,
    WHITE,
    WIDTH,
    HEIGHT,
    TILESIZE,
    SCALE_SIZE,
)
from world import TiledMap, Camera, Obstacle
from characters import Player, Enemy


class Game:
    def __init__(self):
        pg.init()
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # For final release!
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.load_data()

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        assets_folder = os.path.join(game_folder, "assets")
        map_folder = os.path.join(game_folder, "maps")
        self.map = TiledMap(os.path.join(map_folder, "level_2.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemy_weapons = pg.sprite.Group()
        self.player_weapons = pg.sprite.Group()

        # I have no idea why SCALE is necessary but without it the position
        # of everything is 4x too small
        SCALE = SCALE_SIZE / TILESIZE
        for tile_object in self.map.tmx_data.objects:
            tile_object.x = tile_object.x * SCALE
            tile_object.y = tile_object.y * SCALE
            tile_object.width = tile_object.width * SCALE
            tile_object.height = tile_object.height * SCALE

            if tile_object.name == "obstacle":
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "enemy":
                Enemy(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # pg.draw.rect(
        #     self.screen,
        #     WHITE,
        #     self.camera.apply_rect(self.player.weapon.collision_rect),
        #     2,
        # )

        # ENEMY HEALTH BARS, DON'T LIKE THIS HERE!!!
        for enemy in self.enemies:
            pg.draw.rect(
                self.screen,
                WHITE,
                self.camera.apply_rect(enemy.main_health_rect),
                2,
            )
            surface = pg.display.get_surface()
            surface.fill(
                RED,
                self.camera.apply_rect(enemy.health_rect),
            )

        for player in self.players:
            pg.draw.rect(
                self.screen,
                WHITE,
                self.camera.apply_rect(player.main_health_rect),
                2,
            )
            surface = pg.display.get_surface()
            surface.fill(
                RED,
                self.camera.apply_rect(player.health_rect),
            )

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()
