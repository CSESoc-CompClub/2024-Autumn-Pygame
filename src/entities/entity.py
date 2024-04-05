import pygame
from pygame.locals import *
from src.util.vec2d import *


class Entity:
    def __init__(self, hitbox: Rect):
        self.hitbox = hitbox

    def get_position(self) -> Vec2d:
        return Vec2d(self.pos)
