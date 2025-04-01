import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from interface.gui import Menu, Play, Options
from pygame import RESIZABLE
from interface.config import manager

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
            "play": Play(self),
            "options": Options(self)
        }

        self.current_state = self.states["menu"]

    def change_state(self, state_name):
        # Clear all UI elements from the previous state
        manager.clear_and_reset()
        # Change to the new state
        self.current_state = self.states[state_name]
        # Initialize UI elements in the new state
        self.current_state.load_assets()

        # Special case for Play state
        if state_name == "play":
            self.current_state.create_ui()

    def run(self):
        while True:
            td = self.clock.tick(60) / 1000.0

            # Handle events
            self.current_state.handle_events()

            # Update game state
            self.current_state.update(td)  # Pass time_delta here

            # Draw everything
            self.current_state.draw()

            # Update display
            pygame.display.flip()

            manager.update(td)


    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()