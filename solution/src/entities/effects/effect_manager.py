import pygame
from random import choice
from src.entities.effects.cell import Cell
from src.entities.entity import Entity
from src.entities.player import Player
from src.entities.effects.effect import Effect
from src.entities.effects.time_effect import TimeEffect
from src.entities.effects.speed_effect import SpeedEffect
from src.constants import SPEED_BOOST, TIME_LEFT, SPEED_DURATION, PLAYER_SPEED
from src.util.vec2d import Vec2d
from src.entities.food import FOODS

class EffectManager:
    # Manages effect spawning and activation
    def __init__(self):
        # Set up cells based on window size
        width, height = pygame.display.get_window_size()
        cols = width // Effect.SPRITE_SIZE[0]
        rows = height // Effect.SPRITE_SIZE[1]

        self.cells = list[Cell]()
        cell_id = 0
        for row in range(2, rows - 3):
            for col in range(1, cols - 1):
                self.cells.append(
                    Cell(id=cell_id, pos=Vec2d(x_or_pair=col, y=row) * Effect.SPRITE_SIZE)
                )
                cell_id += 1

        # Setup timed spawn events
        self.SPAWN_SPEED_EVENT = pygame.USEREVENT + 1
        self.SPAWN_TIME_EVENT = pygame.USEREVENT + 2

        pygame.time.set_timer(self.SPAWN_SPEED_EVENT, 15000)
        pygame.time.set_timer(self.SPAWN_TIME_EVENT, 10000)

        self.active_effects: dict[type[Effect], bool] = {SpeedEffect: False, TimeEffect: False}
        self.timers = dict()

    # Spawn effect only if it's not already active
    def spawn_effect(self, effect_subtype, entities: list[Entity]):
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

    # Handle scheduled spawn events
    def handle_events(self, event: pygame.event.Event, entities: list[Entity]):
        if event.type == self.SPAWN_SPEED_EVENT:
            self.spawn_effect(SpeedEffect, entities)
        elif event.type == self.SPAWN_TIME_EVENT:
            self.spawn_effect(TimeEffect, entities)

    # Clear cells for expired effects
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

    # Check for collisions between player and effects
    def collide(self, player, entities):
        for effect in [x for x in entities if isinstance(x, Effect)]:
            if player.hitbox.colliderect(effect._hitbox):
                return effect

    # Check if player has picked up an effect and apply it
    def activate_effect(self, entities: list[Entity], state):
        for entity in entities:
            if type(entity) == Player:
                player = entity
                break

        # SOLUTION START --
        effect = self.collide(player, entities)
        if effect:
            if type(effect) == TimeEffect:
                state[TIME_LEFT] += effect.time_boost
            elif type(effect) == SpeedEffect:
                player.speed *= effect.speed_boost
                self.timers[SpeedEffect] = pygame.time.get_ticks() + effect.speed_duration

            entities.remove(effect)

        # Update any effect timers
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
        # -- SOLUTION END
