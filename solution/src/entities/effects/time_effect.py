from src.entities.effects.effect import Effect
from src.util.vec2d import Vec2d
from src.constants import TIME_BOOST

class TimeEffect(Effect):
    # Initialise time effect with position
    # SOLUTION START --
    def __init__(self, pos: Vec2d):
        super().__init__(
            sprite_path="./sprites/effects/timeboost.png",
            despawn_duration=5000,
            active_duration=5000,
            pos=pos
        )
        self.time_boost = TIME_BOOST
    # -- SOLUTION END