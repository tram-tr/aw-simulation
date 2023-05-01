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

player_sprite = pygame.image.load("assets/images/Player.png")
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
        font_path = os.path.join("assets", "fonts", "PixelOperatorSC-Bold.ttf")
        self.font = pygame.font.Font(font_path, 20)
        self.display_time = 1000  # 1 second

        self.intro_text = [
            "Welcome to our simulation exploring", 
            "government use of autonomous weapons in conflict.",
            "Using game theory and the Prisoner's Dilemma,",
            "let's learn about the ethical implications.", 
            "",
            "Embark this exciting journey into", 
            "the world of autonomous weapons and game theory!"
        ]
        self.player_intro_text = [
            "1v1 MODE",
            "",
            "The year is 2050.",
            "You are the newly hired expert",
            "of autonomous weapons in USA's military.",
            "You must decide whether or not to use",
            "autonous weapons in conflict", "with each presented threat..."
        ]
        self.continue_button = Button(
            "Continue", self.settings.screen_width // 2 - 100, 400, 200, 50,
            (200, 200, 200), (225, 225, 225), self.font
        )
        self.current_scene = 0 
        self.num_scenes = 5
        self.running = True
        self.current_line = 0
        self.current_char = 0
        self.char_interval = 30
        self.char_interval = 1
        self.elapsed_time = 0

        self.navleft = NavArrowLeft(40)
        self.navright = NavArrowRight(40)

        self.player_page_data = {
            # 'description_top': {["The decision is yours to make. Before you, lies a terminal that controls an", 
            #                         "autonomous weapon system. If you activate it, your opponent gains an advantage,",
            #                         "but if they activate it, you gain an advantage. You both have a choice to either",
            #                         "COOPERATE (activate the weapon) or CHEAT (refrain from activating the weapon)."]},

            # 'description_bottom': {["Let's say your opponent decides to CHEAT and does not activate the weapon", 
            #                         "What's your move in this game of strategic warfare and moral dilemma?"]},

            'smoke_background': {
                'smoke': SmokeBackground(20, (0, 0, 0)),
                'active': True,
            },
            'use_button': Button("USE Autonomous Weapons", 
                (self.settings.screen_width // 4) - 175, self.settings.screen_height*0.75, 
                350, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'dont_use_button': Button("DONT'T Use Autonomous Weapons", 
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
            'country_resources': Resources(0, 0, (3*self.settings.screen_width/4, self.settings.screen_height/8), self.font),
            'next_button': Button("Continue", 
                (self.settings.screen_width // 4), self.settings.screen_height*0.75, 
                self.settings.screen_width//2, 50,
                (200, 200, 200), (225, 225, 225), self.font),

            # index = match's payoff
            # [(player_payoff, comp_payoff), (...)]
            'payoffs': [],
            
            # display lives and resources lost at end of game for total score 
            'player_lives_lost': 0,
            'player_resources_lost': 0,

            # player's results - sum of payoff from 5 matches 
            'result': 0
        }

        self.results_page_data = {
            'developed': [ "DEVELOPED: Greetings! I never start with force, but I’m not afraid ",
                          "to retaliate by copying your actions. An eye for an eye, a tooth for a tooth.",],
            'developing': [ "DEVELOPING: My priorities are always changing based on the needs of my country.",
                          "Might use ‘em, might not."],
            'resource': ["RESOURCE RICH: Fool me once, shame on you; fool me twice, shame on me.",
                         "I will not give second chances in war."],
            'military': ["MILITARY: We are not afraid to make sacrifices for the benefit of our country.",
                         "Autonomous weapons are the answer."],
            'peaceful': ["PEACEFUL: Violence is never the answer."],
        }

        self.tournament_page_data = {
            'instruction_panel': {
                'panel': InfoPanel(["It's showdown time! Each country will now play", "against every other country, five rounds per matchup.", "Who will emerge victorious? Think fast--and PLACE YOUR BETS!"], "Let's begin!", self.font),
                'active': True,
            },
            'round_data': [ "Match 1: Developed vs Military", 
                            "Match 2: Developed vs Developing", 
                            "Match 3: Developed vs Peaceful",
                            "Match 4: Developed vs Resource Rich",
                            "Match 5: Military vs Developing",
                            "Match 6: Military vs Peaceful",
                            "Match 7: Military vs Resource Rich",
                            "Match 8: Developing vs Peaceful",
                            "Match 9: Developing vs Resource Rich",
                            "Match 10: Peaceful vs Resource Rich" ], 

            'country_data': ["developed", "developing", "military", "peaceful", "resource rich"],
            'strategy_data': ["cautious", "unpredictable", "aggressive", "cooperative", "defensive"],
            'tournament_data': [[-1,3,0,0,0], [19,3,20,0,0], [39,3,20,20,0], [57,3,20,20,18], [57,33,10,20,18], [57,36,10,19,18], [57,45,10,19,15], [57,45,30,39,15], [57,45,29,39,42], [57,45,29,46,45]],
            'next_button': Button("Next match...", 
                (self.settings.screen_width // 4), self.settings.screen_height*0.75, 
                self.settings.screen_width//2, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'final_button': Button("Results!", 
                (self.settings.screen_width // 4), self.settings.screen_height*0.75, 
                self.settings.screen_width//2, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'current_match': 0,
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
    
    def _display_player_intro_text(self):
        y = 100
        for i, line in enumerate(self.player_intro_text[:self.current_line]):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 30

        # typing effect for the current line
        if self.current_line < len(self.player_intro_text):
            current_text = self.player_intro_text[self.current_line][:self.current_char]
            text_surface = self.font.render(current_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)

        self.elapsed_time += self.clock.get_time()
        if self.elapsed_time > self.char_interval:
            self.current_char += 1
            self.elapsed_time = 0
            if self.current_line < len(self.player_intro_text) and self.current_char > len(self.player_intro_text[self.current_line]):
                self.current_line += 1
                self.current_char = 0

    def run(self):
        # game loop
        while self.running:
            self._handle_events()
            #self._update()
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
                self.handle_intro_events(event)
            elif(self.current_scene == 2):
                self.handle_player_events(event)
            elif(self.current_scene == 3):
                self.handle_explanation_events(event)
            elif(self.current_scene == 3):
                self.handle_tournament_events(event)
                
    def handle_intro_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.continue_button.is_hover(mouse_x, mouse_y):
                self.change_scene(self.current_scene+1)
                pygame.time.wait(300)

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
        if(self.current_scene > 1):
            # Set up the left arrow coordinates
            self.navleft.draw(self.screen, mouse_x, mouse_y)
        
        # Right arrow
        if((self.current_scene < self.num_scenes-1) and (self.current_scene > 1)):
            # Set up the right arrow coordinates
            self.navright.draw(self.screen, mouse_x, mouse_y)

    def scene_manager(self):
        if(self.current_scene == -1):
            self.running = False
        elif(self.current_scene == 0):
            self.intro_page()
        elif(self.current_scene == 1):
            self.player_intro_page()
        elif(self.current_scene == 2):
            self.player_page()
        elif(self.current_scene == 3):
            self.explanation_page()
        elif(self.current_scene == 3):
            self.tournament_page()

        self.draw_nav_arrows()

    def intro_page(self):
        self._display_intro_text()
        if self.current_line >= len(self.intro_text):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.continue_button.draw(self.screen, mouse_x, mouse_y)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.continue_button.draw(self.screen, mouse_x, mouse_y)
    
    def player_intro_page(self):
        self._display_player_intro_text()
        if self.current_line >= len(self.intro_text):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.continue_button.draw(self.screen, mouse_x, mouse_y)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.continue_button.draw(self.screen, mouse_x, mouse_y)


    def handle_player_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            print(self.player_page_data['past_matches'])
            print(self.player_page_data['match_state'])

            mouse_x, mouse_y = pygame.mouse.get_pos()
    
            if len(self.player_page_data['past_matches']) == 5 and self.player_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.swipe_transition(self.current_scene + 1)
            else:
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
                            # 1 - use ; 0 - not use
                            player_choice = None
                            if self.player_page_data['use_button'].is_hover(mouse_x, mouse_y):
                                player_choice = 1
                            elif self.player_page_data['dont_use_button'].is_hover(mouse_x, mouse_y):
                                player_choice = 0
                            self.player_page_data['player_selection'] = player_choice
                            computer_choice = get_computer_choice(self.player_page_data['current_opponent']['id'], self.player_page_data['rounds'])
                            self.player_page_data['computer_selection'] = computer_choice

                            # use nash equilibrium
                            if player_choice == 1 and computer_choice == 1:
                                self.player_page_data['player_resources'].lives -= 10
                                self.player_page_data['player_resources'].resources -= 100
                                self.player_page_data['country_resources'].lives -= 10
                                self.player_page_data['country_resources'].resources -= 100
                            elif player_choice == 1 and computer_choice == 0:
                                self.player_page_data['player_resources'].resources -= 100
                                self.player_page_data['country_resources'].lives -= 100
                            elif player_choice == 0 and computer_choice == 1:
                                self.player_page_data['player_resources'].lives -= 100
                                self.player_page_data['country_resources'].resources -= 100
                            elif player_choice == 0 and computer_choice == 0:
                                self.player_page_data['player_resources'].lives -= 1
                                self.player_page_data['player_resources'].resources -= 10
                                self.player_page_data['country_resources'].lives -= 1
                                self.player_page_data['country_resources'].resources -= 10

                            # Alert the player and computer choices
                            player_alert_string = "" 
                            if(player_choice == 1): 
                                player_alert_string = "Uses AWs!"
                            else: 
                                player_alert_string = "Doesn't use AWs!"
                            computer_alert_string = ""
                            if(computer_choice == 1):
                                computer_alert_string = "Uses AWs!"
                            else:
                                computer_alert_string = "Doesn't use AWs!"
                            
                            self.player_page_data['player_selection_alert'] = AlertPanel(player_alert_string, self.player_position[0]-(sprite_size/2), self.player_position[1]-(sprite_size/2), sprite_size*2, (sprite_size/4), self.font)
                            self.player_page_data['computer_selection_alert'] = AlertPanel(computer_alert_string, self.opponent_position[0]-(sprite_size/2), self.opponent_position[1]-(sprite_size/2), sprite_size*2, (sprite_size/4), self.font)


                            # If attacking with AW, create explode particles
                            if(player_choice == 1):
                                self.player_page_data['opponent_attack_particles'] = ExplodeEffect((self.opponent_position[0] + (sprite_size/2), self.opponent_position[1] + (sprite_size/2)), 10, (30, 30, 30))
                            if(computer_choice == 1):
                                self.player_page_data['player_attack_particles'] = ExplodeEffect((self.player_position[0] + (sprite_size/2), self.player_position[1] + (sprite_size/2)), 10, (30, 30, 30))
                            
                            # Save the past round
                            self.player_page_data['rounds'].append((player_choice, computer_choice))
                            # when current match is over
                            if(len(self.player_page_data['rounds']) == 5):
                                # record current match to past_matches array 
                                self.player_page_data['past_matches'].append(('match {0}'.format(self.player_page_data['current_match'] + 1),self.player_page_data['rounds']))
                                # reset rounds array
                                self.player_page_data['rounds'] = []
                                # calculate payoffs
                                player_payoff = (0.7 * self.player_page_data['player_resources'].lives) + (0.3 * self.player_page_data['player_resources'].resources)
                                computer_payoff = (0.7 * self.player_page_data['country_resources'].lives) + (0.3 * self.player_page_data['country_resources'].resources)
                                # record payoffs 
                                self.player_page_data['payoffs'].append(
                                    (player_payoff, computer_payoff)
                                )
                                # record player's game total loss of lives and resources
                                self.player_page_data['player_lives_lost'] += self.player_page_data['player_resources'].lives
                                self.player_page_data['player_resources_lost'] += self.player_page_data['player_resources'].resources

                                # if current match is no more than fifth one
                                if(len(self.player_page_data['past_matches']) < 5):
                                    self.player_page_data['current_match'] += 1
                                    self.player_page_data['current_opponent'] = opponents[self.player_page_data['current_match']]
                                
                                # if five matches have been completed
                                else: 
                                    self.player_page_data['state'] = 'completed'
                                    # calculate player's result which is the sum of payoffs from 5 matches
                                    result = 0
                                    for match in self.player_page_data['payoffs']:
                                        result += match[0]

                                    
                                    

    def draw_player_choices(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if(self.player_page_data['match_state'] == 'waiting' and len(self.player_page_data['past_matches']) < 5):
            self.player_page_data['use_button'].draw(self.screen, mouse_x, mouse_y)
            self.player_page_data['dont_use_button'].draw(self.screen, mouse_x, mouse_y)
            pygame.display.flip()

    def player_page(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player_page_data['smoke_background']['active'] = False #temp fix @solina

        if(self.player_page_data['smoke_background']['active']):
            self.player_page_data['smoke_background']['smoke'].draw(self.screen)

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
    
        self.screen.blit(player_sprite, self.player_position)
        self.screen.blit(self.player_page_data['current_opponent']['sprite'], self.opponent_position)

        self.player_page_data['player_resources'].draw(self.screen)
        self.player_page_data['country_resources'].draw(self.screen)

        self.draw_player_choices()

        # Display response message
        if (self.player_page_data['player_selection_alert'] != None) and (self.player_page_data['computer_selection_alert'] != None) :
        # and (self.player_page_data['player_selection_alert'].active) and (self.player_page_data['computer_selection_alert'].active):
            # start_time = pygame.time.get_ticks()  # get current time in milliseconds
            # while pygame.time.get_ticks() - start_time < self.display_time: # display for 1 second
            self.player_page_data['player_selection_alert'].draw(self.screen)
            self.player_page_data['computer_selection_alert'].draw(self.screen)
            pygame.display.flip()  # update the screen

            pygame.time.wait(1000) # display for 1.5 seconds

            # pop alert panel
            self.player_page_data['match_state'] = 'waiting'
            self.player_page_data['player_selection_alert'] = None
            self.player_page_data['computer_selection_alert'] = None
            self.draw_player_choices()


        else:
            if(self.player_page_data['match_state'] == 'completed'):
                self.swipe_transition(self.current_scene + 1)
            else:
                self.player_page_data['match_state'] = 'waiting'
                self.player_page_data['player_selection_alert'] = None
                self.player_page_data['computer_selection_alert'] = None

        # Display particles when attacking with AW
        # if(self.player_page_data['player_attack_particles'] != None):
        #     if(self.player_page_data['player_attack_particles'].active):
        #         self.player_page_data['player_attack_particles'].draw(self.screen)
        #     else:
        #         self.player_page_data['player_attack_particles'] = None
        # if(self.player_page_data['opponent_attack_particles'] != None):
        #     if(self.player_page_data['opponent_attack_particles'].active):
        #         self.player_page_data['opponent_attack_particles'].draw(self.screen)
        #     else:
        #         self.player_page_data['opponent_attack_particles'] = None

        if(len(self.player_page_data['past_matches']) == 5):
            self.player_page_data['next_button'].draw(self.screen, mouse_x, mouse_y)


        # if(len(self.player_page_data['past_matches']) == 5 and self.player_page_data['match_state'] == 'waiting'):
                


    def handle_explanation_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.tournament_page_data['instruction_panel']['panel'].active:
                self.tournament_page_data['instruction_panel']['panel'].active = False
            elif self.tournament_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.swipe_transition(self.current_scene + 1)
        # Handle events on the explanation page.

    def explanation_page(self):
        # Render the title text
        # text_surface = self.font.render("Explanation page", True, (0, 0, 0))
        # text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        # self.screen.blit(text_surface, text_rect)
        # Define the text to display

        font_path = os.path.join("assets", "fonts", "PixelOperatorSC-Bold.ttf")
        self.font = pygame.font.Font(font_path, 18)
        # Render the text
        text_surface = self.font.render("Your total scores are...", True, (0,0,0))

        # Draw the text on the screen surface
        self.screen.blit(text_surface, (30, 30))
        
        self.font = pygame.font.Font(font_path, 14)
        # Render the explanation text for each category
        y_offset = 100
        for key, values in self.results_page_data.items():
            for value in values:
                explanation_surface = self.font.render(value, True, (0, 0, 0))
                explanation_rect = explanation_surface.get_rect(center=(self.settings.screen_width // 2, y_offset))
                self.screen.blit(explanation_surface, explanation_rect)
                y_offset += 30
            y_offset += 20

    
    def handle_tournament_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.tournament_page_data['instruction_panel']['panel'].active:
                self.tournament_page_data['instruction_panel']['panel'].active = False
            elif self.tournament_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.swipe_transition(self.current_scene + 1)

    def tournament_page(self):
        text_surface = self.font.render("The tournament", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(text_surface, text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
    
    def tournament_results(self):
        text_surface = self.font.render("Tournament results", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(text_surface, text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()