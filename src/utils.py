# src/utils.py
import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen, mouse_x, mouse_y):
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))

        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(button_surface, color, pygame.Rect(0, 0, self.width, self.height))
        screen.blit(button_surface, (self.x, self.y))

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_hover(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

