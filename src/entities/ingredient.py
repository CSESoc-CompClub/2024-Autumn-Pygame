from src.entities.entity import Entity
from src.util.vec2d import *
import pygame

class Ingredient(Entity):
    def __init__(self, pos, sprite_path: str, name: str):
        super().__init__(None, pos)
        self.name = name
        self.sprite = pygame.image.load(sprite_path)

    def draw(self, screen): 
        screen.blit(self.sprite, self.pos)

    def get_name(self) -> str:
        return self.name

    def update(self, entities: list[Entity]):
        pass