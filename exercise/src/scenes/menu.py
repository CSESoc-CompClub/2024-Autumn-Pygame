import pygame
import src.constants as constants
from src.scenes.button import Button

def menu(screen):
    # Background
    background_image = pygame.image.load('spec/images/menu_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Buttons
    play_button = Button("Play", constants.CENTER_X - 270, 525, 210, 45)
    quit_button = Button("Quit", constants.CENTER_X + 110, 525, 210, 45)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.is_clicked(mouse_pos):
                    return "GAME"
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()

        screen.blit(background_image, (0, 0))

        play_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
