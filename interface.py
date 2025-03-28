import pygame
import sys
from pygame import RESIZABLE
from button.button import Button

class GUI:
    def __init__(self,font_name,font_size):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load('images/bh.png')
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_name,self.font_size)
        self.game_active = False

        self.load_assets()

    def load_assets(self):
        pass

    def handle_events(self):
        pass

    def run(self):
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        pass


class Menu(GUI):
    def __init__(self):
        super().__init__("arial",100)

    def load_assets(self):
        self.bg = pygame.image.load('images/lake.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1280,720))
        self.bg_rect = self.bg.get_rect(center=(640, 360))

        self.title_surf = self.font.render("Idle Game", True, "white")
        self.title_rect = self.title_surf.get_rect(center=(640, 150))

        button_width, button_height = 230, 100
        play_button_surface = pygame.Surface((button_width,button_height), pygame.SRCALPHA)
        pygame.draw.rect(play_button_surface, (50, 50, 70), (0, 0, button_width, button_height-7), border_radius=25)
        self.play_button = Button(play_button_surface, 640, 350, "PLAY", "white", "green", "gotham", 90)

        options_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(options_button_surface, (50, 50, 70), (0, 0, button_width, button_height), border_radius=25)
        self.options_button = Button(options_button_surface, 640, 465, "OPTIONS", "white", "green", "arial", 55)

        quit_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(quit_button_surface, (50, 50, 70), (0, 0, button_width, button_height), border_radius=25)
        self.quit_button = Button(quit_button_surface, 640, 590, "QUIT", "white", "green", "arial", 70)

    def draw_title_screen(self):
        self.screen.blit(self.bg, self.bg_rect)
        self.title_bg = pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 20)
        self.screen.blit(self.title_surf, self.title_rect)

        for button in [self.play_button,self.options_button,self.quit_button]:
            button.update(self.screen)
            button.changeColour(pygame.mouse.get_pos())

    def update(self):
        if not self.game_active:
            self.draw_title_screen()

    def handle_events(self):
        super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_active:  # Only check buttons in menu
                    if self.play_button.checkforInput(pygame.mouse.get_pos()):
                        self.game_active = False
                    if self.options_button.checkforInput(pygame.mouse.get_pos()):
                        self.game_active = False  # Or handle options
                    if self.quit_button.checkforInput(pygame.mouse.get_pos()):
                        self.quit()

class Play(GUI):
    def __init__(self):
        super().__init__("arial",100)

    def play(self):
        pygame.display.set_caption("")

        while True:







