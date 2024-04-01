import pygame
from pygame.locals import *
from src.constants import *

class Player():
    def __init__(self):
        self.x_pos = 400
        self.y_pos = 300
        self.speed = 5
        self.sprite = pygame.image.load("./sprites/temp/temp_sprite.png")

    # Set position and clamp within screen size
    def set_position(self, dx: int, dy: int) -> None:
        # stop doubled speed when diagonal (~ sqrt(2)/2)
        speed_cap = 0.7 if dx != 0 and dy != 0 else 1
        self.x_pos = max(min((self.x_pos + dx * self.speed * speed_cap),((GRID_SIZE_X - 1) * TILE_SIZE)), 0)
        self.y_pos = max(min((self.y_pos + dy * self.speed * speed_cap), ((GRID_SIZE_Y - 1) * TILE_SIZE)), 0)
