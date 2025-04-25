##############################################################
#    CompClub Autumn Introduction to PyGame Workshop! :)     #
#        This program was written by: <Your-Name-Here>       #
#                       On: <Date-Here>                      #
##############################################################

import sys
import random
import pygame
from src.entities.food import FOODS, num_food
from src.constants import *
from pygame.locals import *
from src.entities.player import Player
from src.entities.entity import *
from src.entities.customer import *
from src.entities.player import *
from src.entities.effects.effect_manager import EffectManager
from src.util.vec2d import *
from src.scenes.scenes import handle_scenes
from src.entities.respawn_customer import respawn_customer
from src.entities.rubbish_bin import RubbishBin


# #############################################################################
# ########################## Initialise pygame ################################
# #############################################################################
pygame.init()

# [DRAWING THE WINDOW] ########################################################
# Create the screen
screen = pygame.display.set_mode(
    (
        TILE_SIZE * GRID_SIZE_X,
        TILE_SIZE * GRID_SIZE_Y,
    )
)

# Title and Icon
pygame.display.set_caption("Let him cook!!")
pygame.display.set_icon(pygame.image.load("./sprites/game_icon.png"))

# Scene transition map
scene_map = {
    "MENU": {"GAME": "GAME"},
    "GAME": {"SCORE": "SCORE"},
    "SCORE": {"GAME": "GAME", "MENU": "MENU"},
}

# Load background
background_image = pygame.image.load("spec/images/map_background.jpeg").convert()
background_image = pygame.transform.scale(
    background_image, (screen.get_width(), screen.get_height())
)

# [PLACING OUR OBJECTS] #######################################################
# Every object we're storing on the map, such as the:
# -> Player
# -> Customers
# -> Food
entities = []

# Placing our player
player = Player(Vec2d(CENTER_X - 100, CENTER_Y - 100), "./sprites/player/poco_down.png")
entities.append(player)

# Adding foods
foods = list(FOODS.keys())
fruit_pos = [FRUIT1_POS, FRUIT2_POS, FRUIT3_POS, FRUIT4_POS, FRUIT5_POS, FRUIT6_POS]
for i in range(0, num_food()):
    entities.append(Food(fruit_pos[i], FOODS[foods[i]], foods[i]))

# Return a random food
# This function picks a random food from the list of foods.
def getRandomFood():
    # SOLUTION START --
    return foods[random.randint(0, num_food() - 1)]
    # -- SOLUTION END

# Adding customers
customer_pos = [CUST1_POS, CUST2_POS, CUST3_POS, CUST4_POS, CUST5_POS]
customers = []
for position in customer_pos:
    customer = Customer(getRandomFood(), player, Vec2d(position))
    customers.append(customer)
    entities.append(customer)

# Adding effects
effects = EffectManager()

# The initial state of our game
state = {
    CLOCK: pygame.time.Clock(),
    RUNNING: True,
    TIME_LEFT: 60,
    CURRENT_SCENE: "MENU"
}
# Adding rubbish bin
rubbish_bin = RubbishBin(Vec2d(700, 150))
entities.append(rubbish_bin)
# #############################################################################
# ################################ Game Loop ##################################
# #############################################################################

# Everything is rendered from the top to the bottom, so we start off by drawing
# the window, then background, our entities, then our user interface (ie the score/timer text)

try:
    while state[RUNNING]:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state[RUNNING] = False
                break

            # Handle effect-related events
            effects.handle_events(event, entities)

        if not state[RUNNING]:
            break

        # Update game state
        for entity in entities:
            entity.update(entities, state)

        respawn_customer(customers, customer_pos, entities, player)
        effects.update(entities, state)

        # Render
        handle_scenes(screen, player, entities, background_image, state)
        pygame.display.update()

        # Cap the frame rate
        state[CLOCK].tick(60)
except Exception as ex:
    print(ex)
finally:
    pygame.quit()
    sys.exit()
