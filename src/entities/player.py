import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d


class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.pos = pos
        self.speed = 5
        self.hitbox_size = Vec2d(64, 64)
        self.sprite = pygame.image.load(sprite_path)

    # Set position and clamp within screen size
    def set_position(self, pos: Vec2d):
        # stop doubled speed when diagonal (~ sqrt(2)/2)
        speed_cap = 0.7 if pos.x != 0 and pos.y != 0 else 1
        self.pos.x = max(
            min(
                (self.pos.x + pos.x * self.speed * speed_cap),
                ((GRID_SIZE_X - 1) * TILE_SIZE),
            ),
            0,
        )
        self.pos.y = max(
            min(
                (self.pos.y + pos.y * self.speed * speed_cap),
                ((GRID_SIZE_Y - 1) * TILE_SIZE),
            ),
            0,
        )
