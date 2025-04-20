from src.entities.effects.effect import Effect
from src.util.vec2d import Vec2d
from src.constants import SPEED_BOOST, SPEED_DURATION

class SpeedEffect(Effect):
    # Initialise speed effect with position
    def __init__(self, pos: Vec2d):
        super().__init__(
            sprite_path="./sprites/effects/speedboost.png",
            despawn_duration=5000,
            active_duration=10000,
            pos=pos
        )
        self.speed_boost = SPEED_BOOST
        self.speed_duration = SPEED_DURATION
