import copy
from enum import *
from typing import *
from pygame import *
from src.entities.entity import *
from src.entities.obstacle import *
from src.constants import *
from src.util.vec2d import *


class CState(Enum):
    WAITING_FOR_FOOD = 1
    EATING = 2
    LEAVING = 3


CUSTOMER_STATES: Dict[CState, Surface] = {
    CState.WAITING_FOR_FOOD: pygame.image.load("./sprites/temp/temp_sprite.png"),
    CState.EATING: pygame.image.load("./sprites/temp/temp_sprite.png"),
    CState.LEAVING: pygame.image.load("./sprites/temp/temp_sprite.png"),
}

CUSTOMER_SPRITE: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")

# 4 is most calm, 1 is almost angry
PROGRESS_BAR_4: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_3: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_2: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_1: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)

# TODO replace when actual sprites are available
CUSTOMER_EMPTY = Surface((0, 0))

WAITING_AT_ENTRANCE_TIMEOUT: int = 8000  # 8 seconds
WAITING_TO_ORDER_TIMEOUT: int = 8000  # 8 seconds
WAITING_FOR_FOOD_TIMEOUT: int = 8000  # 8 seconds
EATING_TIMEOUT: int = 240  # 5  mseconds

# TODO replace when map is complete
EXIT = Vec2d(550, 640)
ENTRANCE = Vec2d(50, 50)


class Customer(Entity):
    def __init__(
        self,
        order: str,
        pos: Vec2d = Vec2d(0, 0),
    ):
        super().__init__(None, pos)
        self.order = order
        self.angry = False
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timer = 0
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.hitbox = Rect(pos.x, pos.y, CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y)

    def draw(self, screen):
        screen.blit(CUSTOMER_SPRITE, self.hitbox.topleft)

        # place status icon
        statex, statey = self.hitbox.midtop
        statey -= 10
        status_icon_rect = CUSTOMER_STATES[self.state].get_rect(
            midbottom=(statex, statey)
        )
        screen.blit(CUSTOMER_STATES[self.state], status_icon_rect)

        # place waiting bar
        if (
            self.state == CState.WAITING_FOR_FOOD
        ):
            # 3 thresholds means for distinct progress bars
            bar: Surface = None

            if self.cur_timer < self.cur_timeout / 4:
                bar = PROGRESS_BAR_4
            elif self.cur_timer < 2 * self.cur_timeout / 4:
                bar = PROGRESS_BAR_3
            elif self.cur_timer < 3 * self.cur_timeout / 4:
                bar = PROGRESS_BAR_2
            else:
                bar = PROGRESS_BAR_1

            statusx, statusy = status_icon_rect.midtop
            statusy -= 10

            screen.blit(bar, bar.get_rect(midbottom=(statusx, statusy)))

    def update(self, entities: List[Entity]):
        if self.state == CState.WAITING_FOR_FOOD:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.angry = True
                self.leave(True)

        elif self.state == CState.EATING:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(False)

        elif self.state == CState.LEAVING:
            self.destroy(entities)

        print(self.state)
    def receive_order(self):
        self.state = CState.WAITING_FOR_FOOD

        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.cur_timer = 0

    def start_eating(self):
        print("eating")
        self.state = CState.EATING

        self.cur_timeout = EATING_TIMEOUT
        self.cur_timer = 0

    def leave(self, angry: bool):
        self.state = CState.LEAVING

        self.cur_timeout = 0
        self.cur_timer = 0

    def destroy(self, entities: List[Entity]):
        entities.remove(self)

    def interact(self, food_retrieved):
        print(self.state)
        if self.state is CState.WAITING_FOR_FOOD:
            self.try_receive_order(food_retrieved)
        elif self.state is CState.EATING:
            return
        else:
            self.place_order()

        print(self.state)

    def try_receive_order(self, food_retrieved) -> bool:
        if self.order == food_retrieved:
            self.start_eating()
            return True
        else:
            self.leave(True)
            return False
