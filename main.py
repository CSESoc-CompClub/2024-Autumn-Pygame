import pygame
from pygame.locals import *
from src.entities.player import Player
from src.scenes.menu import menu
from src.scenes.map import map
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
    "MENU": {"MAP": "MAP", "CREDIT": "CREDIT"},
    "MAP": {"MENU": "MENU"},
    "CREDIT": {"MENU": "MENU"},
    "SCORE": {"MAP": "MAP", "MENU": "MENU"}
}

# Initialise game state
player = Player()
clock = pygame.time.Clock()
running = True;
current_score = 0
current_scene = "MENU"

# Game Loop #####################################
while running:
    if current_scene == "MENU":
        result = menu(screen)
    elif current_scene == "MAP":
        result = map(screen)
    elif current_scene == "CREDIT":
        result = credit(screen)
    elif current_scene == "SCORE":
        result = score(screen, current_score)

    current_scene = scene_map[current_scene].get(result, current_scene)

    if current_scene == "MAP":
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player
        keys = pygame.key.get_pressed()
        player.set_position(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])
        screen.blit(player.sprite, (player.x_pos, player.y_pos))
    
        pygame.display.update()