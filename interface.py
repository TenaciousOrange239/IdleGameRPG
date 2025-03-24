import pygame
import sys
from pygame import RESIZABLE
import button

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(self.screen)
        self.font = pygame.font.Font('fonts/Gotham/GothamBook.ttf')
        self.game_active = False

        self.load_assets()

    def load_assets(self):
        self.bg = pygame.image.load('images/swamp.png').convert_alpha()
        self.bg = pygame.transform.rotozoom(self.bg, 0, 1.2)
        self.bg_rect = self.bg.get_rect(center=(640, 360))

        self.title_surf = self.font.render("Idle Game", True, "gold")
        self.title_rect = self.title_surf.get_rect(center=(640, 180))
        pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        if not self.game_active:
            self.draw_title_screen()

    def draw_title_screen(self):
        self.screen.blit(self.bg, self.bg_rect)
        self.screen.blit(self.title_surf, self.title_rect)
        pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()

def main():
    gui = GUI()
    gui.run()

if __name__ == "__main__":
    main()