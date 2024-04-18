import pygame
from pygame.locals import *
from src.util.vec2d import *

class Entity:
    def __init__(self, hitbox: Rect, pos: Vec2d):
        self.hitbox = hitbox
        self.pos = pos

    def get_position(self) -> Vec2d:
        return Vec2d(self.pos)
