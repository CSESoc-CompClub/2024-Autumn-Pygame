import copy
from enum import *
from typing import *
from pygame import *
from src.entities.entity import *
from src.entities.obstacle import *
from src.constants import *
from src.util.vec2d import *
import math


class Order(Enum):
    FOOD1 = 1
    FOOD2 = 2
    FOOD3 = 3


class CState(Enum):
    WAITING_AT_ENTRANCE = 1
    MOVING_TO_TABLE = 2
    WAITING_TO_ORDER = 3
    WAITING_FOR_FOOD = 4
    EATING = 5
    LEAVING = 6


CUSTOMER_HAPPY: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
CUSTOMER_ANGRY: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
CUSTOMER_RAISED_HAND: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")

# 4 is most calm, 1 is almost angry
PROGRESS_BAR_4: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_3: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_2: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")
PROGRESS_BAR_1: Surface = pygame.image.load("./sprites/temp/temp_sprite.png")

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)

# TODO replace when actual sprites are available
CUSTOMER_HAPPY = transform.smoothscale(CUSTOMER_HAPPY, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_ANGRY = transform.smoothscale(CUSTOMER_ANGRY, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_RAISED_HAND = transform.smoothscale(CUSTOMER_RAISED_HAND, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_EMPTY = Surface((0, 0))

WAITING_AT_ENTRANCE_TIMEOUT: int = 8000  # 8 seconds
WAITING_TO_ORDER_TIMEOUT: int = 8000  # 8 seconds
WAITING_FOR_FOOD_TIMEOUT: int = 8000  # 8 seconds
EATING_TIMEOUT: int = 8000  # 8 seconds

# TODO replace when map is complete
EXIT = Vec2d(550, 640)
ENTRANCE = Vec2d(50, 50)


class Customer:
    def __init__(
        self,
        order: Order = Order.FOOD1,
        pos: Vec2d = Vec2d(0, 0),
    ):
        self.order = order
        self.wait_at_entrance(pos)

    def draw(self, screen):
        screen.blit(self.sprite, self.hitbox.topleft)
        
        if (
            self.state == CState.WAITING_AT_ENTRANCE
            or self.state == CState.WAITING_TO_ORDER
            or self.state == CState.WAITING_FOR_FOOD
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

            pos = copy.deepcopy(self.hitbox)

            barx, bary = self.hitbox.midtop
            bary -= 10

            screen.blit(bar, bar.get_rect(midbottom=(barx, bary)))


    def update(self, entities: List[Entity]):
        if self.state == CState.WAITING_AT_ENTRANCE:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(True, entities)
    
        elif self.state == CState.MOVING_TO_TABLE:
            self.place_order()

        elif self.state == CState.WAITING_TO_ORDER:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(True, entities)

        elif self.state == CState.WAITING_FOR_FOOD:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(True, entities)
    
        elif self.state == CState.EATING:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(False, entities)

        elif self.state == CState.LEAVING:
            self.destroy(entities)

    def wait_at_entrance(self, pos: Vec2d = ENTRANCE):
        self.state = CState.WAITING_AT_ENTRANCE
        self.sprite = CUSTOMER_HAPPY
        self.hitbox = Rect(pos.x, pos.y, CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y)

        self.cur_timeout = WAITING_AT_ENTRANCE_TIMEOUT
        self.cur_timer = 0

    def move_to_table(self, spot: TableSpot, entities: List[Entity]):
        self.state = CState.MOVING_TO_TABLE
        self.sprite = CUSTOMER_HAPPY
        self.hitbox.center = (spot.pos.x, spot.pos.y)

        self.cur_timeout = 0
        self.cur_timer = 0

    def place_order(self):
        self.state = CState.WAITING_TO_ORDER
        self.sprite = CUSTOMER_RAISED_HAND

        self.cur_timeout = WAITING_TO_ORDER_TIMEOUT
        self.cur_timer = 0

    def receive_order(self):
        self.state = CState.WAITING_FOR_FOOD
        self.sprite = CUSTOMER_HAPPY

        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.cur_timer = 0

    def start_eating(self):
        self.state = CState.EATING
        self.sprite = CUSTOMER_HAPPY

        self.cur_timeout = EATING_TIMEOUT
        self.cur_timer = 0   

    def leave(self, angry: bool, entities: List[Entity]):
        self.state = CState.LEAVING
        self.sprite = CUSTOMER_ANGRY if angry else CUSTOMER_HAPPY

        self.cur_timeout = 0
        self.cur_timer = 0

    def destroy(self, entities: List[Entity]):
        entities.remove(self)
        self.sprite = CUSTOMER_EMPTY

