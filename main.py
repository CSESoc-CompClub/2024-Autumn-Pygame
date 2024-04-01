import pygame
from pygame.locals import *
from src.entities.player import Player
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

# Initialise game state
player = Player()
clock = pygame.time.Clock()
running = True;

# Game Loop #####################################
while running: 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement            
    keys = pygame.key.get_pressed()
    player.set_position(keys[K_d] - keys[K_a], keys[K_s] - keys[K_w])        
    
    # Draw graphics
    # 1) fill bg
    screen.fill((255, 255, 255))

    # 2) fill tiles (map)

    # 3) draw player
    screen.blit(player.sprite, (player.x_pos, player.y_pos))

    # 4) draw hud(?)
    
    pygame.display.update()