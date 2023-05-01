# src/game.py

import pygame
import os
from src.settings import Settings
from src.sprites import *
from src.utils import *

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
        self.num_rounds = 5
        self.num_opponents = len(opponents)
        self.player_name = "You" 

        # color definitions
        self.rgb_colors = dict()
        self.rgb_colors["gray"] = (128, 128, 128)
        self.rgb_colors["green"] = (92, 232, 92)
        self.rgb_colors["dark_green"] = (68, 187, 68)
        self.rgb_colors["red"] = (232, 92, 92)
        self.rgb_colors["dark_red"] = (187, 68, 68)
        self.rgb_colors["black"] = (0,0,0)
        self.rgb_colors["explosion_color"] = (138, 2, 2) # blood red

        # league_results[0][1] = opponents[0] payoff in opponents[0] vs opponents[1]
        # league_results[1][0] = opponents[1] payoff in opponents[0] vs opponents[1]
        self.league_results = {i: [-1] * self.num_opponents for i in range(self.num_opponents)}

        self.life_weight = 0.7
        self.resource_weight = 0.3
        # damage weights applied to life & resources
    
        self.min_damage = 1
        self.mid_damage = 10
        self.max_damage = 100

        self.intro_text = [
            "Welcome to our simulation exploring", 
            "government use of autonomous weapons in conflict.",
            "Let's learn about the ethical implications", 
            "using game theory and the Prisoner's Dilemma.",
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
                self.rgb_colors["green"], self.rgb_colors["dark_green"], self.font), # green
            'dont_use_button': Button("DONT'T Use Autonomous Weapons", 
                (3*self.settings.screen_width // 4) - 175, self.settings.screen_height*0.75, 
                350, 50,
                self.rgb_colors["red"], self.rgb_colors["dark_red"], self.font), # red
            'past_matches': [],
            'match_state': 'waiting',
            'current_match': -1,
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
        self.tournament_intro_text = ["It's showdown time! Each country will now play", "against every other country, five rounds per matchup.", "Who will emerge victorious? Think fast--and PLACE YOUR BETS!"]
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

            # line coordinates
            "tournament_lines_dict" : {
                (0,1): [(400, 200), (285, 230)],
                (0,2): [(400, 200), (525, 230)],
                (0,3): [(400, 200), (320, 270)],
                (0,4): [(400, 200), (480, 270)],
                (1,2): [(285, 230), (525, 230)],
                (1,3): [(285, 230), (320, 270)],
                (1,4): [(285, 230), (480, 270)],
                (2,3): [(525, 230), (320, 270)],
                (2,4): [(525, 230), (480, 270)],
                (3,4): [(320, 270), (480, 270)]
            },
        
            'next_button': Button("Next Match", self.settings.screen_width // 2 - 100, 500, 200, 50,
            (200, 200, 200), (225, 225, 225), self.font),
            'final_button': Button("Results!", 
                (self.settings.screen_width // 4), self.settings.screen_height*0.75, 
                self.settings.screen_width//2, 50,
                (200, 200, 200), (225, 225, 225), self.font),
            'current_match': 0,
        }
        
        # calculate league simulation results before rendering
        self.run_league_simluation()


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
    
    def _display_tournament_intro_text(self):
        y = 100
        for i, line in enumerate(self.tournament_intro_text[:self.current_line]):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 30

        # typing effect for the current line
        if self.current_line < len(self.tournament_intro_text):
            current_text = self.tournament_intro_text[self.current_line][:self.current_char]
            text_surface = self.font.render(current_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.settings.screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)

        self.elapsed_time += self.clock.get_time()
        if self.elapsed_time > self.char_interval:
            self.current_char += 1
            self.elapsed_time = 0
            if self.current_line < len(self.tournament_intro_text) and self.current_char > len(self.tournament_intro_text[self.current_line]):
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
            elif(self.current_scene == 4):
                self.handle_intro_events(event)
            elif (self.current_scene == 5):
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
        elif(self.current_scene == 4):
            self.tournament_intro_page()
        elif(self.current_scene == 5):
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
    
    def tournament_intro_page(self):
        self._display_tournament_intro_text()
        if self.current_line >= len(self.tournament_intro_text):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.continue_button.draw(self.screen, mouse_x, mouse_y)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.continue_button.draw(self.screen, mouse_x, mouse_y)

    def run_league_simluation(self):
        for p1 in range(self.num_opponents):
            for p2 in range(self.num_opponents):

                # skip if already calculated
                if (self.league_results[p1][p2] != -1):
                    continue

                # simulating p1 vs p2...
                p1_past_rounds = list()
                p2_past_rounds = list()

                for r in range(self.num_rounds):
                    p1_choice = get_computer_choice(p1, p1_past_rounds)
                    p2_choice = get_computer_choice(p2, p2_past_rounds)

                    self.update_resources(p1_choice, p2_choice)
                    p1_past_rounds.append((p2_choice, p1_choice))
                    p2_past_rounds.append((p1_choice, p2_choice))

                # compute payoffs after 5 rounds  
                p1_payoff = self.compute_payoff("player_resources")
                p2_payoff = self.compute_payoff("country_resources")

                # store payoffs
                self.league_results[p1][p2] = p1_payoff
                self.league_results[p2][p1] = p2_payoff

                # reset data
                self.format_resources()

    def format_resources(self):
        self.player_page_data['player_resources'].lives = 0
        self.player_page_data['player_resources'].resources = 0
        self.player_page_data['country_resources'].lives = 0
        self.player_page_data['country_resources'].resources = 0


    def update_resources(self, player_choice, computer_choice):
        # use nash equilibrium
        if player_choice == 1 and computer_choice == 1:
            self.player_page_data['player_resources'].lives -= self.mid_damage
            self.player_page_data['player_resources'].resources -= self.max_damage
            self.player_page_data['country_resources'].lives -= 10
            self.player_page_data['country_resources'].resources -= self.max_damage
        elif player_choice == 1 and computer_choice == 0:
            self.player_page_data['player_resources'].resources -= self.max_damage
            self.player_page_data['country_resources'].lives -= self.max_damage
        elif player_choice == 0 and computer_choice == 1:
            self.player_page_data['player_resources'].lives -= 100
            self.player_page_data['country_resources'].resources -= self.max_damage
        elif player_choice == 0 and computer_choice == 0:
            self.player_page_data['player_resources'].lives -= self.min_damage
            self.player_page_data['player_resources'].resources -= self.mid_damage
            self.player_page_data['country_resources'].lives -= self.min_damage
            self.player_page_data['country_resources'].resources -= self.mid_damage


    def compute_payoff(self, mode):
        if not ((mode == "player_resources") or (mode == "country_resources")):
            raise ValueError("Invalid input for compute_payoff mode")

        return (self.life_weight * self.player_page_data[mode].lives) + (self.resource_weight * self.player_page_data[mode].resources)

    def handle_player_events(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            # print(self.player_page_data['past_matches'])
            # print(self.player_page_data['match_state'])

            mouse_x, mouse_y = pygame.mouse.get_pos()
    
            if len(self.player_page_data['past_matches']) == self.num_opponents and self.player_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.swipe_transition(self.current_scene + 1)
            else:
                if(len(self.player_page_data['past_matches']) < self.num_opponents):
                    if (self.player_page_data['match_state'] == 'waiting'):
                        if(self.player_page_data['use_button'].is_hover(mouse_x, mouse_y) or self.player_page_data['dont_use_button'].is_hover(mouse_x, mouse_y)):
                            self.player_page_data['match_state'] = 'selected'
                            self.player_page_data['selected_start_time'] = pygame.time.get_ticks()

                            # for every start of new match, initialize lives and resources to 0
                            if(len(self.player_page_data['rounds']) == 0):
                                self.format_resources()

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

                            self.update_resources(player_choice, computer_choice)
                            
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
                                self.player_page_data['opponent_attack_particles'] = ExplodeEffect((self.opponent_position[0] + (sprite_size/2), self.opponent_position[1] + (sprite_size/2)), 10, self.rgb_colors["explosion_color"])
                            if(computer_choice == 1):
                                self.player_page_data['player_attack_particles'] = ExplodeEffect((self.player_position[0] + (sprite_size/2), self.player_position[1] + (sprite_size/2)), 10, self.rgb_colors["explosion_color"])
                            
                            # Save the past round
                            self.player_page_data['rounds'].append((player_choice, computer_choice))
                            # when current match is over
                            if(len(self.player_page_data['rounds']) == self.num_rounds):
                                # record current match to past_matches array 
                                self.player_page_data['past_matches'].append(('match {0}'.format(self.player_page_data['current_match'] + 1),self.player_page_data['rounds']))
                                
                                # calculate payoffs
                                player_payoff = self.compute_payoff("player_resources")
                                computer_payoff = self.compute_payoff("country_resources")

                                # record payoffs 
                                self.player_page_data['payoffs'].append((player_payoff, computer_payoff))
                                # record player's game total loss of lives and resources
                                self.player_page_data['player_lives_lost'] += self.player_page_data['player_resources'].lives
                                self.player_page_data['player_resources_lost'] += self.player_page_data['player_resources'].resources

                                # if not at last opponent
                                if(len(self.player_page_data['past_matches']) < self.num_opponents):
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

        if(self.player_page_data['match_state'] == 'waiting' and len(self.player_page_data['past_matches']) < self.num_opponents):
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

        for i in range(self.num_rounds):
            circ_pos = (center_x, y_start)
            try:
                if(self.player_page_data['rounds'][i]):
                    pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 0)
                    
                    
            except:
                pygame.draw.circle(self.screen, (50, 50, 50), circ_pos, 20, 3)

            y_start += y_step
        
        # reset rounds array
        if (len(self.player_page_data['rounds']) == self.num_rounds):
            self.player_page_data['rounds'] = []
        
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

        # display user's name
        text_surface = self.font.render(self.player_name, True, (50, 50, 50))
        self.screen.blit(text_surface, (self.player_position[0]+(sprite_size/2.5), shadow_y +(sprite_size/2.5)))

        # display opponent name
        name = self.player_page_data['current_opponent']['name']
        text_surface = self.font.render(name, True, (50, 50, 50))
        self.screen.blit(text_surface, (self.opponent_position[0]+(sprite_size/2.5), shadow_y +(sprite_size/2.5)))


        # Display response message
        self.draw_player_choices()

        if (self.player_page_data['player_selection_alert'] != None) and (self.player_page_data['computer_selection_alert'] != None) :
        
            self.player_page_data['player_selection_alert'].draw(self.screen)
            self.player_page_data['computer_selection_alert'].draw(self.screen)

            # Display particles when attacking with AW
            if(self.player_page_data['player_attack_particles'] != None):
                if(self.player_page_data['player_attack_particles'].active):
                    self.player_page_data['player_attack_particles'].draw(self.screen)

            if(self.player_page_data['opponent_attack_particles'] != None):
                if(self.player_page_data['opponent_attack_particles'].active):
                    self.player_page_data['opponent_attack_particles'].draw(self.screen)
                    
            
            # update the screen & display for 1.5 seconds
            pygame.display.flip()  
            pygame.time.wait(1000)

            # pop alert panel
            self.player_page_data['match_state'] = 'waiting'
            self.player_page_data['player_selection_alert'] = None
            self.player_page_data['computer_selection_alert'] = None
            self.player_page_data['player_attack_particles'] = None
            self.player_page_data['opponent_attack_particles'] = None
            self.draw_player_choices()


        else:
            if(self.player_page_data['match_state'] == 'completed'):
                self.swipe_transition(self.current_scene + 1)
            else:
                self.player_page_data['match_state'] = 'waiting'
                self.player_page_data['player_selection_alert'] = None
                self.player_page_data['computer_selection_alert'] = None
    

        if(len(self.player_page_data['past_matches']) == self.num_opponents):
            self.player_page_data['next_button'].draw(self.screen, mouse_x, mouse_y)                


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
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if(event.type == pygame.MOUSEBUTTONDOWN):
            if self.tournament_page_data['next_button'].is_hover(mouse_x, mouse_y):
                self.tournament_page_data['current_match'] += 1
                if (self.tournament_page_data['current_match'] >= len(self.tournament_page_data['round_data'])):
                    self.change_scene(self.current_scene + 1)
                    pygame.time.wait(1000)

    def tournament_page(self):

        # Render the text
        text_surface = self.font.render("Tournament Mode", True, (0,0,0))
        text_rect = text_surface.get_rect(center=(self.settings.screen_width * 0.5, 30))
        self.screen.blit(text_surface, text_rect)

        # draw sprites & lines
        current_match = self.tournament_page_data['current_match']

        if (current_match < 0) or (current_match >= len(self.tournament_page_data['round_data'])):

            p1 = -1
            p2 = -1
        else:
            (p1, p2) = list(self.tournament_page_data["tournament_lines_dict"].keys())[current_match]

        self.draw_tournament_sprites()
        self.draw_tournament_lines(p1,p2)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.tournament_page_data['next_button'].draw(self.screen, mouse_x, mouse_y)

        self.tournament_results(p1,p2)
    
    def draw_tournament_sprites(self):
        sprite = opponents[0]['sprite']
        self.screen.blit(sprite, (340, 60))  # Draw the sprite at the top-left corner of the screen
        sprite = opponents[1]['sprite']
        self.screen.blit(sprite, (170, 150))
        sprite = opponents[2]['sprite']
        self.screen.blit(sprite, (520, 150))
        sprite = opponents[3]['sprite']
        self.screen.blit(sprite, (250, 280))
        sprite = opponents[4]['sprite']
        self.screen.blit(sprite, (450, 280))
        
    
    def draw_tournament_lines(self, p1, p2):
        tournament_lines = self.tournament_page_data["tournament_lines_dict"]
        for key in tournament_lines:
            
            start = tournament_lines[key][0]
            end = tournament_lines[key][1]

            if (min(p1, p2) == key[0] and max(p1,p2) == key[1]):
                color = self.rgb_colors['green']
            else:
                color = self.rgb_colors['gray']
            
            pygame.draw.line(self.screen, color, start, end) # 0 to 1


    def tournament_results(self, p1, p2):
        if (p1 < 0):
            return

        current_match = self.tournament_page_data['current_match']
        coords = list(self.tournament_page_data['tournament_lines_dict'].keys())[current_match]
        p1_payoff = self.league_results[coords[0]][coords[1]]
        p2_payoff = self.league_results[coords[1]][coords[0]]
        payoff_data = " ".join([str(p1_payoff), 'vs', str(p2_payoff)])
        round_data = self.tournament_page_data['round_data'][current_match]

        mouse_x, mouse_y = pygame.mouse.get_pos()

        text1 = self.font.render(round_data, True, self.rgb_colors["black"])
        text2 = self.font.render(payoff_data, True, self.rgb_colors["dark_green"])
        self.screen.blit(text1, text1.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height * 0.75)))
        self.screen.blit(text2, text2.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height * 0.80)))
