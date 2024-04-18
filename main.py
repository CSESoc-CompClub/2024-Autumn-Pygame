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
    "SCORE": {"GAME": "GAME", "MENU": "MENU"},
}

# Load background
background_image = pygame.image.load("spec/images/map_background.jpeg").convert()
background_image = pygame.transform.scale(
    background_image, (screen.get_width(), screen.get_height())
)

entities = []

# Initialise game state
player = Player(Vec2d(CENTER_X - 100, CENTER_Y - 100), "./sprites/temp/temp_sprite.png")
entities.append(player)

# Adding Ingredients
ingredients = ["watermelon", "sushi", "peach", "banana", "grapes", "strawberry"]
entities.append(Ingredient(Vec2d(60, 0), INGREDIENTS["watermelon"], "watermelon"))
entities.append(Ingredient(Vec2d(190, 0), INGREDIENTS["sushi"], "sushi"))
entities.append(Ingredient(Vec2d(320, 0), INGREDIENTS["peach"], "peach"))
entities.append(Ingredient(Vec2d(450, 0), INGREDIENTS["banana"], "banana"))
entities.append(Ingredient(Vec2d(580, 0), INGREDIENTS["grapes"], "grapes"))
entities.append(Ingredient(Vec2d(720, 0), INGREDIENTS["strawberry"], "strawberry"))

# Return a random ingredient
def getRandomIngredient():
    return ingredients[random.randint(0, 5)]

# Adding customers
customer_1 = Customer(getRandomIngredient(), player, SEAT_1)
customer_2 = Customer(getRandomIngredient(), player, SEAT_2)
customer_3 = Customer(getRandomIngredient(), player, SEAT_3)
customer_4 = Customer(getRandomIngredient(), player, SEAT_4)
customer_5 = Customer(getRandomIngredient(), player, SEAT_5)

entities = entities + [customer_1, customer_2, customer_3, customer_4, customer_5]

# Setting up Game State
clock = pygame.time.Clock()
running = True
count = 20
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
        result = score(screen, player.score)
        player.score = 0
    elif current_scene == "GAME":
        # Handle time out
        if count < 0:
            result = "SCORE"
            count = 60

        screen.blit(background_image, (0, 0))
        clock.tick(60)

        count -= 1/60
        for entity in entities:
            entity.draw(screen)

        # HUD
        time_text = font.render(f'Time: {int(count)} sec', True, WHITE)
        score_text = font.render(f'Score: {player.score}', True, WHITE)

        screen.blit(time_text, title_pos)
        screen.blit(score_text, (FLOOR_MIN_X, FLOOR_MIN_Y + 40))

    if random.randint(0, 1000) > 997:
        if customer_1 not in entities:
            customer_1 = Customer(getRandomIngredient(), player, SEAT_1)
            entities.append(customer_1)
        elif customer_2 not in entities:
            customer_2 = Customer(getRandomIngredient(), player, SEAT_2)
            entities.append(customer_2)
        elif customer_3 not in entities:
            customer_3 = Customer(getRandomIngredient(), player, SEAT_3)
            entities.append(customer_3)
        elif customer_4 not in entities:
            customer_4 = Customer(getRandomIngredient(), player, SEAT_4)
            entities.append(customer_4)
        elif customer_5 not in entities:
            customer_5 = Customer(getRandomIngredient(), player, SEAT_5)
            entities.append(customer_5)

    current_scene = scene_map[current_scene].get(result, current_scene)
    pygame.display.update()
