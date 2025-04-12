import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d
from src.entities.customer import *
from src.entities.ingredient import Ingredient


class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.speed = 5
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        self.sprite = pygame.image.load(sprite_path)
        self.score = 0
        # orders retrieved from the kitchen
        self.food_retrieved = None
        super().__init__(pos)

    # Set position and clamp within screen size
    def update(self, state):
        self.move()
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.interact_nearest(state)

    def move(self):
        keys = pygame.key.get_pressed()
        pos = Vec2d(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])

        # stop doubled speed when moving diagonally (~ sqrt(2)/2)
        speed_cap = 0.7 if pos.x != 0 and pos.y != 0 else 1

        self.hitbox.topleft = (
            max(min(self.hitbox.x + pos.x * self.speed * speed_cap, MAX_X), MIN_X),
            max(min(self.hitbox.y + pos.y * self.speed * speed_cap, MAX_Y), MIN_Y)
        )

        self.pos = self.hitbox.topleft

    def interact_nearest(self, entities):
        threshold_interact_distance = 100
        nearest_entity, nearest_distance = get_nearest_entity(self, entities)

        if type(nearest_entity) is Ingredient:
            if nearest_distance <= threshold_interact_distance:
                self.food_retrieved = nearest_entity.name
        elif type(nearest_entity) is Customer and self.food_retrieved:
            nearest_entity.interact(self.food_retrieved)
            self.food_retrieved = None

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.hitbox.topleft)
        if self.food_retrieved is not None:
            screen.blit(INGREDIENTS[self.food_retrieved], self.hitbox.topleft)
