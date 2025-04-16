from src.entities.entity import Entity
from src.util.vec2d import Vec2d
from src.constants import TILE_SIZE

from pygame import Surface, transform, image, display

class Effect(Entity):
    # static props
    SPRITE_SIZE = (TILE_SIZE, TILE_SIZE)
    
    # instance props
    _sprite: Surface
    _spawn_duration: int
    _despawn_duration: int
    _active_duration: int

    def __init__(self, sprite_path: str, spawn_duration, despawn_duration, active_duration):
        # need to do this because the position is set in super instantiation
        super().__init__(Vec2d(0, 0))

        self._sprite = transform.scale(image.load(sprite_path), Effect.SPRITE_SIZE)
        self._spawn_duration = spawn_duration
        self._despawn_duration = despawn_duration
        self._active_duration = active_duration

    def draw(self, screen: Surface):
        return screen.blit(self._sprite, self.pos) # type: ignore
    
    # TODO: add effect behaviours
    

class Cell:
    occupied: bool
    pos: Vec2d
    id: int

# random spawning in the map - do this with a tiling system
# get the dimensions of the window -- this is fixed anyway so we dont need to recalculate occupied cells
class EffectManager:
    effects: list[Effect]
    cells: list[Cell]
    num_occupied = 0

    def __init__(self):
        self.effects = []
        width, height = display.get_window_size()
        print(width, height)

    def spawn_effect(self, effect: Effect):
        pass