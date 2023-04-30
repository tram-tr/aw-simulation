# src/game.py

import pygame
import os
from src.settings import Settings
from src.sprites import *
from src.utils import *

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
        "id": 1,
        "type": "Developed Country",
        "strategy": "Cautious",
        "sprite": developed_sprite,
    },
    {
        "id": 2,
        "type": "Developing Country",
        "strategy": "Unpredictable",
        "sprite": developing_sprite,
    },
    {
        "id": 3,
        "type": "Resource-Rich Country",
        "strategy": "Defensive",
        "sprite": resource_sprite,
    },
    {
        "id": 4,
        "type": "Military-Focused Country",
        "strategy": "Aggressive",
        "sprite": military_sprite,
    },
    {
        "id": 5,
        "type": "Peace-Focused Country",
        "strategy": "Cooperative",
        "sprite": peace_sprite,
    },
]

player_sprite = pygame.image.load("assets/images/DevelopedCountry.png")
player_sprite = pygame.transform.scale(player_sprite, (sprite_size, sprite_size))

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
        self.continue_button = Button(
            "Continue", self.settings.screen_width // 2 - 100, 400, 200, 50,
            (200, 200, 200), (225, 225, 225), self.font
        )
        self.current_scene = 0 
        self.num_scenes = 3
        self.running = True
        self.current_line = 0
        self.current_char = 0
        # self.char_interval = 30
        self.char_interval = 1
        self.elapsed_time = 0

        self.navleft = NavArrowLeft(50)
        self.navright = NavArrowRight(50)

        self.player_page_data = {
            'instruction_panel': {
                'panel': InfoPanel(["The year is 2050.", "", "You are the newly hired expert", "of autonomous weapons in", "the United States of America's", "military. Your task is to", "decide whether or not to use", "autonous weapons in conflict", "with each presented threat."], "okay...", self.font),
                # 'deactivated': False,
                'active': True,
            },
            'smoke_background': {
                'smoke': SmokeBackground(20, (0, 0, 0)),
                'active': True,
            },
            'in_game': False,
            'use_button': Button("Use Autonomous Weapons", 
                (self.settings.screen_width // 4) - 175, self.settings.screen_height*0.75, 
                350, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'dont_use_button': Button("Don't Use Autonomous Weapons", 
                (3*self.settings.screen_width // 4) - 175, self.settings.screen_height*0.75, 
                350, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'past_matches': [],
            'match_state': 'waiting',
            'current_match': 0,
            'rounds': [],
            'current_opponent': opponents[0],
            'player_selection': None,
            'computer_selection': None,
            'player_selection_alert': None,
            'computer_selection_alert': None,
            'player_attack_particles': None,
            'opponent_attack_particles': None,
            'player_resources': Resources(0, 0, (self.settings.screen_width/8, self.settings.screen_height/8), self.font),
            # country_resources is meant for 1v1 game
            'country_resources': Resources(0, 0, (self.settings.screen_width/8, self.settings.screen_height/8), self.font),
            'next_button': Button("Continue", 
                (self.settings.screen_width // 4), self.settings.screen_height*0.75, 
                self.settings.screen_width//2, 50,
                (200, 200, 200), (225, 225, 225), self.font),
        }


    def _display_intro_text(self):
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

        self.elapsed_time += self.clock.get_time()
        if self.elapsed_time > self.char_interval:
            self.current_char += 1
            self.elapsed_time = 0
            if self.current_line < len(self.intro_text) and self.current_char > len(self.intro_text[self.current_line]):
                self.current_line += 1
                self.current_char = 0

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
        self.scene_manager()
        pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle nav arrows
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if(self.navleft.is_hover(mouse_x, mouse_y)):
                    self.change_scene(self.current_scene - 1)
                elif(self.navright.is_hover(mouse_x, mouse_y)):
                    self.change_scene(self.current_scene + 1)

            if(self.current_scene == 0):
                self.handle_intro_events(event)
            elif(self.current_scene == 1):
                self.handle_player_events(event)
            elif(self.current_scene == 2):
                self.handle_explanation_events(event)
                
    def handle_intro_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.continue_button.is_hover(mouse_x, mouse_y):
                # self.intro_page = False
                self.change_scene(1)

                pygame.time.wait(300)
                # self.player_page = True

    def _update(self):
        # Update game state based on game logic (e.g., updating scores, checking for game over)
        pass

    def change_scene(self, scene):
        self.swipe_transition(scene)

    def swipe_transition(self, scene):
        transition_duration = 1000

        square_color = (0, 0, 0)

        ysize = 10
        ratio = round(self.settings.screen_width/self.settings.screen_height)
        xsize = round(ysize * ratio)

        xchecksize = round(self.settings.screen_width/xsize)
        ychecksize = round(self.settings.screen_height/ysize)

        square_positions = []
        square_offsets = []

        for i in range(xsize):
            for j in range(ysize):
                # find normalized centered position on screen using i and j
                # add 0.5 because the pos will be the center of the checkerboard squares
                ipos = (i+0.5)/xsize
                jpos = (j+0.5)/ysize

                # convert to screen position
                x = ipos * self.settings.screen_width
                y = jpos * self.settings.screen_height

                # determine if it is an on or off square
                # on = (i + j) % 2 == 0

                square_positions.append((x, y))
                square_offsets.append(((i+j)/((xsize-1) + (ysize-1)))/2)

        grow_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - grow_start_time < transition_duration // 2:
            self.scene_manager()

            progress = (pygame.time.get_ticks() - grow_start_time)/(transition_duration / 2)

            for i, pos in enumerate(square_positions):
                offset = square_offsets[i]

                amt = 0
                if(progress > offset + 0.5):
                    amt = 1.1
                elif(progress > offset):
                    amt = translate(progress, offset, offset+0.5, 0, 1.1)

                amtx = amt*xchecksize
                amty = amt*ychecksize
                rect = pygame.Rect(pos[0] - (amtx/2), pos[1] - (amty/2), amtx, amty)
                pygame.draw.rect(self.screen, square_color, rect)

            pygame.display.flip()

        self.current_scene = scene

        if(self.current_scene != -1):
            # Step 5: Shrink checkerboards back down
            shrink_start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - shrink_start_time < transition_duration // 2:
                self.screen.fill((255, 255, 255))
                self.scene_manager()
                
                progress = ((pygame.time.get_ticks() - shrink_start_time)/(transition_duration / 2))
                

                for i, pos in enumerate(square_positions):
                    offset = square_offsets[i]

                    amt = 1.1
                    if(progress > offset + 0.5):
                        amt = 0
                    elif(progress > offset):
                        amt = translate(progress, offset, offset+0.5, 1.1, 0)

                    amtx = amt*xchecksize
                    amty = amt*ychecksize
                    rect = pygame.Rect(pos[0] - (amtx/2), pos[1] - (amty/2), amtx, amty)
                    pygame.draw.rect(self.screen, square_color, rect)
                
                pygame.display.flip()

    def draw_nav_arrows(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Left arrow
        if(self.current_scene > 0):
            # Set up the left arrow coordinates
            self.navleft.draw(self.screen, mouse_x, mouse_y)
        
        # Right arrow
        if(self.current_scene < self.num_scenes-1):
            # Set up the right arrow coordinates
            self.navright.draw(self.screen, mouse_x, mouse_y)

    def scene_manager(self):
        if(self.current_scene == -1):
            self.running = False
        elif(self.current_scene == 0):
            self.intro_page()
        elif(self.current_scene == 1):
            self.player_page()
        elif(self.current_scene == 2):
            self.explanation_page()

        self.draw_nav_arrows()

    def intro_page(self):
        # self._display_intro_text()
        # if self.current_line >= len(self.intro_text):
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     self.continue_button.draw(self.screen, mouse_x, mouse_y)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.continue_button.draw(self.screen, mouse_x, mouse_y)

    def handle_player_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print(self.player_page_data['past_matches'])
            print(self.player_page_data['match_state'])

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.player_page_data['instruction_panel']['panel'].active and self.player_page_data['instruction_panel']['panel'].is_hover(mouse_x, mouse_y):
                self.player_page_data['instruction_panel']['panel'].active = False
                self.player_page_data['in_game'] = True
            elif len(self.player_page_data['past_matches']) == 5 and self.player_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.swipe_transition(self.current_scene + 1)
            elif self.player_page_data['in_game']:
                if(len(self.player_page_data['past_matches']) < 5):
                    if (self.player_page_data['match_state'] == 'waiting'):
                        if(self.player_page_data['use_button'].is_hover(mouse_x, mouse_y) or self.player_page_data['dont_use_button'].is_hover(mouse_x, mouse_y)):
                            self.player_page_data['match_state'] = 'selected'
                            self.player_page_data['selected_start_time'] = pygame.time.get_ticks()

                            # for every start of new match, initialize lives and resources to 0
                            if(len(self.player_page_data['rounds']) == 0):
                                self.player_page_data['player_resources'].lives = 0
                                self.player_page_data['player_resources'].resources = 0
                                self.player_page_data['country_resources'].lives = 0
                                self.player_page_data['country_resources'].resources = 0
                            
                            # Get both choices
                            player_choice = None
                            if self.player_page_data['use_button'].is_hover(mouse_x, mouse_y):
                                player_choice = 'use'
                            elif self.player_page_data['dont_use_button'].is_hover(mouse_x, mouse_y):
                                player_choice = 'dont_use'
                            self.player_page_data['player_selection'] = player_choice
                            computer_choice = get_computer_choice(self.player_page_data['current_opponent']['id'], self.player_page_data['rounds'])
                           
                            # convert get_computer_choice value into appropriate value
                            if computer_choice == 1:
                                computer_choice = 'use'
                            elif computer_choice == 0:
                                computer_choice = 'dont_use'
                            self.player_page_data['computer_selection'] = computer_choice

                            # Alert the player and computer choices
                            player_alert_string = "" 
                            if(player_choice == "use"): 
                                player_alert_string = "Uses AWs!"
                            else: 
                                player_alert_string = "Doesn't use AWs!"
                            computer_alert_string = ""
                            if(computer_choice == "use"):
                                computer_alert_string = "Uses AWs!"
                            else:
                                computer_alert_string = "Doesn't use AWs!"
                            self.player_page_data['player_selection_alert'] = AlertPanel(player_alert_string, self.player_position[0]-(sprite_size/4), self.player_position[1]-(sprite_size/4), sprite_size*2, (sprite_size/4), self.font)
                            self.player_page_data['computer_selection_alert'] = AlertPanel(computer_alert_string, self.opponent_position[0]-(sprite_size/4), self.opponent_position[1]-(sprite_size/4), sprite_size*2, (sprite_size/4), self.font)

                            # Use nash equilibrium and update player & country score
                            if player_choice == "use" and computer_choice == "use":
                                self.player_page_data['player_resources'].lives -= 10
                                self.player_page_data['player_resources'].resources -= 100
                                self.player_page_data['country_resources'].lives -= 10
                                self.player_page_data['country_resources'].resources -= 100
                            elif player_choice == "use" and computer_choice == "dont_use":
                                self.player_page_data['player_resources'].resources -= 100
                                self.player_page_data['country_resources'].lives -= 100
                            elif player_choice == "dont_use" and computer_choice == "use":
                                self.player_page_data['player_resources'].lives -= 100
                                self.player_page_data['country_resources'].resources -= 100
                            elif player_choice == "dont_use" and player_choice == "dont_use":
                                self.player_page_data['player_resources'].lives -= 1
                                self.player_page_data['player_resources'].resources -= 10
                                self.player_page_data['country_resources'].lives -= 1
                                self.player_page_data['country_resources'].resources -= 10

                            # If attacking with AW, create explode particles
                            if(player_choice == 'use'):
                                self.player_page_data['opponent_attack_particles'] = ExplodeEffect((self.opponent_position[0] + (sprite_size/2), self.opponent_position[1] + (sprite_size/2)), 10, (30, 30, 30))
                            if(computer_choice == 'use'):
                                self.player_page_data['player_attack_particles'] = ExplodeEffect((self.player_position[0] + (sprite_size/2), self.player_position[1] + (sprite_size/2)), 10, (30, 30, 30))

                            # Save the past round
                            self.player_page_data['rounds'].append((player_choice, computer_choice))

                            # if 5 rounds / 1 match has passed
                            if(len(self.player_page_data['rounds']) == 5):
                                # calculate payoff

                                # record 5 past rounds 
                                self.player_page_data['past_matches'].append(self.player_page_data['rounds'])
                                # reset current record of rounds 
                                self.player_page_data['rounds'] = []
                                # if still under five matches 
                                if(len(self.player_page_data['past_matches']) < 5):
                                    self.player_page_data['current_match'] += 1
                                    self.player_page_data['current_opponent'] = opponents[self.player_page_data['current_match']]
                                else: 
                                    self.player_page_data['state'] = 'completed'


    def player_page(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if(self.player_page_data['smoke_background']['active']):
            self.player_page_data['smoke_background']['smoke'].draw(self.screen)

        if(self.player_page_data['instruction_panel']['panel'].active):
            self.player_page_data['instruction_panel']['panel'].draw(self.screen, mouse_x, mouse_y)
        else:
            text_surface = self.font.render(f"Match {self.player_page_data['current_match'] + 1}", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 4))
            self.screen.blit(text_surface, text_rect)

            center_x = self.settings.screen_width//2
            y_spread = self.settings.screen_height/3
            y_step = y_spread/4
            y_start = (self.settings.screen_height//2)-(y_spread/2)

            for i in range(5):
                circ_pos = (center_x, y_start)
                try:
                    if(self.player_page_data['rounds'][i]):
                        pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 0)
                except:
                    pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 3)

                # if(len(self.player_page_data['rounds']) < i+1):
                #     pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 0)
                # else:
                # pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 3)
                y_start += y_step

                
            # Find player and opponent positions
            self.player_position = ((self.settings.screen_width/4) - (sprite_size/2), (self.settings.screen_height/2) - (sprite_size/2))
            self.opponent_position = ((3*self.settings.screen_width/4) - (sprite_size/2), (self.settings.screen_height/2) - (sprite_size/2))

            # Create shadow surface
            shadow_surface = pygame.Surface((3*sprite_size/4, sprite_size/4), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (50, 50, 50), shadow_surface.get_rect())

            # Draw the shadows
            shadow_y = self.player_position[1]+(7*sprite_size/8)
            self.screen.blit(shadow_surface, (self.player_position[0]+(sprite_size/8), shadow_y))
            self.screen.blit(shadow_surface, (self.opponent_position[0]+(sprite_size/8), shadow_y))
        
            self.screen.blit(military_sprite, self.player_position)
            self.screen.blit(self.player_page_data['current_opponent']['sprite'], self.opponent_position)

            self.player_page_data['player_resources'].draw(self.screen)

            if(self.player_page_data['match_state'] == 'waiting' and len(self.player_page_data['past_matches']) < 5):
                self.player_page_data['use_button'].draw(self.screen, mouse_x, mouse_y)
                self.player_page_data['dont_use_button'].draw(self.screen, mouse_x, mouse_y)
            
            # Display message of what each side chose
            if(self.player_page_data['player_selection_alert'] != None):
                if(self.player_page_data['player_selection_alert'].active):
                    self.player_page_data['player_selection_alert'].draw(self.screen)
                else:
                    if(self.player_page_data['match_state'] == 'completed'):
                        self.swipe_transition(self.current_scene + 1)
                    else:
                        self.player_page_data['match_state'] = 'waiting'
                        self.player_page_data['player_selection_alert'] = None
            if(self.player_page_data['computer_selection_alert'] != None):
                if(self.player_page_data['computer_selection_alert'].active):
                    self.player_page_data['computer_selection_alert'].draw(self.screen)
                else:
                    self.player_page_data['match_state'] = 'waiting'
                    self.player_page_data['computer_selection_alert'] = None
                 
            # Display particles when attacking with AW
            if(self.player_page_data['player_attack_particles'] != None):
                if(self.player_page_data['player_attack_particles'].active):
                    self.player_page_data['player_attack_particles'].draw(self.screen)
                else:
                    self.player_page_data['player_attack_particles'] = None
            if(self.player_page_data['opponent_attack_particles'] != None):
                if(self.player_page_data['opponent_attack_particles'].active):
                    self.player_page_data['opponent_attack_particles'].draw(self.screen)
                else:
                    self.player_page_data['opponent_attack_particles'] = None

            if(len(self.player_page_data['past_matches']) == 5):
                self.player_page_data['next_button'].draw(self.screen, mouse_x, mouse_y)


            # if(len(self.player_page_data['past_matches']) == 5 and self.player_page_data['match_state'] == 'waiting'):
                

    def handle_explanation_events(self, event):
        pass
        # Handle events on the explanation page.

    def explanation_page(self):
        text_surface = self.font.render("Explanation Page.", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(text_surface, text_rect)