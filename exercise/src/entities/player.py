import pygame
from pygame.rect import *
from pygame.locals import *
from src.entities.entity import *
from src.constants import *
from src.util.vec2d import Vec2d
from src.entities.customer import *
from src.entities.food import Food

# Load and scale a sprite to a given size
def load_sprite(sprite_path: str, size: tuple[int, int]):
    return pygame.transform.scale(pygame.image.load(sprite_path), size)

class Player(Entity):
    PLAYER_SIZE = (100, 100)

    # Load directional sprites
    MOVE_UP_SPRITE = load_sprite("./sprites/player/poco_up.png", PLAYER_SIZE)
    MOVE_DOWN_SPRITE = load_sprite("./sprites/player/poco_down.png", PLAYER_SIZE)
    MOVE_LEFT_SPRITE = load_sprite("./sprites/player/poco_left.png", PLAYER_SIZE)
    MOVE_RIGHT_SPRITE = load_sprite("./sprites/player/poco_right.png", PLAYER_SIZE)

    # Initialise position, hitbox, speed and default sprite
    def __init__(self, pos: Vec2d, sprite_path: str):
        # Initialise position, hitbox, speed and default sprite
        self.speed = PLAYER_SPEED
        self.hitbox = Rect(pos.x, pos.y, TILE_SIZE, TILE_SIZE)
        self.sprite = load_sprite(sprite_path, Player.PLAYER_SIZE)
        self.score = 0
        self.food_retrieved = None  # Holds food name if carrying
        super().__init__(pos)

    # Called every frame to update player logic
    def update(self, entities: list[Entity], state):
        self.move()

        # Check for interaction key
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.interact_nearest(entities)

    # Handle movement and update sprite based on direction
    def move(self):
        keys = pygame.key.get_pressed()
        pos = Vec2d(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])

        # Apply diagonal movement speed cap
        speed_cap = 0.7 if pos.x != 0 and pos.y != 0 else 1

        # Update hitbox and clamp within map bounds
        self.hitbox.topleft = (
            max(min(self.hitbox.x + pos.x * self.speed * speed_cap, MAX_X), MIN_X),
            max(min(self.hitbox.y + pos.y * self.speed * speed_cap, MAX_Y), MIN_Y)
        )

        # Update position
        self.pos = self.hitbox.topleft

        # Skip sprite change if not moving
        if pos.x == 0 and pos.y == 0:
            return

        # Set sprite based on movement angle
        angle = pos.get_angle()
        if angle == -90:
            self.sprite = Player.MOVE_UP_SPRITE
        elif angle == 90:
            self.sprite = Player.MOVE_DOWN_SPRITE
        elif -90 < angle < 90:
            self.sprite = Player.MOVE_RIGHT_SPRITE
        else:
            self.sprite = Player.MOVE_LEFT_SPRITE

    # Interact with nearest entity (pickup or delivery)
    def interact_nearest(self, entities):
        threshold_interact_distance = 100
        nearest_entity, nearest_distance = get_nearest_entity(self, entities)

        # Pick up food
        if type(nearest_entity) is Food:
            if nearest_distance <= threshold_interact_distance:
                self.food_retrieved = nearest_entity.name

        # Deliver food
        elif type(nearest_entity) is Customer and self.food_retrieved:
            nearest_entity.interact(self.food_retrieved)
            self.food_retrieved = None

    # Draw player and floating food (if any)
    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.hitbox.topleft)

        if self.food_retrieved is not None:
            food_pos = Vec2d(self.hitbox.topleft) + (-25, -25)
            screen.blit(FOODS[self.food_retrieved], food_pos)
