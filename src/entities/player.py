import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d
from src.entities.customer import *
from src.entities.ingredient import Ingredient

# TODO: return the distance between two entities
# HINT -> use entity.pos
def get_entities_distance(entity1: Entity, entity2: Entity):
    pass

# TODO: return the nearest entity between
# HINT: -> use `get_entities_distance(...)`
# HINT: -> make sure that the entities you are comparing are not the same
def get_nearest_entity(player: Entity, entities: list[Entity]) -> Entity:
    return player


class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.speed = 5
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        self.sprite = pygame.image.load(sprite_path)
        self.score = 0
        # orders retrieved from the kitchen
        self.food_retrieved = None
        super().__init__(pos)

    def update(self, entities):
        pass

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
        pass

    def draw(self, screen: pygame.Surface):
        pass
