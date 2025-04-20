import pygame
from random import choice
from abc import ABC
from pygame.rect import *

from src.entities.entity import Entity, NoRangeInteraction
from src.util.vec2d import Vec2d
from src.constants import TILE_SIZE
from src.entities.player import *

from dataclasses import dataclass
from typing import Union

class Effect(NoRangeInteraction, ABC):
    # static props
    SPRITE_SIZE = (TILE_SIZE, TILE_SIZE)
    
    # instance props
    _sprite: pygame.Surface
    _despawn: int
    _active: int

    def __init__(self, sprite_path: str, despawn_duration, active_duration, pos: Vec2d):
        # need to do this because the position is set in super instantiation
        super().__init__(pos)
        self._hitbox = Rect(pos.x - TILE_SIZE, pos.y - TILE_SIZE, TILE_SIZE, TILE_SIZE)

        self._sprite = pygame.transform.scale(pygame.image.load(sprite_path), Effect.SPRITE_SIZE)
        self._despawn = despawn_duration
        self._active = active_duration
        self._spawn_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface):
        return screen.blit(self._sprite, self.pos) # type: ignore
    
    def update(self, entities: list[Entity], state):      
        current_time = pygame.time.get_ticks()
        if current_time - self._spawn_time >= self._despawn:
            entities.remove(self)


class SpeedEffect(Effect):
    def __init__(self, pos: Vec2d):
        super().__init__(
            sprite_path="./sprites/speedboost.png",
            despawn_duration=5000,
            active_duration=10000,
            pos=pos
        )
        self.speed_boost = SPEED_BOOST
        self.speed_duration = SPEED_DURATION

class TimeEffect(Effect):
    def __init__(self, pos: Vec2d):
        super().__init__(
            sprite_path="./sprites/timeboost.png",
            despawn_duration=5000,
            active_duration=5000,
            pos=pos
        )
        self.time_boost = TIME_BOOST
    

@dataclass
class Cell:
    pos: Vec2d
    id: int
    effect: Union[Effect, None] = None

class EffectManager:
    # get the dimensions of the window -- this is fixed anyway so we dont need to recalculate occupied cells
    def __init__(self):
        width, height = pygame.display.get_window_size()
        cols = width // Effect.SPRITE_SIZE[0]
        rows = height // Effect.SPRITE_SIZE[1]

        cell_id = 0
        self.cells = list[Cell]()
        for row in range(2, rows-3):
            for col in range(1, cols-1):
                self.cells.append(
                    Cell(id=cell_id, pos=Vec2d(x_or_pair=col, y=row) * Effect.SPRITE_SIZE)
                )
                cell_id += 1

        self.SPAWN_SPEED_EVENT = pygame.USEREVENT + 1
        self.SPAWN_TIME_EVENT = pygame.USEREVENT + 2

        pygame.time.set_timer(self.SPAWN_SPEED_EVENT, 15_000)
        pygame.time.set_timer(self.SPAWN_TIME_EVENT, 10_000)

        self.active_effects: dict[type[Effect], bool] = {SpeedEffect: False, TimeEffect: False}
        self.timers = dict()

    def spawn_effect(self, effect_subtype, entities: list[Entity]):
        # don't spawn more effects if that effect type is currently spawned
        if self.active_effects[effect_subtype]:
            return

        available_cells = [c for c in self.cells if c.effect is None]
        if not available_cells:
            return
        
        cell = choice(available_cells)
        effect = effect_subtype(pos=cell.pos)
        
        self.cells[cell.id].effect = effect
        self.active_effects[effect_subtype] = True
        entities.append(effect)

    def handle_events(self, event: pygame.event.Event, entities: list[Entity]):
        if event.type == self.SPAWN_SPEED_EVENT:
            self.spawn_effect(SpeedEffect, entities)
        elif event.type == self.SPAWN_TIME_EVENT:
            self.spawn_effect(TimeEffect, entities)

    def update(self, entities: list[Entity], state):
        for cell in self.cells:
            if cell.effect is None or cell.effect in entities:
                continue

            for effect_class in self.active_effects:
                if isinstance(cell.effect, effect_class) and self.active_effects[effect_class]:
                    self.active_effects[effect_class] = False
                    break

            cell.effect = None
        self.activate_effect(entities, state)
    
    def collide(self, player, entities):
        for effect in [x for x in entities if isinstance(x, Effect)]:
            if player.hitbox.colliderect(effect._hitbox):
                return effect
    
    def activate_effect(self, entities: list[Entity], state):
        for entity in entities:
            if type(entity) == Player:
                player = entity
                break
        
        effect = self.collide(player, entities)
        if effect:
            if type(effect) == TimeEffect:
                state[TIME_LEFT] += effect.time_boost
            elif type(effect) == SpeedEffect:
                player.speed *= effect.speed_boost
                self.timers[SpeedEffect] = pygame.time.get_ticks() + effect.speed_duration
            entities.remove(effect)

        # Process timers for effects
        current_time = pygame.time.get_ticks()
        for timer in [x for x in self.timers.keys() if self.timers[x] is not None]:
            if timer == SpeedEffect: 
                time_left = self.timers[SpeedEffect] - current_time
                # Decaying speed boost
                bonus_speed = time_left / SPEED_DURATION * SPEED_BOOST
                player.speed = PLAYER_SPEED + bonus_speed
                if time_left <= 0:
                    player.speed = PLAYER_SPEED
                    self.timers[SpeedEffect] = None

        