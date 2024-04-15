from src.entities.entity import Entity


class Ingredient(Entity):
    def __init__(self, x_pos: int, y_pos: int, sprite_path: str, name: str):
        super().__init__(x_pos, y_pos, sprite_path)
        self.name = name

    def get_name(self) -> str:
        return self.name
