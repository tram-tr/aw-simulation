# src/game.py

import pygame
import os
from src.settings import Settings
from src.sprites import Player, Country

class Game:
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Autonomous Weapons Simulation")
        icon_path = os.path.join("assets", "images", "icon.png")
        self.icon = pygame.image.load(icon_path)
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.countries = [Country(strategy) for strategy in self.settings.strategies]
        font_path = os.path.join("assets", "fonts", "Minecraft.ttf")
        self.font = pygame.font.Font(font_path, 20)
        self.intro_text = [
            "Welcome to our simulation project exploring", 
            "the impact of autonomous weapons on international relations.",
            "Using game theory and the classic Prisoner's Dilemma,",
            "we'll examine potential the use of autonomous weapons",
            "in a conflict scenario, gaining insights into", 
            "their potential impact and ethical implications.", 
            "",
            "Join us on this exciting journey into", 
            "the world of autonomous weapons and international relations!"
        ]

        self.running = True
        self.current_line = 0
        self.current_char = 0
        self.char_interval = 35
        self.elapsed_time = 0

    def display_intro_text(self):
        y = 100
        for i, line in enumerate(self.intro_text[:self.current_line]):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 30

        # typing effect for the current line
        if self.current_line < len(self.intro_text):
            current_text = self.intro_text[self.current_line][:self.current_char]
            text_surface = self.font.render(current_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)

    def run(self):
        # game loop
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

    def _draw(self):
        self.screen.fill((255, 255, 255))
        self.display_intro_text()
        pygame.display.update()

        self.elapsed_time += self.clock.get_time()
        if self.elapsed_time > self.char_interval:
            self.current_char += 1
            self.elapsed_time = 0
            if self.current_line < len(self.intro_text) and self.current_char > len(self.intro_text[self.current_line]):
                self.current_line += 1
                self.current_char = 0

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        # Update game state based on game logic (e.g., updating scores, checking for game over)
        pass
