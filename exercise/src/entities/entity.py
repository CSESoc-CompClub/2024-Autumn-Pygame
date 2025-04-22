import pygame
from pygame.locals import *
from src.util.vec2d import *
import math

class Entity:
    # Base class for any object with a position in the game world.
    def __init__(self, pos: Vec2d):
        self.pos = pos

    # Return the current position as a new Vec2d.
    def get_position(self) -> Vec2d:
        return Vec2d(self.pos)


class NoRangeInteraction(Entity):
    # Marker class for entities that shouldn't be interacted with based on distance.
    pass


# Calculate and return the distance between two entities.
def get_entities_distance(entity1: Entity, entity2: Entity) -> float:
    pass  # TODO: Place your code here!


# Return the closest entity to the given one, skipping itself and any NoRangeInteraction objects.
def get_nearest_entity(entity: Entity, entities: list[Entity]) -> tuple[Entity, float]:
    pass  # TODO: Place your code here!
