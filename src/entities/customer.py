from enum import Enum
from typing import *
import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.entities.obstacle import TableSpot
from src.constants import *
from src.util.vec2d import Vec2d


class Order(Enum):
    FOOD1 = 1
    FOOD2 = 2
    FOOD3 = 3


class CustomerState(Enum):
    WAITING_AT_ENTRANCE = 1
    WALKING_TO_TABLE = 2
    WAITING_TO_ORDER = 3
    WAITING_FOR_FOOD = 4
    EATING = 5
    LEAVING = 6


CUSTOMER_HAPPY = "./sprites/temp/temp_sprite.png"
CUSTOMER_ANGRY = "./sprites/temp/temp_sprite.png"


WAITING_AT_ENTRANCE_TIMEOUT = 10000  # 10 seconds
WAITING_TO_ORDER_TIMEOUT = 10000  # 10 seconds
WAITING_FOR_FOOD_TIMEOUT = 10000  # 10 seconds
EATING_TIMEOUT = 10000  # 10 seconds


EXIT = Vec2d(600, 600)


class Customer:
    def __init__(
        self,
        order: Order = Order.FOOD1,
        pos: Vec2d = Vec2d(0, 0),
        state: CustomerState = CustomerState.WAITING_AT_ENTRANCE,
    ):
        self.happy_costume = pygame.image.load(CUSTOMER_HAPPY)
        self.angry_costume = pygame.image.load(CUSTOMER_ANGRY)
        self.sprite = self.happy_costume
        self.pos: Vec2d = pos
        self.hitbox_size: Vec2d = Vec2d(64, 64)
        self.table_pos: TableSpot = None
        self.order: Order = Order.FOOD1
        self.state: CustomerState = state

    def set_position(self, pos: Vec2d):
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.sprite, (self.pos.x, self.pos.y))

    def wait_at_entrance(self, pos: Vec2d):
        self.set_position(pos)
        self.state = CustomerState.WAITING_AT_ENTRANCE

        # main game loop should call move_to_table at some point...
        pygame.time.wait(WAITING_AT_ENTRANCE_TIMEOUT)

        if self.state == CustomerState.WAITING_AT_ENTRANCE:
            self.sprite = self.angry_costume
            self.leave()

    def move_to_table(self, spot: TableSpot, entities: List[Entity]):
        if (
            self.state != CustomerState.WAITING_AT_ENTRANCE
            and self.state != CustomerState.LEAVING
        ):
            raise Exception("Customer is not waiting at entrance")

        self.state = CustomerState.WALKING_TO_TABLE

        # A* algorithm
        open_set = {self.pos}
        came_from = {}
        g_score = {self.pos: 0}
        f_score = {self.pos: self.pos.get_distance(spot.pos)}

        while len(open_set):
            current = min(open_set, key=lambda x: f_score[x])

            # check if current is within +- TILE_SIZE/4 of spot
            if (
                current.x - TILE_SIZE / 4 <= spot.pos.x <= current.x + TILE_SIZE / 4
                and current.y - TILE_SIZE / 4 <= spot.pos.y <= current.y + TILE_SIZE / 4
            ):
                self.table_pos = spot
                spot.occupied = True

                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)

                path.reverse()
                for i in range(1, len(path)):
                    self.pos = path[i]
                    print(path[i])
                    # pygame.time.wait(0)
                self.state = CustomerState.WAITING_TO_ORDER
                return

            open_set.remove(current)

            neighbors = [
                Vec2d(current.x + dx, current.y + dy)
                for dx, dy in [
                    (TILE_SIZE / 4, 0),
                    (-TILE_SIZE / 4, 0),
                    (0, TILE_SIZE / 4),
                    (0, -TILE_SIZE / 4),
                    (TILE_SIZE / 4, TILE_SIZE / 4),
                    (-TILE_SIZE / 4, -TILE_SIZE / 4),
                    (TILE_SIZE / 4, -TILE_SIZE / 4),
                    (-TILE_SIZE / 4, TILE_SIZE / 4),
                ]
            ]

            for neighbor in neighbors:
                if any([entity.is_overlapping_point(neighbor) for entity in entities]):
                    continue

                tentative_g_score = g_score[current] + current.get_distance(neighbor)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.get_distance(
                        spot.pos
                    )
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        raise Exception("No path to table")

    def wait_to_order(self):
        if self.state != CustomerState.WAITING_TO_ORDER:
            raise Exception("Customer is not waiting to order")

        # create_order(self)
        # player should call wait_for_food at some point...
        pygame.time.wait(WAITING_TO_ORDER_TIMEOUT)
        if self.state == CustomerState.WAITING_TO_ORDER:
            self.sprite = self.angry_costume
            self.leave()

    def wait_for_food(self):
        if self.state != CustomerState.WAITING_TO_ORDER:
            raise Exception("Customer is not waiting for food")

        self.state = CustomerState.WAITING_FOR_FOOD

        # player should call serve_food at some point...
        pygame.time.wait(WAITING_FOR_FOOD_TIMEOUT)
        if self.state == CustomerState.WAITING_FOR_FOOD:
            self.sprite = self.angry_costume
            self.leave()

    def serve_food(self):
        if self.state != CustomerState.WAITING_FOR_FOOD:
            raise Exception("Customer is not eating")

        self.state = CustomerState.EATING

        pygame.time.wait(EATING_TIMEOUT)
        self.leave()

    def leave(self, entities: List[Entity]):
        self.state = CustomerState.LEAVING
        spot = TableSpot(EXIT, False)
        self.move_to_table(spot, entities)
        # delete this entity
