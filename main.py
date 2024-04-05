import pygame
from src.constants import *
from pygame.locals import *
from src.entities.entity import *
from src.entities.obstacle import *
from src.entities.customer import *
from src.entities.player import *
from src.util.vec2d import *

# Initialise pygame ###############################
pygame.init()

# Create the screen
screen = pygame.display.set_mode(
    (
        TILE_SIZE * GRID_SIZE_X,
        TILE_SIZE * GRID_SIZE_Y,
    )
)

# Title and Icon
pygame.display.set_caption("Let him cook!!")
pygame.display.set_icon(pygame.image.load("./sprites/temp/temp_icon.png"))

entities = []

# Initialise game state
player = Player(Vec2d(500, 500), "./sprites/temp/temp_sprite.png")
entities.append(player)
customer = Customer(Order.FOOD1, Vec2d(100, 100))
customer.move_to_table(TableSpot(Vec2d(200, 200), True), entities)
entities.append(customer)
clock = pygame.time.Clock()
running = True
count = 0

# Game Loop #####################################
while running:
    clock.tick(60)
    count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if count % 100 == 0:
        customer.move_to_table(TableSpot(Vec2d(player.hitbox.x, player.hitbox.y), True), entities)

    for entity in entities:
        entity.update(entities)

    # Draw graphics
    # 1) fill bg
    screen.fill((255, 255, 255))

    # 2) fill tiles (map)

    # 3) draw player
    screen.blit(player.sprite, player.hitbox.topleft)

    # 4) draw customer
    screen.blit(customer.sprite, customer.hitbox.topleft)

    # 4) draw hud(?)

    pygame.display.update()
