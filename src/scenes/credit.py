import pygame
import src.constants as constants
from src.scenes.button import Button

def credit(screen):
    # Background
    background_image = pygame.image.load('spec/images/credits_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Title text
    font = pygame.font.SysFont('Palatino', 90)
    title_text = font.render('Credits', True, constants.BURGUNDY)
    title_pos = (constants.CENTER_X - 400, 90)

    # Button
    Menu_button = Button("Menu", constants.CENTER_X - 50, 525, 140, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Menu_button.is_clicked(mouse_pos):
                    return "MENU"

        screen.blit(background_image, (0, 0))

        screen.blit(title_text, title_pos)

        Menu_button.draw(screen)

        pygame.display.flip()