import pygame as pg
import os

from .base import Weapon

vec = pg.math.Vector2


class Sword(Weapon):
    def __init__(self, game, character, group):
        super(Sword, self).__init__(game, character, group, "sword")

    def update(self):
        self.pos = self.character.pos

        self.follow()
        self.rotate()

        self.rect.centerx = self.pt_x
        self.rect.centery = self.pt_y
        self.collision_rect.centerx = self.pt_x
        self.collision_rect.centery = self.pt_y

        self.animate()

    def rotate(self):
        self.rot += 45
        self.image = pg.transform.rotate(self.original_image, int(self.rot))

    def follow(self):
        if self.character.role == "player":
            self.tracking_pos_x, self.tracking_pos_y = pg.mouse.get_pos()
        elif self.character.role == "enemy":
            self.tracking_pos_x, self.tracking_pos_y = self.game.player.pos

        # add camera offset
        self.tracking_pos_x = self.tracking_pos_x - self.game.camera.camera.left
        self.tracking_pos_y = self.tracking_pos_y - self.game.camera.camera.top
        self.rot = (vec(self.tracking_pos_x, self.tracking_pos_y) - self.pos).angle_to(
            vec(1, 0)
        )

        if not self.attacking:
            circle_vec = vec(self.tracking_pos_x, self.tracking_pos_y) - self.pos
            circle_vec.scale_to_length(-self.radius)
            self.pt_x, self.pt_y = self.pos.x + circle_vec.x, self.pos.y + circle_vec.y
