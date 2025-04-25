import pygame
import src.constants as constants
from src.scenes.button import Button

def score(screen, current_score, leaderboard):
    # Background
    background_image = pygame.image.load('spec/images/score_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Game Over text
    font = pygame.font.SysFont('Palatino', 100)
    game_over_text = font.render('Game Over', True, constants.RED_BLACK)
    game_over_pos = (constants.CENTER_X - 420, 70)

    # Leaderboard text
    leaderboard_font = pygame.font.SysFont("Palatino", 30)
    score_font = pygame.font.SysFont("Palatino", 20)
    leaderboard.seek(0)
    leaderboard_text = leaderboard_font.render(f"Leaderboard: ", True, constants.RED_BLACK)
    scores = leaderboard.read().split('|')
    scores.pop()
    print(scores)

    prev_y = 50
    scores_text_and_pos = [
        (leaderboard_font.render(f"{position}: {score}", True, constants.RED_BLACK),
            (constants.MAX_X - 50, (prev_y := prev_y + 30))
         )
        for position, score in enumerate(sorted(scores)[::-1][:5])
    ]

    leaderboard_pos = (constants.MAX_X - 50, 50)

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

        screen.blit(leaderboard_text, leaderboard_pos)

        for score_text, pos in scores_text_and_pos:
            screen.blit(score_text,pos)

        pygame.display.flip()
