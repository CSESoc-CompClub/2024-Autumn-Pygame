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
from src.scenes.scenes import handle_scenes



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
ingredients = ["strawberry", "sushi", "peach", "banana", "grapes", "watermelon"]
fruit_pos = [FRUIT1_POS, FRUIT2_POS, FRUIT3_POS, FRUIT4_POS, FRUIT5_POS, FRUIT6_POS]
for i in range(0, num_food()):
    entities.append(Ingredient(fruit_pos[i], INGREDIENTS[ingredients[i]], ingredients[i]))

# Return a random ingredient
def getRandomIngredient():
    return ingredients[random.randint(0, 5)]

# Adding customers
customer_pos = [CUST1_POS, CUST2_POS, CUST3_POS, CUST4_POS, CUST5_POS]
customers = []
for position in customer_pos:
    customer = Customer(getRandomIngredient(), player, Vec2d(position))
    customers.append(customer)
    entities += [customer]

# Deciding if a customer should be spawned this tick
def shouldSpawnCustomer():
    return random.randint(0, 1000) > 997

# The initial state of our game
clock = pygame.time.Clock()
running = True
time_left = 60
current_scene = "MENU"


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

    # Spawning more customers if they left
    if shouldSpawnCustomer():
        for i, customer in enumerate(customers):
            if customer not in entities:
                customer = Customer(getRandomIngredient(), player, Vec2d(customer_pos[i]))
                customers[i] = customer
                entities.append(customer)
                break

    # Handle scene logic
    current_scene, time_left = handle_scenes(screen, player, entities, 
                                             background_image, clock, time_left, 
                                             current_scene)
    pygame.display.update()

