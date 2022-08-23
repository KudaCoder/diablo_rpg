import pygame as pg

from .base import Character
from conf.settings import (
    WHITE,
    PURPLE,
    SCALE_SIZE,
    ENEMY_SPEED,
    PLAYER_SPEED,
    AVOID_RADIUS,
    ATTACK_RADIUS,
    COLLISION_RECT,
    PLAYER_ROT_SPEED,
    ENGAGEMENT_RADIUS,
)
from weapons import Sword

vec = pg.math.Vector2


class Player(Character):
    def __init__(self, game, x, y):
        super(Player, self).__init__(game, x, y)
        self.groups = self.game.all_sprites, self.game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.load_images("player")
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.collision_rect = COLLISION_RECT.copy()
        self.collision_rect.center = self.rect.center

        self.role = "player"
        self.weapon = Sword(game, self, self.game.player_weapons)

        self.main_health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 50, 15
        )
        self.health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 48, 13
        )

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mice = pg.mouse.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if mice[0]:
            self.weapon.attack(self.game.enemies, self.game.player_weapons)

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.animate()

        self.get_keys()
        self.rect = self.image.get_rect()
        self.collision_rect.center = self.pos
        self.pos.x += self.vel.x * self.game.dt
        self.pos.y += self.vel.y * self.game.dt

        self.collision_rect.centerx = self.pos.x
        self.collide_with_walls(self, self.game.obstacles, "x")
        self.collision_rect.centery = self.pos.y
        self.collide_with_walls(self, self.game.obstacles, "y")
        self.rect.center = self.collision_rect.center

        self.main_health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 50, 15
        )
        self.health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2) + 1,
            self.pos.y - self.rect.height + 1,
            48 * (self.health / 100),
            13,
        )

        if self.health <= 0:
            self.kill_all()


class Enemy(Character):
    def __init__(self, game, x, y):
        super(Enemy, self).__init__(game, x, y)
        self.groups = self.game.all_sprites, self.game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.load_images("enemy")
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.collision_rect = COLLISION_RECT.copy()
        self.collision_rect.center = self.rect.center

        self.role = "enemy"
        self.weapon = Sword(game, self, self.game.enemy_weapons)

        self.main_health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 50, 15
        )
        self.health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 48, 13
        )

    def avoid_enemies(self):
        for enemy in self.game.enemies:
            if enemy != self:
                distance = self.pos - enemy.pos
                if 0 < distance.length() < AVOID_RADIUS:
                    self.vel = distance.normalize()

    def update(self):
        self.animate()

        self.vel = vec(0, 0)

        self.collision_rect.center = self.pos
        distance_to_player = self.pos - self.game.player.pos
        if AVOID_RADIUS < distance_to_player.length() < ENGAGEMENT_RADIUS:
            self.vel = -(distance_to_player)
            self.vel.normalize()
            self.avoid_enemies()
            self.vel.scale_to_length(ENEMY_SPEED)

            self.pos.x += self.vel.x * self.game.dt
            self.pos.y += self.vel.y * self.game.dt

        if distance_to_player.length() <= ATTACK_RADIUS:
            self.weapon.attack(self.game.players, self.game.enemy_weapons)

        self.collision_rect.centerx = self.pos.x
        self.collide_with_walls(self, self.game.obstacles, "x")
        self.collision_rect.centery = self.pos.y
        self.collide_with_walls(self, self.game.obstacles, "y")
        self.rect.center = self.collision_rect.center

        self.main_health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2), self.pos.y - self.rect.height, 50, 15
        )
        self.health_rect = pg.Rect(
            self.pos.x - (self.rect.width / 2) + 1,
            self.pos.y - self.rect.height + 1,
            48 * (self.health / 100),
            13,
        )

        if self.health <= 0:
            self.kill_all()
