from src.entities.entity import Entity
from src.util.vec2d import *
from src.constants import *
import pygame

SPRITE_SIZE = (TILE_SIZE, TILE_SIZE)

FOODS = {
    "watermelon": pygame.transform.scale(pygame.image.load("./sprites/watermelon.png"), SPRITE_SIZE),
    "sushi": pygame.transform.scale(pygame.image.load("./sprites/sushi.png"), SPRITE_SIZE),
    "peach": pygame.transform.scale(pygame.image.load("./sprites/peach.png"), SPRITE_SIZE),
    "banana": pygame.transform.scale(pygame.image.load("./sprites/banana.png"), SPRITE_SIZE),
    "grapes": pygame.transform.scale(pygame.image.load("./sprites/grapes.png"), SPRITE_SIZE),
    "strawberry": pygame.transform.scale(pygame.image.load("./sprites/strawberry.png"), SPRITE_SIZE)
}

def num_food() -> int: 
    return len(FOODS)


class Food(Entity):
    def __init__(self, pos, sprite: str, name: str):
        super().__init__(pos)
        self.name = name
        self.sprite = sprite

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def get_name(self) -> str:
        return self.name

    def update(self, entities: list[Entity]):
        pass
