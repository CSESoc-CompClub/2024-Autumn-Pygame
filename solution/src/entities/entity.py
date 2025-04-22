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
    # SOLUTION START --
    pos1 = entity1.get_position()
    pos2 = entity2.get_position()

    # Use Vec2d distance method
    return pos1.get_distance(pos2)
    # -- SOLUTION END


# Return the closest entity to the given one, skipping itself and any NoRangeInteraction objects.
def get_nearest_entity(entity: Entity, entities: list[Entity]) -> tuple[Entity, float]:
    # SOLUTION START --
    nearest_entity = entities[0]
    nearest_distance = math.inf  # Start with a large number

    for e in entities:
        # Skip self and non-interactable entities
        if e != entity and not isinstance(e, NoRangeInteraction):
            distance = get_entities_distance(entity, e)
            if distance < nearest_distance:
                nearest_entity = e
                nearest_distance = distance

    return nearest_entity, nearest_distance
    # -- SOLUTION END
