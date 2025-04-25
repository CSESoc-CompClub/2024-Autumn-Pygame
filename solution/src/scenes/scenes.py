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

def handle_scenes(screen, player, entities, background_image, state, file):
    if state[CURRENT_SCENE] == "MENU":
        result = menu(screen)
    elif state[CURRENT_SCENE] == "SCORE":
        file.write(f"{player.score}")
        result = score(screen, player.score)
        player.score = 0
    elif state[CURRENT_SCENE] == "GAME":
        result = "GAME"

        # Handle time out
        if state[TIME_LEFT] < 0:
            result = "SCORE"
            state[TIME_LEFT] = 60

        screen.blit(background_image, (0, 0))
        state[CLOCK].tick(60)

        state[TIME_LEFT] -= 1/60
        for entity in entities:
            entity.draw(screen)
        player.draw(screen)

        # Display our user interface
        time_text = font.render(f'Time: {int(state[TIME_LEFT])} sec', True, WHITE)
        score_text = font.render(f'Score: {player.score}', True, WHITE)

        screen.blit(time_text, (FLOOR_MIN_X, FLOOR_MIN_Y))
        screen.blit(score_text, (FLOOR_MIN_X, FLOOR_MIN_Y + 40))

    state[CURRENT_SCENE] = result
