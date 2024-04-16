import pygame
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
entities.append(Ingredient(Vec2d(100, 20), "./sprites/temp/temp_item_tile.png", "cat"))
entities.append(Customer("cat", Vec2d(50, 520)))
entities.append(Customer("cat", Vec2d(200, 520)))
entities.append(Customer("cat", Vec2d(350, 520)))
entities.append(Customer("cat", Vec2d(500, 520)))
entities.append(Customer("cat", Vec2d(640, 520)))
clock = pygame.time.Clock()
running = True
count = 0
current_score = 0
current_scene = "MENU"

# Game Loop #####################################
while running:
    clock.tick(60)
    count += 1
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
        result = score(screen, current_score)
    elif current_scene == "GAME":
        screen.blit(background_image, (0, 0))

        for entity in entities:
            entity.draw(screen)

        # Handle ending the game
        # result = "SCORE"

    current_scene = scene_map[current_scene].get(result, current_scene)
    pygame.display.update()
