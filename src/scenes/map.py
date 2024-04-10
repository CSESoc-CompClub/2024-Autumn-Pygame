import pygame

def map(screen):
    background_image = pygame.image.load('spec/images/map_background.jpeg').convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    screen.blit(background_image, (0, 0))

    pygame.display.flip()