# src/sprites.py
import pygame
import random

class Player:
    def __init__(self):
        # Initialize player attributes, such as score and move history
        pass

class Country:
    def __init__(self, strategy):
        self.strategy = strategy
        # Initialize country attributes, such as resources and strategy-specific behavior
        pass

class Resources:
    def __init__(self, lives, resources, pos, font):
        self.lives = lives
        self.resources = resources
        self.pos = pos
        self.font = font
    
    def draw(self, screen):
        text_surface = self.font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=self.pos)
        screen.blit(text_surface, text_rect)

        text_surface = self.font.render(f"Resources: {self.resources}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(self.pos[0], self.pos[1]+30))
        screen.blit(text_surface, text_rect)

# Given the game so far and the strategy in use, make the choice
# 1 - use ; 0 - not use
def get_computer_choice(strategy, past_rounds):
    if(strategy == 1): # Developed Country
        # Strategy: Cautious - choose to either cooperate or defect on what the opponent chose to do in the last round
        if(len(past_rounds) > 0):
            return past_rounds[-1][0]
        else:
            return random.randint(0, 100) % 2

    elif(strategy == 2): # Developing Country
        # Strategy: Unpredictable - alternate between cooperate and defect based on their perceived needs and resources
        return len(past_rounds)%2

    elif(strategy == 3): # Resource-rich Country
        # Strategy: Defensive - choose to cooperate most of the time but starting to defect if the other opponent chooses to defect
        for r in past_rounds:
            if r[0]:
                return 1
        return 0

    elif(strategy == 4): # Military-focused Country
        # Strategy: Aggressive - choose to defect most of the time
        return 1

    elif(strategy == 5): # Peace-focused Country
        # Strategy: Cooperative - choose to cooperate most of the time
        return 0
    
    return -1
