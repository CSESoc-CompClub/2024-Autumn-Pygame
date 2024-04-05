import pygame
from pygame.locals import *
from src.entities.entity import Entity
from src.entities.obstacle import TableSpot
from src.entities.customer import Customer, CustomerState, Order
from src.entities.player import Player
import src.constants as constants
from src.util.vec2d import Vec2d

# Initialise pygame ###############################
pygame.init()

# Create the screen
screen = pygame.display.set_mode(
    (
        constants.TILE_SIZE * constants.GRID_SIZE_X,
        constants.TILE_SIZE * constants.GRID_SIZE_Y,
    )
)

# Title and Icon
pygame.display.set_caption("Let him cook!!")
pygame.display.set_icon(pygame.image.load("./sprites/temp/temp_icon.png"))

# Initialise game state
player = Player(Vec2d(100, 100), "./sprites/temp/temp_sprite.png")
customer = Customer(Order.FOOD1, Vec2d(100, 100), CustomerState.LEAVING)
clock = pygame.time.Clock()
running = True
count = 0

# Game Loop #####################################
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    player.set_position(Vec2d(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w]))
    # Draw graphics
    # 1) fill bg
    screen.fill((255, 255, 255))

    # 2) fill tiles (map)

    # 3) draw player
    screen.blit(player.sprite, (player.pos.x, player.pos.y))

    # 4) draw customer
    screen.blit(customer.sprite, (customer.pos.x, customer.pos.y))

    if count == 0:
        customer.leave(
            [Entity(Vec2d(200, 100), Vec2d(300, 300), "./sprites/temp/temp_sprite.png")]
        )
        count = 1

    # 4) draw hud(?)

    pygame.display.update()
