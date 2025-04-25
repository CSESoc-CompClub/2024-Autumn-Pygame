import pygame
from src.entities.entity import Entity
from src.util.vec2d import Vec2d

class RubbishBin(Entity):
    SIZE = (64, 64)

    def __init__(self, pos: Vec2d):
        super().__init__(pos)
        self.sprite = pygame.transform.scale(
            pygame.image.load("./sprites/rubbish_bin.png"), RubbishBin.SIZE
        )
        
        self._hitbox = pygame.Rect(pos.x, pos.y, *RubbishBin.SIZE)


    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.pos)

    def update(self, entities, state):
        pass
