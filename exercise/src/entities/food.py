from src.entities.entity import Entity
from src.util.vec2d import *
from src.constants import *
import pygame

# Size for all food sprites
SPRITE_SIZE = (TILE_SIZE, TILE_SIZE)

# Preload and scale all food sprites
FOODS = {
    "watermelon": pygame.transform.scale(pygame.image.load("./sprites/food/watermelon.png"), SPRITE_SIZE),
    "sushi": pygame.transform.scale(pygame.image.load("./sprites/food/sushi.png"), SPRITE_SIZE),
    "peach": pygame.transform.scale(pygame.image.load("./sprites/food/peach.png"), SPRITE_SIZE),
    "banana": pygame.transform.scale(pygame.image.load("./sprites/food/banana.png"), SPRITE_SIZE),
    "grapes": pygame.transform.scale(pygame.image.load("./sprites/food/grapes.png"), SPRITE_SIZE),
    "strawberry": pygame.transform.scale(pygame.image.load("./sprites/food/strawberry.png"), SPRITE_SIZE)
}

def num_food() -> int:
    # Return the number of different food types.
    return len(FOODS)


class Food(Entity):
    # Create a Food object with position, sprite and name.
    def __init__(self, pos, sprite: str, name: str):
        super().__init__(pos)
        self.name = name  # Set the name of the food
        self.sprite = sprite  # Assign the sprite for the food

    # Draw the food sprite on the screen at its position.
    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    # Return the name of the food item.
    def get_name(self) -> str:
        return self.name

    # Food doesn't update itself, but required for consistency with other entities.
    def update(self, entities: list[Entity], state):
        pass
