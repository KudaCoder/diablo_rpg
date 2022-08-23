import pygame as pg
import pytmx

from conf.settings import SCALE_SIZE, WIDTH, HEIGHT


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = (tm.width * tm.tilewidth) * 2
        self.height = (tm.height * tm.tileheight) * 2
        self.tmx_data = tm

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pg.transform.scale(tile, (SCALE_SIZE, SCALE_SIZE))
                        surface.blit(
                            tile,
                            (x * SCALE_SIZE, y * SCALE_SIZE),
                        )

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, WIDTH, HEIGHT)
