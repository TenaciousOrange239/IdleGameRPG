import pygame
import os
import json
import datetime
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from interface.gui import Menu, Play, SaveLoadMenu, Inventory, Combat, Mining, Smithing, Woodcutting
from interface.config import button_manager, selection_list_manager, panel_manager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Death in Kill Land")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.show_fps = False  # Toggle for showing FPS counter

        # pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "audio", "tang.mp3"))
        # pygame.mixer.music.play(-1)

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
        icon_path = os.path.join(base_dir, "resources", "images", "lake.png")
        try:
            self.icon = pygame.image.load(icon_path)
            pygame.display.set_icon(self.icon)
        except FileNotFoundError:
            print(f"Could not load icon at {icon_path}")

        # Initialize font for FPS display
        self.font = pygame.font.SysFont(None, 24)

        # Initialize game states
        self.states = {
            "menu": Menu(self),
            "play": Play(self),
            "saveload": SaveLoadMenu(self),

            "inventory": Inventory(self),
            "combat": Combat(self),
            "mining": Mining(self),
            "smithing": Smithing(self),
            "woodcutting": Woodcutting(self)
        }

        self.current_state = self.states["menu"]
        self.current_activity = self.states["mining"]

    def calculate_xp_for_level(self, level):
        # Simple exponential formula for level progression
        # Level 1 = 0 XP
        # Level 2 = 83 XP
        # Levels get progressively harder
        return int(sum(int(level * (1 + level * 0.1)) for level in range(1, level)))

    def add_skill_xp(self, skill, amount):
        if skill not in self.player_data["skills"]:
            return False

        # Add XP
        self.player_data["skills"][skill]["xp"] += amount
        current_level = self.player_data["skills"][skill]["level"]

        # Check if level up occurred
        next_level = current_level + 1
        xp_needed = self.calculate_xp_for_level(next_level)

        if self.player_data["skills"][skill]["xp"] >= xp_needed:
            self.player_data["skills"][skill]["level"] = next_level
            return True  # Indicates a level up

        return False

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

    def change_activity(self, new_activity):
        # Clear all UI before changing
        button_manager.clear_and_reset()
        selection_list_manager.clear_and_reset()
        panel_manager.clear_and_reset()

        # Then proceed with the activity change
        if hasattr(self, 'current_activity'):
            self.current_activity = new_activity
        else:
            self.current_activity_state = new_activity
        self.states[new_activity].reset()
        self.states[new_activity].create_ui()

    def run(self):
        self.running = True
        try:
            while self.running:
                # Get time delta - limit to reasonable values in case of lag
                time_delta = self.clock.tick(60) / 1000

                # Process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    # Add ESC key to exit the game
                    if event.type == pygame.KEYDOWN:
                        if self.current_state == "play":
                            if event.key == pygame.K_ESCAPE:
                                self.change_state("menu")
                        if self.current_state == "saveload":
                            if event.key == pygame.K_ESCAPE:
                                self.change_state("menu")

                    # Pass events to the UI managers
                    button_manager.process_events(event)
                    selection_list_manager.process_events(event)
                    panel_manager.process_events(event)

                    # Let current state handle events
                    self.current_state.handle_event(event)

                # Update
                button_manager.update(time_delta)
                selection_list_manager.update(time_delta)
                panel_manager.update(time_delta)
                self.current_state.update(time_delta)

                # Draw
                self.screen.fill((0, 0, 0))  # Clear screen
                self.current_state.draw()
                button_manager.draw_ui(self.screen)
                selection_list_manager.draw_ui(self.screen)
                panel_manager.draw_ui(self.screen)

                pygame.display.flip()  # Update the display

        except KeyboardInterrupt:
            print("Game interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"Error in game loop: {e}")
        finally:
            self.quit()

    def quit(self):
        # Perform any necessary cleanup
        try:
            print("Shutting down game...")
            pygame.mixer.quit()  # Clean up mixer if used
            pygame.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        sys.exit()


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        pygame.quit()
        sys.exit(1)
