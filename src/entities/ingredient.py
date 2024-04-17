from src.entities.entity import Entity
from src.util.vec2d import *
import pygame


INGREDIENTS = {
    "watermelon": pygame.transform.scale(pygame.image.load("./sprites/watermelon.png"), (120, 120)),
    "sushi": pygame.transform.scale(pygame.image.load("./sprites/sushi.png"), (120, 120))
}


class Ingredient(Entity):
    def __init__(self, pos, sprite: str, name: str):
        super().__init__(None, pos)
        self.name = name
        self.sprite = sprite

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def get_name(self) -> str:
        return self.name

    def update(self, entities: list[Entity]):
        pass
