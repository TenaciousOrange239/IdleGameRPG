import pygame
import os
import json
import datetime
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from interface.gui import Menu, Play, Options, SaveLoadMenu, Inventory, Combat, Mining, Smithing, Hunting, Woodcutting, Cooking
from pygame import RESIZABLE
from interface.config import button_manager, selection_list_manager, panel_manager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()

        self.player_data = {
            "skills": {
                "mining": {"level": 1, "xp": 0, "max_xp": 100},
                "woodcutting": {"level": 1, "xp": 0, "max_xp": 100},
                "cooking": {"level": 1, "xp": 0, "max_xp": 100},
                "smithing": {"level": 1, "xp": 0, "max_xp": 100},
                "magic": {"level": 1, "xp": 0, "max_xp": 100},
                "hunting": {"level": 1, "xp": 0, "max_xp": 100},
                "combat": {"level": 1, "xp": 0, "max_xp": 100}
            },
            "inventory": {
                "ores": {},
                "wood": {},
                "food": {},
                "equipment": {}
            },
            "game_time": 0,
            "last_save": None
        }

        self.activity_data = {
            "mining": {
                "ores_mined": {
                    "Copper": 0,
                    "Iron": 0,
                    "Steel": 0,
                    "Tungsten": 0,
                    "Titanium": 0,
                    "Goatium": 0,
                    "Infinium": 0
                }
            },
            "woodcutting": {
                "wood_chopped": {
                    "Oak": 0,
                    "Dark Oak": 0,
                    "Darkest Oak": 0,
                    "Darker Oak (how???)": 0,
                    "Strong Wood": 0,
                    "Best Wood In The Game": 0
                }
            }
        }

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
            "options": Options(self),
            "saveload": SaveLoadMenu(self),


            "inventory": Inventory(self),
            "combat": Combat(self),
            "mining": Mining(self),
            "smithing": Smithing(self),
            "hunting": Hunting(self),
            "woodcutting": Woodcutting(self),
            "cooking": Cooking(self)
        }

        self.current_state = self.states["menu"]
        self.current_activity = self.states["mining"]

    def save_game(self, save_slot=1):
        """Save the current game state to a file."""
        # Create a save data dictionary with all relevant data
        save_data = {
            "player_data": self.player_data,
            "activity_data": self.activity_data,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Make sure the saves directory exists
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
        os.makedirs(save_dir, exist_ok=True)

        # Create the save file path
        save_path = os.path.join(save_dir, f"save_slot_{save_slot}.json")

        # Save the data to a JSON file
        try:
            with open(save_path, 'w') as save_file:
                json.dump(save_data, save_file, indent=2)

            self.player_data["last_save"] = datetime.datetime.now().isoformat()
            print(f"Game saved successfully to {save_path}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, save_slot=1):
        """Load a saved game from a file."""
        # Create the save file path
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
        save_path = os.path.join(save_dir, f"save_slot_{save_slot}.json")

        # Check if the save file exists
        if not os.path.exists(save_path):
            print(f"No save file found at {save_path}")
            return False

        # Load the data from the JSON file
        try:
            with open(save_path, 'r') as save_file:
                save_data = json.load(save_file)

            # Update the game state with the loaded data
            self.player_data = save_data["player_data"]
            self.activity_data = save_data["activity_data"]
            print(f"Game loaded successfully from {save_path}")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def change_state(self, state_name):
        button_manager.clear_and_reset()
        selection_list_manager.clear_and_reset()
        panel_manager.clear_and_reset()

        self.current_state = self.states[state_name]
        self.current_state.load_assets()

        if state_name == "play":
            self.current_state.reset()

    def change_activity(self, activity_name):
        # Clear current activity UI but preserve selection list
        panel_manager.clear_and_reset()
        button_manager.clear_and_reset()

        # Switch to the new activity
        self.current_activity = self.states[activity_name]  # Update current_activity
        self.current_state = self.states[activity_name]  # Also update current_state

        # Load assets and create UI for the new activity
        self.current_activity.load_assets()
        self.current_activity.create_ui()

    def run(self):
        while True:
            td = self.clock.tick(60) / 1000.0

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

                button_manager.process_events(event)
                selection_list_manager.process_events(event)
                panel_manager.process_events(event)

                # If we're in the Mining state, process ore button events
                if isinstance(self.current_state, Mining):
                    self.current_state.ore_button_manager.process_events(event)

                # Let the current state handle the event
                self.current_state.handle_event(event)

            # Update game state
            self.current_state.update(td)

            # Draw everything
            self.current_state.draw()

            # Update display
            pygame.display.flip()

            button_manager.update(td)
            selection_list_manager.update(td)
            panel_manager.update(td)

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
