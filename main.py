import pygame
from pygame.locals import *
from src.entities.player import Player
from src.scenes.menu import menu
from src.scenes.credit import credit
from src.scenes.score import score
import src.constants as constants

# Initialise pygame ###############################
pygame.init()

# Create the screen
screen = pygame.display.set_mode((
    constants.TILE_SIZE * constants.GRID_SIZE_X, 
    constants.TILE_SIZE * constants.GRID_SIZE_Y))

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

# Initialise game state
player = Player()
clock = pygame.time.Clock()
running = True
current_score = 0
current_scene = "MENU"

# Game Loop #####################################
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_scene == "MENU":
        result = menu(screen)
    elif current_scene == "CREDIT":
        result = credit(screen)
    elif current_scene == "SCORE":
        result = score(screen, current_score)
    elif current_scene == "GAME":
        screen.blit(background_image, (0, 0))

        # Adding player
        keys = pygame.key.get_pressed()
        player.set_position(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])
        screen.blit(player.sprite, (player.x_pos, player.y_pos))

        # Handle ending the game
        # result = "SCORE"

    current_scene = scene_map[current_scene].get(result, current_scene)
    pygame.display.flip()
