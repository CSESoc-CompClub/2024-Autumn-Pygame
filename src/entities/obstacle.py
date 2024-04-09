from typing import *
from dataclasses import dataclass
import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d


@dataclass
class TableSpot:
    pos: Vec2d
    occupied: bool


class Table(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str, spots: List[TableSpot] = []):
        super().__init__(pos)
        self.sprite = pygame.image.load(sprite_path)
        self.spots = spots

    def draw(self, screen):
        screen.blit(self.sprite, (self.pos.x, self.pos.y))
