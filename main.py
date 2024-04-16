import pygame
from src.constants import *
from pygame.locals import *
from src.entities.player import Player
from src.scenes.menu import menu
from src.scenes.credit import credit
from src.scenes.score import score
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

# Scene transition map
scene_map = {
    "MENU": {"GAME": "GAME", "CREDIT": "CREDIT"},
    "GAME": {"SCORE": "SCORE"},
    "CREDIT": {"MENU": "MENU"},
    "SCORE": {"GAME": "GAME", "MENU": "MENU"}
}

# Load background
background_image = pygame.image.load('spec/images/map_background.jpeg').convert()
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

entities = []

# Initialise game state
player = Player(Vec2d(CENTER_X - 100, CENTER_Y - 100), "./sprites/temp/temp_sprite.png")
entities.append(player)

# Seats
seats = []
seat_positions = [position...,]
for position in seat_positions:
    seats.append(Seat(position))

#customer = Customer(Order.FOOD1, Vec2d(100, 100))
#entities.append(customer)
clock = pygame.time.Clock()
running = True
count = 10
current_score = 0
current_scene = "MENU"

# HUD Stuff
font = pygame.font.SysFont('Palatino', 30)
title_pos = (FLOOR_MIN_X, FLOOR_MIN_Y)


# Game Loop #####################################
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for entity in entities:
        entity.update(entities)

    if current_scene == "MENU":
        result = menu(screen)
    elif current_scene == "CREDIT":
        result = credit(screen)
    elif current_scene == "SCORE":
        result = score(screen, current_score)
    elif current_scene == "GAME":
        if count < 0:
            result = "SCORE"
            count = 10
            current_score = 0
        
        screen.blit(background_image, (0, 0))
        clock.tick(60)

        count -= 1/60
        for entity in entities:
            entity.draw(screen)

        # Handle ending the game
        time_text = font.render(f'Time: {int(count)} sec', True, 0xFFFF)
        score_text = font.render(f'Score: {current_score}', True, 0xFFFF)
        curr_c_text = font.render(f'Currently carrying: ', True, 0xFFFF)
        
        
        screen.blit(time_text, title_pos)
        screen.blit(score_text, (FLOOR_MIN_X, FLOOR_MIN_Y + 20))
        screen.blit(curr_c_text, (FLOOR_MIN_X, FLOOR_MIN_Y + 40))
        pygame.draw.rect(screen, 0xFFFF, pygame.Rect(FLOOR_MIN_X + 200, FLOOR_MIN_Y + 40, 30, 30))
        


    current_scene = scene_map[current_scene].get(result, current_scene)
    pygame.display.update()
