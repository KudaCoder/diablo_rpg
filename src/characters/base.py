import pygame as pg
import os

from conf.settings import SCALE_SIZE, PURPLE

vec = pg.math.Vector2


class Character(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.weapon = None

        # Type of details...
        self.role = None
        self.health = 100

        # For animations
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.facing = None

    def load_images(self, character):
        game_folder = os.path.dirname(os.path.dirname(__file__))
        assets_folder = os.path.join(game_folder, "assets")

        self.idle_frames = []
        for image in os.listdir(os.path.join(assets_folder, character, "idle")):
            img = pg.image.load(os.path.join(assets_folder, character, "idle", image))
            img = pg.transform.scale(img, (SCALE_SIZE, SCALE_SIZE))
            img.set_colorkey(PURPLE)
            self.idle_frames.append(img)

        self.walk_frames_l = []
        self.walk_frames_r = []
        for image in os.listdir(os.path.join(assets_folder, character, "walk")):
            img = pg.image.load(os.path.join(assets_folder, character, "walk", image))
            img = pg.transform.scale(img, (SCALE_SIZE, SCALE_SIZE))
            img.set_colorkey(PURPLE)
            self.walk_frames_r.append(img)
            img = pg.transform.flip(img, True, False)
            self.walk_frames_l.append(img)

    def animate(self):
        now = pg.time.get_ticks()

        self.walking = False
        if self.vel.x != 0 or self.vel.y != 0:
            self.walking = True

        # Idle animations (None for now)
        if not self.jumping and not self.walking:
            self.facing = None
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]

        # Walking animations
        if self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                    self.facing = "right"
                if self.vel.x < 0:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.facing = "left"

                if self.vel.y != 0 and self.vel.x == 0:
                    if self.facing == "right":
                        self.image = self.walk_frames_r[self.current_frame]
                    elif self.facing == "left":
                        self.image = self.walk_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    @staticmethod
    def collide_with_rect(sprite_1, sprite_2):
        return sprite_1.collision_rect.colliderect(sprite_2.rect)

    @staticmethod
    def collide_with_walls(sprite, group, direction):
        if direction == "x":
            collisions = pg.sprite.spritecollide(
                sprite, group, False, sprite.collide_with_rect
            )
            if collisions:
                collision = collisions[0]
                if sprite.vel.x > 0:
                    sprite.pos.x = collision.rect.left - sprite.collision_rect.width / 2
                if sprite.vel.x < 0:
                    sprite.pos.x = (
                        collision.rect.right + sprite.collision_rect.width / 2
                    )
                sprite.vel.x = 0
                sprite.collision_rect.centerx = sprite.pos.x
        if direction == "y":
            collisions = pg.sprite.spritecollide(
                sprite, group, False, sprite.collide_with_rect
            )
            if collisions:
                collision = collisions[0]
                if sprite.vel.y > 0:
                    sprite.pos.y = collision.rect.top - sprite.collision_rect.height / 2
                if sprite.vel.y < 0:
                    sprite.pos.y = (
                        collision.rect.bottom + sprite.collision_rect.height / 2
                    )
                sprite.vel.y = 0
                sprite.collision_rect.centery = sprite.pos.y

    def kill_all(self):
        self.kill()
        if self.weapon is not None:
            self.weapon.kill()
