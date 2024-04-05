import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d


class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.speed = 5
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        self.sprite = pygame.image.load(sprite_path)

    # Set position and clamp within screen size
    def update(self, entities: list[Entity]):
        keys = pygame.key.get_pressed()
        pos = Vec2d(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])

        # stop doubled speed when diagonal (~ sqrt(2)/2)
        speed_cap = 0.7 if pos.x != 0 and pos.y != 0 else 1

        self.hitbox.topleft = (
            max(
                min(
                    (self.hitbox.x + pos.x * self.speed * speed_cap),
                    ((GRID_SIZE_X - 1) * TILE_SIZE),
                ),
                0,
            ),
            max(
                min(
                    (self.hitbox.y + pos.y * self.speed * speed_cap),
                    ((GRID_SIZE_Y - 1) * TILE_SIZE),
                ),
                0,
            ),
        )
