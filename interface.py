import pygame
import sys
from pygame import RESIZABLE
from button.button import Button

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load('images/bh.png')
        self.font = pygame.font.Font('fonts/Gotham/GothamBook.ttf')
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
        super().__init__()

    def load_assets(self):
        self.bg = pygame.image.load('images/swamp.png').convert_alpha()
        self.bg = pygame.transform.rotozoom(self.bg, 0, 1.2)
        self.bg_rect = self.bg.get_rect(center=(640, 360))

        self.title_surf = self.font.render("Idle Game", True, "gold")
        self.title_surf = pygame.transform.rotozoom(self.title_surf, 0, 3)
        self.title_rect = self.title_surf.get_rect(center=(640, 180))

    def draw_title_screen(self):
        self.screen.blit(self.bg, self.bg_rect)
        self.title_bg = pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 5)
        self.screen.blit(self.title_surf, self.title_rect)

        Play_Button = Button(image="images/bh.png",x_pos=640,y_pos=400,txt_input="PLAY",font_name='Comic Sans MS', font_size=100)

    def update(self):
        if not self.game_active:
            self.draw_title_screen()

class Play(GUI):
    pass