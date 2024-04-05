import pygame
from pygame.locals import *
from src.util.vec2d import Vec2d


class Entity:
    def __init__(self, pos: Vec2d, hitbox_size: Vec2d, sprite_path: str):
        self.pos = pos
        self.hitbox_size = hitbox_size
        self.sprite = pygame.image.load(sprite_path)

    def is_overlapping(self, other) -> bool:
        return (
            self.pos.x < other.pos.x + other.hitbox_size.x
            and self.pos.x + self.hitbox_size.x > other.pos.x
            and self.pos.y < other.pos.y + other.hitbox_size.y
            and self.pos.y + self.hitbox_size.y > other.pos.y
        )

    def is_overlapping_point(self, point: Vec2d) -> bool:
        return (
            self.pos.x < point.x < self.pos.x + self.hitbox_size.x
            and self.pos.y < point.y < self.pos.y + self.hitbox_size.y
        )

    def get_position(self) -> Vec2d:
        return Vec2d(self.pos.x, self.pos.y)
