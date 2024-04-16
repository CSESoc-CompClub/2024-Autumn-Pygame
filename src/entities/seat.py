import pygame
# from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d


class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        # temp
        self.sprite = pygame.image.load(sprite_path)
