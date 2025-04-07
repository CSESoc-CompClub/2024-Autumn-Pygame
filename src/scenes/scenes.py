# Don't do this
import pygame
from src.constants import *
from pygame.locals import *
from src.scenes.menu import menu
from src.scenes.score import score
from src.entities.entity import *
from src.entities.customer import *
from src.entities.player import *
from src.util.vec2d import *

# Font for our user interface
pygame.init()
font = pygame.font.SysFont('Palatino', 30)

def handle_scenes(screen, player, entities, background_image, clock, time_left, current_scene):
    if current_scene == "MENU":
        result = menu(screen)
    elif current_scene == "SCORE":
        result = score(screen, player.score)
        player.score = 0
    elif current_scene == "GAME":
        result = "GAME"

        # Handle time out
        if time_left < 0:
            result = "SCORE"
            time_left = 60

        screen.blit(background_image, (0, 0))
        clock.tick(60)

        time_left -= 1/60
        for entity in entities:
            entity.draw(screen)

        # Display our user interface
        time_text = font.render(f'Time: {int(time_left)} sec', True, WHITE)
        score_text = font.render(f'Score: {player.score}', True, WHITE)

        screen.blit(time_text, (FLOOR_MIN_X, FLOOR_MIN_Y))
        screen.blit(score_text, (FLOOR_MIN_X, FLOOR_MIN_Y + 40))

    return result, time_left
