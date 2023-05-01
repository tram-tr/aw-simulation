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
    if(strategy == 0): # Developed Country
        # Strategy: Cautious - choose to either cooperate or defect on what the opponent chose to do in the last round
        if(len(past_rounds) > 0):
            return past_rounds[-1][0]
        else:
            return random.randint(0, 100) % 2

    elif(strategy == 1): # Developing Country
        # Strategy: Unpredictable - alternate between cooperate and defect based on their perceived needs and resources
        return len(past_rounds)%2

    elif(strategy == 2): # Resource-rich Country
        # Strategy: Defensive - choose to cooperate most of the time but starting to defect if the other opponent chooses to defect
        for r in past_rounds:
            if r[0]:
                return 1
        return 0

    elif(strategy == 3): # Military-focused Country
        # Strategy: Aggressive - choose to defect most of the time
        return 1

    elif(strategy == 4): # Peace-focused Country
        # Strategy: Cooperative - choose to cooperate most of the time
        return 0
    
    return -1



sprite_size = 128

# Load sprites for the different characters
developed_sprite = pygame.image.load("assets/images/DevelopedCountry.png")
developed_sprite = pygame.transform.scale(developed_sprite, (sprite_size, sprite_size))

developing_sprite = pygame.image.load("assets/images/DevelopingCountry.png")
developing_sprite = pygame.transform.scale(developing_sprite, (sprite_size, sprite_size))

military_sprite = pygame.image.load("assets/images/MilitaryFocused.png")
military_sprite = pygame.transform.scale(military_sprite, (sprite_size, sprite_size))

peace_sprite = pygame.image.load("assets/images/PeaceFocused.png")
peace_sprite = pygame.transform.scale(peace_sprite, (sprite_size, sprite_size))

resource_sprite = pygame.image.load("assets/images/ResourceRich.png")
resource_sprite = pygame.transform.scale(resource_sprite, (sprite_size, sprite_size))

opponents = [
    {
        "id": 0,
        "type": "Developed Country",
        "strategy": "Cautious",
        "sprite": developed_sprite,
        "name": "Joe"
    },
    {
        "id": 1,
        "type": "Developing Country",
        "strategy": "Unpredictable",
        "sprite": developing_sprite,
        "name": "Kanye"
    },
    {
        "id": 2,
        "type": "Resource-Rich Country",
        "strategy": "Defensive",
        "sprite": resource_sprite,
        "name": "Sam"
    },
    {
        "id": 3,
        "type": "Military-Focused Country",
        "strategy": "Aggressive",
        "sprite": military_sprite,
        "name": "Lizzy"
    },
    {
        "id": 4,
        "type": "Peace-Focused Country",
        "strategy": "Cooperative",
        "sprite": peace_sprite,
        "name": "Dierre"
    },
]

player_sprite = pygame.image.load("assets/images/Player.png")
player_sprite = pygame.transform.scale(player_sprite, (sprite_size, sprite_size))