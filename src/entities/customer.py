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

CUSTOMER_SIZE = (100, 100)
ANIMALS = {
    1: pygame.transform.scale(pygame.image.load("./sprites/animal1.png"), CUSTOMER_SIZE),
    2: pygame.transform.scale(pygame.image.load("./sprites/animal2.png"), CUSTOMER_SIZE),
    3: pygame.transform.scale(pygame.image.load("./sprites/animal3.png"), CUSTOMER_SIZE),
    4: pygame.transform.scale(pygame.image.load("./sprites/animal4.png"), CUSTOMER_SIZE),
}

EATING_SPRITE: Surface = pygame.transform.scale(pygame.image.load("./sprites/eating.png"), (120, 120))

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)

WAITING_AT_ENTRANCE_TIMEOUT: int = 8000  # 8 seconds
WAITING_TO_ORDER_TIMEOUT: int = 8000  # 8 seconds
WAITING_FOR_FOOD_TIMEOUT: int = 8000  # 8 seconds
EATING_TIMEOUT: int = 240  # 5  mseconds


class Customer(Entity):
    def __init__(
        self,
        order: str,
        player,
        pos: Vec2d,
    ):
        super().__init__(pos)
        self.order = order
        self.angry = False
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timer = 0
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.player = player
        self.sprite: Surface = ANIMALS[random.randint(1, 4)]

    def draw(self, screen):
        # TODO: Write your code here
        pass

    def update(self, entities: list[Entity]):
        # TODO: Write your code here
        pass

    def start_eating(self):
        # TODO: Write your code here
        pass

    def leave(self, angry: bool):
        # TODO: Write your code here
        pass

    def destroy(self, entities: list[Entity]):
        # TODO: Write your code here
        pass

    def interact(self, food_retrieved):
        # TODO: Write your code here
        pass

    def try_receive_order(self, food_retrieved) -> bool:
        # TODO: Write your code here
        pass
