import pygame
import pygame_gui
import os
from .config import manager


class GameState:
    def __init__(self, game,font_name="arial", font_size=50):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.load_assets()

    def load_assets(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        time_delta = self.clock.tick(60) / 1000.0
        manager.update(time_delta)

    def draw(self):
        pass


class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 100)
        self.load_assets()

    def load_assets(self):
        # Get the base directory path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construct correct path to images
        bg_path = os.path.join(base_dir, "resources", "images", "lake.png")
        try:
            self.bg = pygame.image.load(bg_path).convert_alpha()
        except FileNotFoundError:
            print(f"Error: Could not load background image at {bg_path}")
            # Create a blank surface as fallback
            self.bg = pygame.Surface((1280, 720))
            self.bg.fill((0, 0, 255))  # Blue fallback

        self.bg = pygame.transform.scale(self.bg, (1280, 720))

        self.title_surf = self.font.render("Level Up Game", True, "white")
        self.title_rect = self.title_surf.get_rect(center=(640, 150))

        # Create buttons
        button_width, button_height = 230, 100

        # Play button
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 275), (230, 100)), text='PLAY',manager=manager)

        # Options button
        self.options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 400), (230, 100)), text='OPTIONS',manager=manager)

        # Quit button
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 525), (230, 100)), text='QUIT',manager=manager)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.play_button:
                    self.game.change_state("play")
                elif event.ui_element == self.options_button:
                    self.game.change_state("options")
                elif event.ui_element == self.quit_button:
                    self.game.quit()

            manager.process_events(event)

    def update(self):
        super().update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 25)
        self.screen.blit(self.title_surf, self.title_rect)
        manager.draw_ui(self.screen)

class Play(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 50)
        self.load_assets()

    def load_assets(self):
        # Load game assets here
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("menu")

            manager.process_events(event)

    def update(self):
        super().update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("GAME SCREEN - Press ESC to return to menu", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        manager.draw_ui(self.screen)
        # Additional game rendering here

class Options(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 50)
        self.load_assets()

    def load_assets(self):
        # Load game assets here
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("menu")

            manager.process_events(event)

    def update(self):
        super().update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Options Screen - Press ESC to return to menu", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        manager.draw_ui(self.screen)