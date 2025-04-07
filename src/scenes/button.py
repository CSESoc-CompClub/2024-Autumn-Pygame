import pygame
import src.constants as constants

class Button:
    def __init__(self, text, x, y, width, height):
        # Dimensions
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = constants.BUTTON_BORDER_RADIUS

        # Text
        self.text = text
        self.text_color = constants.YELLOW
        self.font = pygame.font.SysFont('Palatino', constants.BUTTON_FONT_SIZE)

        # Rectangle
        self.rect = pygame.Rect(x, y, width, height)
        self.color = constants.BURGUNDY

        # Border
        self.border_rect = pygame.Rect(
            x + constants.BUTTON_BORDER_X_OFFSET,
            y + constants.BUTTON_BORDER_Y_OFFSET,
            width + constants.BUTTON_BORDER_W_OFFSET,
            height + constants.BUTTON_BORDER_H_OFFSET
        )
        self.border_color = constants.BLACK

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, self.border_rect, border_radius = self.border_radius)
        pygame.draw.rect(screen, self.color, self.rect, border_radius = self.border_radius)

        # Draw text
        text = self.font.render(self.text, True, self.text_color)
        text_width, text_height = text.get_size()
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + (self.height - text_height) // 2
        screen.blit(text, (text_x, text_y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
