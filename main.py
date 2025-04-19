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
player = Player(Vec2d(CENTER_X - 100, CENTER_Y - 100), "./sprites/temp/temp_sprite.png")
entities.append(player)

# Adding Ingredients
ingredients = ["watermelon", "sushi", "peach", "banana", "grapes", "strawberry"]
entities.append(Ingredient(FRUIT1_POS, INGREDIENTS["strawberry"], "strawberry"))
entities.append(Ingredient(FRUIT2_POS, INGREDIENTS["sushi"], "sushi"))
entities.append(Ingredient(FRUIT3_POS, INGREDIENTS["peach"], "peach"))
entities.append(Ingredient(FRUIT4_POS, INGREDIENTS["banana"], "banana"))
entities.append(Ingredient(FRUIT5_POS, INGREDIENTS["grapes"], "grapes"))
entities.append(Ingredient(FRUIT6_POS, INGREDIENTS["watermelon"], "watermelon"))


##############################################################################
# TODO: Return a random ingredient from ingredient list ######################
##############################################################################
def getRandomIngredient():
    """Return a random ingredient from ingredient list
    Returns:
        _type_: string representing the ingredient
    """
    # TODO: Write your code here!
    return ingredients[0]

# Adding customers
customer_1 = Customer(getRandomIngredient(), player, Vec2d(CUST1_POS))
customer_2 = Customer(getRandomIngredient(), player, Vec2d(CUST2_POS))
customer_3 = Customer(getRandomIngredient(), player, Vec2d(CUST3_POS))
customer_4 = Customer(getRandomIngredient(), player, Vec2d(CUST4_POS))
customer_5 = Customer(getRandomIngredient(), player, Vec2d(CUST5_POS))
customers = [customer_1, customer_2, customer_3, customer_4, customer_5]
entities = entities + random.sample(customers, 3)

# Deciding if a customer should be spawned this tick
def shouldSpawnCustomer():
    return random.randint(0, 1000) > 997

# The initial state of our game
clock = pygame.time.Clock()
running = True
time_left = 60
current_scene = "MENU"

# Font for our user interface
font = pygame.font.SysFont('Palatino', 30)

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
        player.score = 0
    elif current_scene == "GAME":
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

    # Also don't do this
    if random.randint(0, 1000) > 997:
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

