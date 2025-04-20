from src.util.vec2d import Vec2d
from typing import Union
from src.entities.effects.effect import Effect

class Cell:
    # Initialise the cell with position, unique id and optional effect
    def __init__(self, pos: Vec2d, id: int, effect: Union[Effect, None] = None):
        self.pos = pos
        self.id = id
        self.effect = effect
