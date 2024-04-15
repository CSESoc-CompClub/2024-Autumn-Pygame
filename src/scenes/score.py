import pygame
import src.constants as constants
from src.scenes.button import Button

def score(screen, current_score):
    # Background
    background_image = pygame.image.load('spec/images/score_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Game Over text
    font = pygame.font.SysFont('Palatino', 100)
    game_over_text = font.render('Game Over', True, constants.RED_BLACK)
    game_over_pos = (constants.CENTER_X - 420, 70)

    # Score text
    font = pygame.font.SysFont('Palatino', 50)
    score_text = font.render(f'Score: {current_score}', True, constants.RED_BLACK)
    score_pos = (constants.CENTER_X  - 260, 180)

    # Buttons
    menu_button = Button("Menu", constants.CENTER_X  - 50, 525, 140, 40)
    play_button = Button("Play Again!", constants.CENTER_X  - 80, 425, 200, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if menu_button.is_clicked(mouse_pos):
                    return "MENU"
                if play_button.is_clicked(mouse_pos):
                    return "GAME"

        screen.blit(background_image, (0, 0))

        screen.blit(game_over_text, game_over_pos)
        screen.blit(score_text, score_pos)

        menu_button.draw(screen)
        play_button.draw(screen)

        pygame.display.flip()