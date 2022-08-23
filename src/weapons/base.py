import pygame as pg
import os

from conf.settings import SCALE_SIZE, WEAPON_COLLISION_RECT, BLACK, TILESIZE, WHITE

vec = pg.math.Vector2


class Weapon(pg.sprite.Sprite):
    def __init__(self, game, character, group, weapon_type):
        self.game = game
        self.groups = self.game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)

        self.weapon_type = weapon_type
        self.character = character
        self.pos = vec(self.character.pos.x, self.character.pos.y)
        self.pt_x = self.pt_y = 0
        self.load_images()
        self.original_image = self.idle_frames[0]
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.collision_rect = WEAPON_COLLISION_RECT.copy()
        self.collision_rect.center = self.rect.center

        # These values should be set from a JSON
        # Animation
        self.animation_speed = 0.14
        self.current_frame = 0
        self.last_update = 0

        # This is how far from the character the weapon circles
        self.radius = 50
        # Rotation of weapon - intended to keep pointing at target
        # i.e. mouse or player if enemy
        self.rot = 0

        self.attacking = False
        self.attack_speed = 350
        self.last_attack = 0
        self.damage = 25

    def load_images(self):
        game_folder = os.path.dirname(os.path.dirname(__file__))
        assets_folder = os.path.join(game_folder, "assets")

        self.idle_frames = []
        for image in os.listdir(
            os.path.join(assets_folder, "weapons", self.weapon_type, "idle")
        ):
            img = pg.image.load(
                os.path.join(assets_folder, "weapons", self.weapon_type, "idle", image)
            )
            self.idle_frames.append(img)

        self.attack_frames = []
        images = os.listdir(
            os.path.join(assets_folder, "weapons", self.weapon_type, "attack")
        )
        images = self.sort_images(images)
        for image in images:
            img = pg.image.load(
                os.path.join(
                    assets_folder, "weapons", self.weapon_type, "attack", image
                )
            )
            self.attack_frames.append(img)

    # Shouldn't need this but listdir is not returning images in order
    def sort_images(self, images):
        return sorted(images, key=lambda x: x.split("_")[-1])

    def animate(self):
        if self.attacking is True:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.attack_frames):
                self.image = self.idle_frames[0]
                self.current_frame = 0
                self.attacking = False
            else:
                self.image = self.attack_frames[int(self.current_frame)]
                self.image = pg.transform.rotate(self.image, self.rot)

    def attack(self, group_1, group_2):
        now = pg.time.get_ticks()
        if (now - self.last_attack) > self.attack_speed:
            self.attacking = True
            self.last_attack = now
            circle_vec = vec(self.tracking_pos_x, self.tracking_pos_y) - self.pos
            circle_vec.scale_to_length(self.radius)
            self.pt_x, self.pt_y = self.pos.x + circle_vec.x, self.pos.y + circle_vec.y
            self.collide_with_character(group_1, group_2)

    def collide_with_rect(self, sprite_1, sprite_2):
        return sprite_1.rect.colliderect(sprite_2.collision_rect)

    def collide_with_character(self, group_1, group_2):
        """
        Group 1 should be the group of characters intended to collide with
        Group 2 should be the group of weapons used to do the colliding
        """
        hits = pg.sprite.groupcollide(
            group_1, group_2, False, False, self.collide_with_rect
        )
        for character in hits:
            character.health -= self.damage
