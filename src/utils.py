# src/utils.py
import pygame
import random
import math

from src.settings import Settings

settings = Settings()

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
        self.text_color = (0,0,0)

    def draw(self, screen, mouse_x, mouse_y):
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))

        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(button_surface, color, pygame.Rect(0, 0, self.width, self.height))
        screen.blit(button_surface, (self.x, self.y))

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_hover(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def update_colors(self, color, hover_color, text_color):
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        return

class InfoPanel:
    def __init__(self, main_text, button_text, font):
        self.main_text = main_text
        self.button_text = button_text
        self.panel_color = (200, 200, 200)
        self.font = font

        self.panel_width = settings.screen_width/2
        self.panel_height = settings.screen_height/2
        self.panel_x = (settings.screen_width/2) - (self.panel_width/2)
        self.panel_y = (settings.screen_height/8)

        self.active = True

        button_width = self.panel_width/2
        button_height = self.panel_height/4
        button_x = (settings.screen_width/2) - (button_width/2)
        button_y = (settings.screen_height * 0.75)-(button_height/2)
        button_color = (200, 200, 200)
        button_hover_color = (225, 225, 225)

        self.button = Button(self.button_text, button_x, button_y, button_width, button_height, button_color, button_hover_color, self.font)

    def draw(self, screen, mouse_x, mouse_y):

        # Draw the panel
        panel_surface = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.panel_color)

        pygame.draw.rect(panel_surface, self.panel_color, pygame.Rect(0, 0, self.panel_width, self.panel_width))
        screen.blit(panel_surface, (self.panel_x, self.panel_y))

        # Draw the panel text
        text_y = self.panel_y + 30
        for i, line in enumerate(self.main_text):
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(settings.screen_width // 2, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 30

        # main_text_surface = self.font.render(self.main_text, True, (0, 0, 0))
        # main_text_rect = main_text_surface.get_rect(center=(self.panel_x + self.panel_width // 2, self.panel_y + self.panel_height // 2))
        # screen.blit(main_text_surface, main_text_rect)

        # Draw the button
        self.button.draw(screen, mouse_x, mouse_y)

    def is_hover(self, mouse_x, mouse_y):
        return self.button.is_hover(mouse_x, mouse_y)
        # return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
   
def translate(value, leftMin, leftMax, rightMin, rightMax):

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class SmokeParticle:
    def __init__(self, color):
        self.active = True
        self.x = random.randint(0, settings.screen_width)
        self.y = settings.screen_height + random.randint(50, 200)
        self.radius = random.randint(3, 10)

        self.color = color

        self.rise_speed = random.randint(1, 3)
        self.decay_rate = random.uniform(0.01, 0.03)/10
        self.tick_rate = random.randint(1, 5)
        self.tick_counter = 0
        self.decay_counter = 1
        self.amplitude = random.randint(1, 5)
        self.wobble_rate = random.uniform(0.1, 0.2)
        

    def draw(self, surface):
        self.decay_counter -= self.decay_rate
        if((self.decay_counter <= 0) or (self.y < (self.radius * -1))):
            self.active = False
            return

        # Calculate the new position of the particle
        curr_x = self.x + math.sin((self.tick_counter/20) * self.wobble_rate) * (self.amplitude * (self.tick_counter/50))
        self.y -= self.rise_speed

        # Calculate the new radius and transparency of the particle
        radius = self.radius + self.tick_counter/20
        alpha = 255 * self.decay_counter

        # Draw the particle on the surface
        color = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(surface, color, (curr_x, self.y), radius)

        # Update the particle's tick counter and amplitude
        self.tick_counter += self.tick_rate
        self.decay_counter -= self.decay_rate

class SmokeBackground:
    def __init__(self, max_particles, particle_color):
        self.max_particles = max_particles
        self.color = particle_color

        self.particles = []
        for i in range(max_particles):
            new_particle = SmokeParticle(self.color)
            self.particles.append(new_particle)
    
    def draw(self, screen):
        if(len(self.particles) < self.max_particles):
            if(random.randint(0, 30) < 2):
                new_particle = SmokeParticle(self.color)
                self.particles.append(new_particle)

        smoke_surface = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA)

        if(len(self.particles) > 0):
            i = 0
            while(i < len(self.particles)):
                particle = self.particles[i]
                if(particle.active):
                    particle.draw(smoke_surface)
                    i += 1
                else:
                    del self.particles[i]
                    i -= 1

        # pygame.draw.rect(smoke_surface, (255, 255, 255), pygame.Rect(0, 0, settings.screen_width, settings.screen_height))
        screen.blit(smoke_surface, (0, 0))

class NavArrowLeft:
    def __init__(self, size):
        self.size = size
        self.x = 1*size
        self.y = settings.screen_height - 1.5*size
        self.color = (200, 200, 200)
        self.hover_color = (225, 225, 225)

    def draw(self, screen, mouse_x, mouse_y):
        if(self.is_hover(mouse_x, mouse_y)):
            pygame.draw.polygon(screen, self.hover_color, [(self.x, self.y + self.size/2), (self.x + self.size, self.y), (self.x + self.size, self.y + self.size)])
        else:
            pygame.draw.polygon(screen, self.color, [(self.x, self.y + self.size/2), (self.x + self.size, self.y), (self.x + self.size, self.y + self.size)])

    def is_hover(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.size and self.y <= mouse_y <= self.y + self.size

class NavArrowRight:
    def __init__(self, size):
        self.size = size
        self.x = settings.screen_width - 2*size
        self.y = settings.screen_height - 1.5*size
        self.color = (200, 200, 200)
        self.hover_color = (225, 225, 225)

    def draw(self, screen, mouse_x, mouse_y):
        if(self.is_hover(mouse_x, mouse_y)):
            pygame.draw.polygon(screen, self.hover_color, [(self.x, self.y), (self.x + self.size, self.y + self.size/2), (self.x, self.y + self.size)])
        else:
            pygame.draw.polygon(screen, self.color, [(self.x, self.y), (self.x + self.size, self.y + self.size/2), (self.x, self.y + self.size)])

    def is_hover(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.size and self.y <= mouse_y <= self.y + self.size


class ExplodeParticle:
    def __init__(self, pos, color):
        self.active = True
        self.x = pos[0]
        self.y = pos[1]

        vel_x = random.randint(1, 3)
        if((random.randint(0,100)%2)): vel_x = vel_x * -1
        vel_y = random.randint(1, 3)
        if((random.randint(0,100)%2)): vel_y = vel_y * -1

        self.vel_x = vel_x
        self.vel_y = vel_y
        
        self.radius = random.randint(3, 10)
        self.thickness = 5

        self.color = color

        # self.rise_speed = random.randint(1, 3)
        self.decay_rate = random.uniform(0.01, 0.03)/3
        self.tick_rate = random.randint(1, 5)
        self.tick_counter = 0
        self.decay_counter = 1
        # self.amplitude = random.randint(1, 5)
        # self.wobble_rate = random.uniform(0.1, 0.2)
        

    def draw(self, surface):
        self.decay_counter -= self.decay_rate
        if((self.decay_counter <= 0) or (self.y < (self.radius * -1))):
            self.active = False
            return

        # Calculate the new position of the particle
        self.x += self.vel_x
        self.y += self.vel_y

        # Calculate the new radius and transparency of the particle
        radius = self.radius + self.tick_counter/20
        alpha = 255 * self.decay_counter

        # Draw the particle on the surface
        color = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(surface, color, (self.x, self.y), radius, round(self.thickness*self.decay_counter) + 1)

        # Update the particle's tick counter and amplitude
        self.tick_counter += self.tick_rate
        self.decay_counter -= self.decay_rate

class ExplodeEffect:
    def __init__(self, pos, max_particles, particle_color):
        self.active = True
        self.max_particles = max_particles
        self.color = particle_color
        self.particles = []
        for i in range(max_particles):
            new_particle = ExplodeParticle(pos, self.color)
            self.particles.append(new_particle)
    
    def draw(self, screen):
        if(len(self.particles) == 0):
            self.active = False

        explode_surface = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA)

        if(len(self.particles) > 0):
            i = 0
            while(i < len(self.particles)):
                try:
                    particle = self.particles[i]
                    if(particle.active):
                        particle.draw(explode_surface)
                        i += 1
                    else:
                        del self.particles[i]
                        i -= 1
                except:
                    self.active = False
                    return

        # pygame.draw.rect(smoke_surface, (255, 255, 255), pygame.Rect(0, 0, settings.screen_width, settings.screen_height))
        screen.blit(explode_surface, (0, 0))


class AlertPanel:
    def __init__(self, text, x, y, width, height, font):
        self.active = True
        self.created = pygame.time.get_ticks()
        self.active_time = 2000
        self.fade_time = 1000
        self.fade_duration = 1000

        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = None
        self.font = font
    
        if (text == "Uses AWs!"):
            self.color = (92, 232, 92)
        else:
            self.color = (232, 92, 92)

        self.text_color = (255, 255, 255)

    def draw(self, screen):

        alpha = 1
        if self.active_time > 0:
            self.active_time -= (pygame.time.get_ticks() - self.created)
        elif self.fade_time > 0:
            self.fade_time -= (pygame.time.get_ticks() - self.created)
            alpha = (self.fade_time/self.fade_duration)
        
        if alpha < 0 or self.fade_time < 0: 
            self.active = False
            return
        else:
            alpha = round(alpha*255)

        
        color = (self.color[0], self.color[1], self.color[2], alpha)

        alert_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        alert_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(alert_surface, color, pygame.Rect(0, 0, self.width, self.height))
        screen.blit(alert_surface, (self.x, self.y))

        text_color = (self.text_color[0], self.text_color[1], self.text_color[2], alpha)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
