import pygame
from pygame.locals import *
from src.constants import TILE_SIZE

class Entity():
    def __init__(self, x_pos: int, y_pos: int , sprite_path: str):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprite = pygame.image.load(sprite_path)
    
    def is_overlapping(self, other) -> bool:
        start_x = self.get_x() - (TILE_SIZE / 2)
        end_x = self.get_x() + (TILE_SIZE / 2)

        start_y = self.get_y() - (TILE_SIZE / 2)
        end_y = self.get_y() + (TILE_SIZE / 2)

        # must be between x and y
        return (other.get_x() >= start_x and other.get_x() <= end_x) and (other.get_y() >= start_y and other.get_y() <= end_y)
    
    def get_x(self):
        return self.x_pos + (TILE_SIZE / 2)
    
    def get_y(self):
        return self.y_pos + (TILE_SIZE / 2)