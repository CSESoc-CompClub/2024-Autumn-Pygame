import pygame
from pygame.rect import Rect
from src.entities.entity import NoRangeInteraction
from src.util.vec2d import Vec2d
from abc import ABC
from src.constants import TILE_SIZE

class Effect(NoRangeInteraction, ABC):
    SPRITE_SIZE = (TILE_SIZE, TILE_SIZE)

    # Initialise the effect with sprite path, despawn duration, active duration and position
    def __init__(self, sprite_path: str, despawn_duration, active_duration, pos: Vec2d):
        NoRangeInteraction.__init__(self, pos)
        self._hitbox = Rect(pos.x - TILE_SIZE, pos.y - TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self._sprite = pygame.transform.scale(pygame.image.load(sprite_path), Effect.SPRITE_SIZE)
        self._despawn = despawn_duration
        self._active = active_duration
        self._spawn_time = pygame.time.get_ticks()


    # Draw the effect sprite on the screen
    def draw(self, screen: pygame.Surface):
        return screen.blit(self._sprite, self.pos)

    # Update the effect, remove it after its despawn time
    def update(self, entities, state):
        current_time = pygame.time.get_ticks()
        if current_time - self._spawn_time >= self._despawn:
            entities.remove(self)
