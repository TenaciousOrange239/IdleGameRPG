import pygame
import sys
import os
from pygame import RESIZABLE

from IdleGameRPG.interface.button import Button


class GameState:
    def __init__(self, game, font_name="arial", font_size=50):
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
        pass

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
        play_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(play_button_surface, (50, 50, 70), (0, 0, button_width, button_height - 7), border_radius=25)
        self.play_button = Button(play_button_surface, 640, 350, "PLAY", "white", "green", "gotham", 90)

        # Options button
        options_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(options_button_surface, (50, 50, 70), (0, 0, button_width, button_height - 7), border_radius=25)
        self.options_button = Button(options_button_surface, 640, 465, "OPTIONS", "white", "green", "gotham", 65)

        # Quit button
        quit_button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        pygame.draw.rect(quit_button_surface, (50, 50, 70), (0, 0, button_width, button_height - 7), border_radius=25)
        self.quit_button = Button(quit_button_surface, 640, 590, "QUIT", "white", "green", "gotham", 90)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkforInput(pygame.mouse.get_pos()):
                    self.game.change_state("play")
                elif self.options_button.checkforInput(pygame.mouse.get_pos()):
                    print("Options button pressed")
                elif self.quit_button.checkforInput(pygame.mouse.get_pos()):
                    self.game.quit()

    def update(self):
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.play_button, self.options_button, self.quit_button]:
            button.changeColour(mouse_pos)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 25)
        self.screen.blit(self.title_surf, self.title_rect)

        # Draw buttons
        for button in [self.play_button, self.options_button, self.quit_button]:
            button.update(self.screen)


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

    def update(self):
        # Game logic updates here
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("GAME SCREEN - Press ESC to return to menu", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        # Additional game rendering here


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()

        # Load icon with proper path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "resources", "images", "bh.png")
        try:
            self.icon = pygame.image.load(icon_path)
            pygame.display.set_icon(self.icon)
        except FileNotFoundError:
            print(f"Could not load icon at {icon_path}")

        # Initialize game states
        self.states = {
            "menu": Menu(self),
            "play": Play(self)
        }
        self.current_state = self.states["menu"]

    def change_state(self, state_name):
        """Switch to another game state"""
        self.current_state = self.states[state_name]

    def run(self):
        """Main game loop"""
        while True:
            # Handle events
            self.current_state.handle_events()

            # Update game state
            self.current_state.update()

            # Draw everything
            self.current_state.draw()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

    def quit(self):
        pygame.quit()
        sys.exit()