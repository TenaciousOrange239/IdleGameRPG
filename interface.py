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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()

class Menu(GUI):
    def __init__(self):
        super().__init__("arial",100)

    def load_assets(self):
        self.bg = pygame.image.load('images/lake.png').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1280,720))
        self.bg_rect = self.bg.get_rect(center=(640, 360))

        self.title_surf = self.font.render("Idle Game", True, "white")
        self.title_surf = pygame.transform.rotozoom(self.title_surf, 0, 1)
        self.title_rect = self.title_surf.get_rect(center=(640, 180))

        button_surface = pygame.image.load("images/bh.png")
        button_surface = pygame.transform.scale(button_surface, (400, 150))
        self.play_button = Button(button_surface, 640, 400, "PLAY", "white", "green", "arial", 120)

    def draw_title_screen(self):
        self.screen.blit(self.bg, self.bg_rect)
        self.title_bg = pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 20)
        self.screen.blit(self.title_surf, self.title_rect)

        self.play_button.update(self.screen)
        self.play_button.changeColour(pygame.mouse.get_pos())

    def update(self):
        if not self.game_active:
            self.draw_title_screen()

    def handle_events(self):
        super().handle_events()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkforInput(pygame.mouse.get_pos()):
                    self.game_active = True

class Play(GUI):
    def __init__(self):
        super().__init__()
