import pygame
import src.constants as constants
from src.scenes.button import Button

def credit(screen):
    # Background
    background_image = pygame.image.load('spec/images/credits_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Title text
    font = pygame.font.SysFont('Palatino', constants.CREDIT_FONT_SIZE)
    title_text = font.render('Credits', True, constants.BURGUNDY)
    title_pos = (
        constants.CENTER_X + constants.CREDIT_TITLE_POS_X_OFFSET,
        constants.CREDIT_TITLE_POS_Y
    )

    # Button
    Menu_button = Button(
        "Menu",
        constants.MENU_BUTTON_POS_X,
        constants.MENU_BUTTON_POS_Y,
        constants.MENU_BUTTON_POS_W,
        constants.MENU_BUTTON_POS_H
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Menu_button.is_clicked(mouse_pos):
                    return "MENU"

        screen.blit(background_image, constants.ORIGIN_POS)

        screen.blit(title_text, title_pos)

        Menu_button.draw(screen)

        pygame.display.flip()