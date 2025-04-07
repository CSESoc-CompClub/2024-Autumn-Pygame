import copy
import random
from enum import *
from typing import *
from pygame import *
from src.entities.ingredient import INGREDIENTS
from src.entities.entity import *
from src.constants import *
from src.util.vec2d import *

class CState(Enum):
    WAITING_FOR_FOOD = 1
    EATING = 2
    LEAVING = 3

CUSTOMER_STATES: Dict[CState, Surface] = {
    CState.WAITING_FOR_FOOD: pygame.image.load("./sprites/temp/temp_item_tile.png"),
    CState.EATING: pygame.image.load("./sprites/temp/temp_item_tile.png"),
    CState.LEAVING: pygame.image.load("./sprites/temp/temp_item_tile.png"),
}

ANIMALS = [
    pygame.transform.scale(pygame.image.load(f"./sprites/animal{i}.png"), CUSTOMER_SIZE)
    for i in range(ANIMAL_LABEL_START, ANIMAL_LABEL_STOP + 1)
]

EATING_SPRITE: Surface = pygame.transform.scale(
    pygame.image.load("./sprites/eating.png"),
    EATING_SPRITE_SIZE
)

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)


class Customer(Entity):
    def __init__(
        self,
        order: str,
        player,
        pos: Vec2d,
    ):
        super().__init__(pos)
        self.order = order
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timer = 0
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.player = player
        self.sprite: Surface = random.choice(ANIMALS)

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

        # place status icon
        statex, statey = self.pos
        if self.state == CState.EATING:
            screen.blit(
                EATING_SPRITE,
                (statex + EATING_ICON_OFFSET_Y, statey + EATING_ICON_OFFSET_X)
            )
        else:
            screen.blit(
                INGREDIENTS[self.order],
                (statex + WAITING_ICON_OFFSET_Y, statey + WAITING_ICON_OFFSET_X)
            )

    def update(self, entities: list[Entity]):
        if self.state == CState.WAITING_FOR_FOOD:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(True)

        elif self.state == CState.EATING:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(False)

        elif self.state == CState.LEAVING:
            self.destroy(entities)

    def receive_order(self):
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.cur_timer = 0

    def start_eating(self):
        self.state = CState.EATING
        self.cur_timeout = EATING_TIMEOUT
        self.cur_timer = 0

    def leave(self, angry: bool):
        self.state = CState.LEAVING
        if angry == True:
            self.player.score -= 1
        else:
            self.player.score += 1

        self.cur_timeout = 0
        self.cur_timer = 0

    def destroy(self, entities: list[Entity]):
        entities.remove(self)

    def interact(self, food_retrieved):
        if self.state is CState.WAITING_FOR_FOOD:
            self.try_receive_order(food_retrieved)

    def try_receive_order(self, food_retrieved) -> bool:
        if self.order == food_retrieved:
            self.start_eating()
        else:
            self.leave(True)
