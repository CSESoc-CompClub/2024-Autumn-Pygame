##############################################################
#    CompClub Autumn Introduction to PyGame Workshop! :)     #
#        This program was written by: <Your-Name-Here>       #
#                       On: <Date-Here>                      #
##############################################################

import random
import pygame
from src.entities.ingredient import INGREDIENTS
from src.constants import *
from pygame.locals import *
from src.entities.player import Player
from src.scenes.menu import menu
from src.scenes.credit import credit
from src.scenes.score import score
from src.entities.entity import *
from src.entities.customer import *
from src.entities.player import *
from src.util.vec2d import *
from src.entities.ingredient import num_food


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
pygame.display.set_icon(pygame.image.load("./sprites/temp/temp_icon.png"))

# Scene transition map
scene_map = {
    "MENU": {"GAME": "GAME", "CREDIT": "CREDIT"},
    "GAME": {"SCORE": "SCORE"},
    "CREDIT": {"MENU": "MENU"},
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
player = Player(Vec2d(PLAYER_START_X, PLAYER_START_Y), "./sprites/temp/temp_sprite.png")
entities.append(player)

# Adding Ingredients
ingredients = ["watermelon", "sushi", "peach", "banana", "grapes", "strawberry"]
entities.append(Ingredient(FRUIT1_POS, INGREDIENTS["strawberry"], "strawberry"))
entities.append(Ingredient(FRUIT2_POS, INGREDIENTS["sushi"], "sushi"))
entities.append(Ingredient(FRUIT3_POS, INGREDIENTS["peach"], "peach"))
entities.append(Ingredient(FRUIT4_POS, INGREDIENTS["banana"], "banana"))
entities.append(Ingredient(FRUIT5_POS, INGREDIENTS["grapes"], "grapes"))
entities.append(Ingredient(FRUIT6_POS, INGREDIENTS["watermelon"], "watermelon"))

# Return a random ingredient
def getRandomIngredient():
    return random.choice(ingredients)

# Adding customers
customer_1 = Customer(getRandomIngredient(), player, Vec2d(CUST1_POS))
customer_2 = Customer(getRandomIngredient(), player, Vec2d(CUST2_POS))
customer_3 = Customer(getRandomIngredient(), player, Vec2d(CUST3_POS))
customer_4 = Customer(getRandomIngredient(), player, Vec2d(CUST4_POS))
customer_5 = Customer(getRandomIngredient(), player, Vec2d(CUST5_POS))
entities = entities + [customer_1, customer_2, customer_3, customer_4, customer_5]

# Deciding if a customer should be spawned this tick
def shouldSpawnCustomer():
    randint = random.randint(
        SPAWN_CUSTOMER_RANGE_START,
        SPAWN_CUSTOMER_RANGE_STOP
    )

    return randint > SPAWN_CUSTOMER_REQUIRED_LOWERBOUND

# The initial state of our game
clock = pygame.time.Clock()
running = True
time_left = INITIAL_TIME_LEFT
current_scene = "MENU"

# Font for our user interface
font = pygame.font.SysFont('Palatino', FONT_SIZE)

# #############################################################################
# ################################ Game Loop ##################################
# #############################################################################

# Everything is rendered from the top to the bottom, so we start off by drawing
# the window, then background, our entities, then our user interface (ie the score/timer text)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for entity in entities:
        entity.update(entities)

    # Don't do this
    if current_scene == "MENU":
        result = menu(screen)
    elif current_scene == "CREDIT":
        result = credit(screen)
    elif current_scene == "SCORE":
        result = score(screen, player.score)
        player.score = INITIAL_SCORE
    elif current_scene == "GAME":
        # Handle time out
        if time_left < 0:
            result = "SCORE"
            time_left = INITIAL_TIME_LEFT


        screen.blit(background_image, BACKGROUND_COORDS)
        clock.tick(FPS)

        time_left -= 1/FPS
        for entity in entities:
            entity.draw(screen)

        # Display our user interface
        time_text = font.render(f'Time: {int(time_left)} sec', True, WHITE)
        score_text = font.render(f'Score: {player.score}', True, WHITE)

        screen.blit(time_text, (FLOOR_MIN_X, FLOOR_MIN_Y))
        screen.blit(score_text, (FLOOR_MIN_X, FLOOR_MIN_Y + SCORE_TEXT_Y_OFFSET))

    # Also don't do this
    if shouldSpawnCustomer():
        if customer_1 not in entities:
            customer_1 = Customer(getRandomIngredient(), player, Vec2d(CUST1_POS))
            entities.append(customer_1)
        elif customer_2 not in entities:
            customer_2 = Customer(getRandomIngredient(), player, Vec2d(CUST2_POS))
            entities.append(customer_2)
        elif customer_3 not in entities:
            customer_3 = Customer(getRandomIngredient(), player, Vec2d(CUST3_POS))
            entities.append(customer_3)
        elif customer_4 not in entities:
            customer_4 = Customer(getRandomIngredient(), player, Vec2d(CUST4_POS))
            entities.append(customer_4)
        elif customer_5 not in entities:
            customer_5 = Customer(getRandomIngredient(), player, Vec2d(CUST5_POS))
            entities.append(customer_5)

    current_scene = scene_map[current_scene].get(result, current_scene)
    pygame.display.update()

