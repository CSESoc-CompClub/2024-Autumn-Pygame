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

CUSTOMER_HITBOX_SIZE: Vec2d = Vec2d(TILE_SIZE / 2, TILE_SIZE)

# TODO replace when actual sprites are available
CUSTOMER_HAPPY = transform.smoothscale(CUSTOMER_HAPPY, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_ANGRY = transform.smoothscale(CUSTOMER_ANGRY, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_RAISED_HAND = transform.smoothscale(CUSTOMER_RAISED_HAND, (CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y))
CUSTOMER_EMPTY = Surface((0, 0))

WAITING_AT_ENTRANCE_TIMEOUT: int = 10000  # 10 seconds
WAITING_TO_ORDER_TIMEOUT: int = 10000  # 10 seconds
WAITING_FOR_FOOD_TIMEOUT: int = 10000  # 10 seconds
EATING_TIMEOUT: int = 10000  # 10 seconds

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

    def update(self, entities: List[Entity]):
        if self.state == CState.WAITING_AT_ENTRANCE:
            self.cur_timer += 1
            if self.cur_timer >= self.cur_timeout:
                self.leave(True, entities)
    
        elif self.state == CState.MOVING_TO_TABLE:
            if self.pathfind_index < len(self.pathfind_path):
                self.hitbox.topleft = self.pathfind_path[self.pathfind_index]
                self.pathfind_index += 1
            else:
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
            if self.pathfind_index < len(self.pathfind_path):
                self.hitbox.topleft = self.pathfind_path[self.pathfind_index]
                self.pathfind_index += 1
            else:
                self.destroy(entities)

    def wait_at_entrance(self, pos: Vec2d = ENTRANCE):
        self.state = CState.WAITING_AT_ENTRANCE
        self.sprite = CUSTOMER_HAPPY
        self.hitbox = Rect(pos.x, pos.y, CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y)
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = WAITING_AT_ENTRANCE_TIMEOUT
        self.cur_timer = 0

    def move_to_table(self, spot: TableSpot, entities: List[Entity]):
        self.state = CState.MOVING_TO_TABLE
        self.sprite = CUSTOMER_HAPPY

        # Will be updated by move
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = 0
        self.cur_timer = 0

        self.move(spot.pos, entities)

    def place_order(self):
        self.state = CState.WAITING_TO_ORDER
        self.sprite = CUSTOMER_RAISED_HAND
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = WAITING_TO_ORDER_TIMEOUT
        self.cur_timer = 0

    def receive_order(self):
        self.state = CState.WAITING_FOR_FOOD
        self.sprite = CUSTOMER_HAPPY
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = WAITING_FOR_FOOD_TIMEOUT
        self.cur_timer = 0

    def start_eating(self):
        self.state = CState.EATING
        self.sprite = CUSTOMER_HAPPY
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = EATING_TIMEOUT
        self.cur_timer = 0   

    def leave(self, angry: bool, entities: List[Entity]):
        self.state = CState.LEAVING
        self.sprite = CUSTOMER_ANGRY if angry else CUSTOMER_HAPPY

        # Will be updated by move
        self.pathfind_dest = None
        self.pathfind_path = []
        self.pathfind_index = 0

        self.cur_timeout = 0
        self.cur_timer = 0

    def destroy(self, entities: List[Entity]):
        entities.remove(self)
        self.sprite = CUSTOMER_EMPTY
        

    def move(self, dest: Vec2d, entities: List[Entity], callback: Callable = None):
        entities = [e for e in entities if e != self]
        collider = self.hitbox.collideobjects(entities, key=lambda o: o.hitbox)
        if collider:
            raise Exception(f"Customer {str(self)} @ {self.hitbox} already colliding with entity {str(collider)} @ {collider.hitbox}!")

        print(f"Moving customer {str(self)} from {self.hitbox.topleft} to {dest}")

        self.pathfind_dest = dest
        self.pathfind_path = []
        self.pathfind_index = 0

        # A*
        src = Vec2d(self.hitbox.x, self.hitbox.y)
        open_set: Set[Vec2d] = {src}
        came_from: Set[Vec2d] = {}
        g_score: Dict[Vec2d, float] = {src: 0}
        f_score: Dict[Vec2d, float] = {src: src.get_distance(dest)}

        fuzzy_dest = Rect(dest.x, dest.y, 8, 8)
        fuzzy_dest.center = (dest.x, dest.y)
        canvas = Rect(0, 0, GRID_SIZE_X * TILE_SIZE, GRID_SIZE_Y * TILE_SIZE)

        while len(open_set):
            current = min(open_set, key=lambda x: f_score[x])

            # print("Current: ", current)
            if fuzzy_dest.colliderect(Rect(current.x, current.y, CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y)):
                print(f"Found path to destination {dest} for customer {str(self)}")
                self.pathfind_path = [current]
                while current in came_from:
                    current = came_from[current]
                    self.pathfind_path.append(current)

                self.pathfind_path.reverse()
                return

            open_set.remove(current)

            neighbors = [
                Rect(current.x + dx, current.y + dy, CUSTOMER_HITBOX_SIZE.x, CUSTOMER_HITBOX_SIZE.y)
                for dx, dy in [
                    (4, 0),
                    (-4, 0),
                    (0, 4),
                    (0, -4),
                    (4, 4),
                    (4, -4),
                    (-4, 4),
                    (-4, -4)
                ]
            ]

            for neighbor in neighbors:
                n_vec2d = Vec2d(neighbor.x, neighbor.y)
                if (
                    neighbor.collideobjects(entities, key=lambda o: o.hitbox) 
                ):
                    continue

                tentative_g_score = g_score[current] + current.get_distance(n_vec2d)
                if n_vec2d not in g_score or tentative_g_score < g_score[n_vec2d]:
                    came_from[n_vec2d] = current
                    g_score[n_vec2d] = tentative_g_score
                    f_score[n_vec2d] = tentative_g_score + n_vec2d.get_distance(dest)
                    if n_vec2d not in open_set:
                        open_set.add(n_vec2d)

        raise Exception("No path to destination found!")
