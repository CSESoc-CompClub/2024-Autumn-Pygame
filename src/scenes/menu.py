import pygame
import src.constants as constants
from src.scenes.button import Button

def menu(screen):
    # Background
    background_image = pygame.image.load('spec/images/menu_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Buttons
    play_button = Button(
        "Play",
        constants.CENTER_X + constants.MENU_PLAY_BUTTON_POS_X_OFFSET,
        constants.DEFAULT_BUTTON_POS_Y,
        constants.DEFAULT_MENU_BUTTON_POS_W,
        constants.DEFAULT_MENU_BUTTON_POS_H
    )

    credit_button = Button(
        "Credits",
        constants.CENTER_X + constants.MENU_CREDIT_BUTTON_POS_X_OFFSET,
        constants.DEFAULT_BUTTON_POS_Y,
        constants.DEFAULT_MENU_BUTTON_POS_W,
        constants.DEFAULT_MENU_BUTTON_POS_H
    )

    quit_button = Button(
        "Quit",
        constants.CENTER_X + constants.MENU_QUIT_BUTTON_POS_X_OFFSET,
        constants.DEFAULT_BUTTON_POS_Y,
        constants.DEFAULT_MENU_BUTTON_POS_W,
        constants.DEFAULT_MENU_BUTTON_POS_H
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.is_clicked(mouse_pos):
                    return "GAME"
                elif credit_button.is_clicked(mouse_pos):
                    return "CREDIT"
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()

        screen.blit(background_image, constants.BACKGROUND_POS)

        play_button.draw(screen)
        credit_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
