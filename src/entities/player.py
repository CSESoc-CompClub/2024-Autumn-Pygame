import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d
from src.entities.customer import *
from src.entities.ingredient import Ingredient

def get_entities_distance(entity1: Entity, entity2: Entity):
    pos1 = entity1.get_position()
    pos2 = entity2.get_position()

    # use vec2d function supplied
    return pos1.get_distance(pos2)

def get_nearest_entity(entity: Entity, entities: list[Entity]) -> Entity:
    nearest_entity = entities[0]
    nearest_distance = 12031239
    for e in entities:
        if e != entity:
            distance = get_entities_distance(entity, e)
            if distance < nearest_distance:
                nearest_entity = e
                nearest_distance = distance

    print(nearest_distance, nearest_entity)

    return nearest_entity

class Player(Entity):
    def __init__(self, pos: Vec2d, sprite_path: str):
        self.speed = 5
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        self.sprite = pygame.image.load(sprite_path)
        # orders retrieved from the kitchen
        self.food_retrieved = None
        super().__init__(self.hitbox, pos)

    # Set position and clamp within screen size
    def update(self, state):
        keys = pygame.key.get_pressed()
        pos = Vec2d(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])

        # stop doubled speed when moving diagonally (~ sqrt(2)/2)
        speed_cap = 0.7 if pos.x != 0 and pos.y != 0 else 1

        self.hitbox.topleft = (
            max(
                min(
                    (self.hitbox.x + pos.x * self.speed * speed_cap),
                    (MAX_X),
                ),
                MIN_X,
            ),
            max(
                min(
                    (self.hitbox.y + pos.y * self.speed * speed_cap),
                    (MAX_Y),
                ),
                MIN_Y,
            ),
        )
        self.pos = self.hitbox.topleft

        if keys[K_SPACE]:
             self.interact_nearest(state)

    def interact_nearest(self, entities):
            nearest_entity = get_nearest_entity(self, entities)
            if type(nearest_entity) is Ingredient:
                if self.food_retrieved is None:
                    self.food_retrieved = nearest_entity
            elif type(nearest_entity) is Customer:
                if nearest_entity.interact(self.food_retrieved):
                    self.food_retrieved = None

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.hitbox.topleft)



