import copy
import random
import time
from enum import Enum
from typing import Dict
import pygame
from pygame import Surface
from src.entities.food import FOODS
from src.entities.entity import Entity
from src.constants import *
from src.util.vec2d import Vec2d

class CState(Enum):
    # Enum representing the customer's current state.
    WAITING_FOR_FOOD = 1
    EATING = 2
    LEAVING = 3

# Status icons shown based on customer state
CUSTOMER_STATES: Dict[CState, Surface] = {
    CState.WAITING_FOR_FOOD: pygame.image.load("./sprites/states/empty.png"),
    CState.EATING: pygame.image.load("./sprites/states/empty.png"),
    CState.LEAVING: pygame.image.load("./sprites/states/empty.png"),
}

CUSTOMER_SIZE = (100, 100)

# Preload and scale customer animal sprites
ANIMALS = {
    1: pygame.transform.scale(pygame.image.load("./sprites/customers/animal1.png"), CUSTOMER_SIZE),
    2: pygame.transform.scale(pygame.image.load("./sprites/customers/animal2.png"), CUSTOMER_SIZE),
    3: pygame.transform.scale(pygame.image.load("./sprites/customers/animal3.png"), CUSTOMER_SIZE),
    4: pygame.transform.scale(pygame.image.load("./sprites/customers/animal4.png"), CUSTOMER_SIZE),
}

EATING_SPRITE: Surface = pygame.transform.scale(
    pygame.image.load("./sprites/states/eating.png"), (120, 120)
)

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)

# Timeouts for different customer actions
WAITING_AT_ENTRANCE_TIMEOUT: int = 8000
WAITING_TO_ORDER_TIMEOUT: int = 8000
WAITING_FOR_FOOD_TIMEOUT: int = 8000
EATING_TIMEOUT: int = 240  # Frames, not milliseconds


class Customer(Entity):
    # Represents a customer that orders food, waits, eats, or leaves.
    def __init__(self, order: str, player, pos: Vec2d):
        # Create a customer with a food order, linked player and position.
        super().__init__(pos)
        self.order = order
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timer = 0
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.player = player
        self.sprite: Surface = ANIMALS[random.randint(1, 4)]
        self.time_at_leaving = None

    # Draw the customer and their current state icon (food or eating icon).
    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

        statex, statey = self.pos

        if self.state == CState.EATING:
            # Show eating icon
            screen.blit(EATING_SPRITE, (statex - 75, statey - 50))
        else:
            # Show the food they want
            screen.blit(FOODS[self.order], (statex - 50, statey - 25))

    # Update customer behavior depending on their current state.
    def update(self, entities: list[Entity], state):
        if self.state == CState.WAITING_FOR_FOOD:
            pass  # TODO: Place your code here!

        elif self.state == CState.EATING:
            pass  # TODO: Place your code here!

        elif self.state == CState.LEAVING:
            pass  # TODO: Place your code here!

    # Called when customer is ready to receive food.
    def receive_order(self):
        self.state = CState.WAITING_FOR_FOOD
        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.cur_timer = 0

    # Begin the eating phase and reset the timer.
    def start_eating(self):
        pass  # TODO: Place your code here!

    # Trigger customer leaving. Change score based on mood.
    def leave(self, angry: bool):
        pass  # TODO: Place your code here!

    # Remove the customer from the entity list.
    def destroy(self, entities: list[Entity]):
        pass  # TODO: Place your code here!

    # Check if the player gave the correct food.
    def try_receive_order(self, food_retrieved) -> bool:
        pass  # TODO: Place your code here!

    # Called when the player tries to give food to the customer.
    def interact(self, food_retrieved):
        pass  # TODO: Place your code here!
