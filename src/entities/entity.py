import pygame
from pygame.locals import *
from src.util.vec2d import *

class Entity:
    def __init__(self, pos: Vec2d):
        self.pos = pos

    def get_position(self) -> Vec2d:
        return Vec2d(self.pos)

def get_entities_distance(entity1: Entity, entity2: Entity):
    pos1 = entity1.get_position()
    pos2 = entity2.get_position()

    # use vec2d function supplied
    return pos1.get_distance(pos2)


def get_nearest_entity(entity: Entity, entities: list[Entity]) -> tuple[Entity, float]:
    nearest_entity = entities[0]
    nearest_distance = math.inf 
    for e in entities:
        if e != entity:
            distance = get_entities_distance(entity, e)
            if distance < nearest_distance:
                nearest_entity = e
                nearest_distance = distance
    return nearest_entity, nearest_distance