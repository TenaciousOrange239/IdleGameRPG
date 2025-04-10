import os
import json
import pygame
import pygame_gui
import datetime
import random

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .config import button_manager, selection_list_manager, panel_manager
from resources.enemy import *


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

    def handle_event(self, event):
        # Handle a single event
        pass

    def handle_events(self):
        # This method is kept for backward compatibility
        # but should be avoided in new code
        for event in pygame.event.get():
            self.handle_event(event)

    def update(self, time_delta):
        button_manager.update(time_delta)
        selection_list_manager.update(time_delta)

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
        self.title_rect = self.title_surf.get_rect(center=(640, 100))

        # Button size and spacing
        button_width = 230
        button_height = 100
        button_spacing = 25
        start_y = 200

        # Play button
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((525, start_y), (button_width, button_height)),
            text='PLAY',
            manager=button_manager
        )

        # Save/Load button
        self.saveload_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((525, start_y + button_height + button_spacing), (button_width, button_height)),
            text='SAVE/LOAD',
            manager=button_manager
        )

        # Quit button
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((525, start_y + 2 * (button_height + button_spacing)),
                                      (button_width, button_height)),
            text='QUIT',
            manager=button_manager
        )

    def handle_event(self, event):
        # Process events for the button manager
        button_manager.process_events(event)

        if event.type == pygame.QUIT:
            self.game.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.game.change_state("play")
            elif event.ui_element == self.saveload_button:
                self.game.change_state("saveload")
            elif event.ui_element == self.quit_button:
                self.game.quit()

    def update(self, time_delta):
        pass

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.screen, (26, 29, 37), self.title_rect, 0, 25)
        self.screen.blit(self.title_surf, self.title_rect)
        button_manager.draw_ui(self.screen)
        selection_list_manager.draw_ui(self.screen)
        pygame.display.flip()

class Play(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Initialize the UI manager
        self.manager = pygame_gui.UIManager((1280, 720))
        self.activity_buttons = {}
        self.ui_created = False
        self.font = pygame.font.Font(None, 36)
        # Load assets immediately
        self.load_assets()
        # Create UI immediately
        self.create_ui()

    def reset(self):
        # Clear and reset UI elements
        self.ui_created = False
        # Create a new UI manager to clear previous elements
        self.manager = pygame_gui.UIManager((1280, 720))
        button_manager.clear_and_reset()
        panel_manager.clear_and_reset()
        # Recreate UI elements
        self.create_ui()

    def load_assets(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "resources", "images", "lake.png")

        # Load background
        try:
            self.bg = pygame.image.load(bg_path).convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (1280, 720))
        except FileNotFoundError:
            print(f"Error: Could not load background image at {bg_path}")
            # Create a fallback background
            self.bg = pygame.Surface((1280, 720))
            self.bg.fill((50, 50, 100))  # Dark blue fallback

    def create_ui(self):
        # Create a panel to contain the activity buttons
        panel_width = 300
        panel_height = 500
        panel_x = 490  # Centered
        panel_y = 110  # Below title

        # Create the panel
        self.activity_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.manager,
            starting_height = 1
        )

        # Panel title
        self.panel_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 10, panel_width, 40),
            text="Choose an Activity",
            manager=self.manager,
            container=self.activity_panel
        )

        # Define activity buttons inside the panel
        button_width = 250
        button_height = 50
        button_x = 25  # Centered in panel
        initial_y = 60  # Below title
        padding = 20

        # Define activity buttons
        activities = ["inventory", "combat", "mining", "smithing", "woodcutting"]
        self.activity_buttons = {}

        # Create a button for each activity
        for i, activity in enumerate(activities):
            button_y = initial_y + (button_height + padding) * i
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            self.activity_buttons[activity] = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=activity,
                manager=self.manager,
                container=self.activity_panel
            )

        # Back button (outside the panel)
        back_button_rect = pygame.Rect(10, 650, 180, 50)
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=back_button_rect,
            text="Back to Menu",
            manager=self.manager
        )

        self.ui_created = True

    def handle_event(self, event):
        # Process events for the UI manager
        super().handle_event(event)
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Handle back button
                if event.ui_element == self.back_button:
                    self.game.change_state('menu')
                    return

                # Check if the button is one of the activity buttons
                for activity, button in self.activity_buttons.items():
                    if event.ui_element == button:
                        # Directly create and show the activity class
                        if activity == 'mining':
                            # Create Mining instance and set it as current state
                            mining_screen = Mining(self.game)
                            self.game.states['mining'] = mining_screen
                            self.game.change_state('mining')
                            self.reset()
                        elif activity == 'woodcutting':
                            # Create Mining instance and set it as current state
                            mining_screen = Woodcutting(self.game)
                            self.game.states['woodcutting'] = mining_screen
                            self.game.change_state('woodcutting')
                            self.reset()
                        elif activity == 'combat':
                            # Create Combat instance and set it as current state
                            combat_screen = Combat(self.game)
                            self.game.states['combat'] = combat_screen
                            self.game.change_state('combat')
                            self.reset()
                        elif activity == 'inventory':
                            # Create Inventory instance and set it as current state
                            inventory_screen = Inventory(self.game)
                            self.game.states['inventory'] = inventory_screen
                            self.game.change_state('inventory')
                            self.reset()
                        # Add other activities as needed
                        return



        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.reset()
                    self.game.change_state("menu")


    def update(self, dt):
        # Update the UI manager with delta time
        self.manager.update(dt)

        # Create UI if not already created
        if not self.ui_created:
            self.create_ui()

    def draw(self):
        # Draw background
        self.screen.blit(self.bg, (0, 0))

        # Draw UI elements
        self.manager.draw_ui(self.screen)


class Mining(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.ore_buttons = []
        self.ore_button_manager = pygame_gui.UIManager((1280, 720), "ore_button_theme.json")
        self.mining_in_progress = {}  # Track which ores are being mined
        self.mining_progress = {}  # Track progress for each ore (0-100%)
        self.placeholder_icon = None
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "resources", "images", "lake.png")
        self.bg = pygame.image.load(bg_path).convert_alpha()
        # Will hold the placeholder ore icon

        # Define ores with their level requirements and XP rewards
        self.ores = {
            "Copper": {"required_level": 1, "xp_reward": 5, "mining_time": 3, "color": (184, 115, 51)},
            "Iron": {"required_level": 5, "xp_reward": 10, "mining_time": 5, "color": (136, 136, 136)},
            "Steel": {"required_level": 10, "xp_reward": 15, "mining_time": 7, "color": (176, 196, 222)},
            "Tungsten": {"required_level": 15, "xp_reward": 25, "mining_time": 10, "color": (50, 50, 50)},
            "Titanium": {"required_level": 20, "xp_reward": 40, "mining_time": 15, "color": (211, 211, 211)},
            "Goatium": {"required_level": 30, "xp_reward": 70, "mining_time": 20, "color": (244, 164, 96)},
            "Infinium": {"required_level": 50, "xp_reward": 120, "mining_time": 30, "color": (70, 130, 180)}
        }

        self.current_ore = None
        self.xp_bar_rect = pygame.Rect(50, 650, 400, 20)
        self.level_text_rect = pygame.Rect(50, 625, 400, 20)

    def reset(self):
        self.ore_button_manager.clear_and_reset()
        self.create_ui()

    def create_ui(self):
        self.ore_button_manager.clear_and_reset()
        self.ore_buttons = []

        self.screen.blit(self.bg, (0, 0))

        # Load placeholder icon
        try:
            self.placeholder_icon = pygame.Surface((32, 32))
            self.placeholder_icon.fill((100, 100, 100))
            pygame.draw.circle(self.placeholder_icon, (200, 200, 200), (16, 16), 12)
            pygame.draw.circle(self.placeholder_icon, (150, 150, 150), (16, 16), 8)
        except Exception as e:
            print(f"Could not create placeholder icon: {e}")

        # Add back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (100, 40)),
            text="Back",
            manager=self.ore_button_manager,
        )

        # Add ore buttons
        button_width = 280
        button_height = 120
        grid_cols = 3
        padding = 30
        start_x = ((self.game.screen.get_width() - (grid_cols * button_width + (grid_cols - 1) * padding)) // 2)
        start_y = 180

        for i, (ore_name, ore_data) in enumerate(self.ores.items()):
            row = i // grid_cols
            col = i % grid_cols

            x_pos = start_x + col * (button_width + padding)
            y_pos = start_y + row * (button_height + padding)

            button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=f"{ore_name}\n(Level {ore_data['required_level']})",
                manager=self.ore_button_manager,
                object_id=pygame_gui.core.ObjectID(class_id='@ore_buttons', object_id=ore_name)
            )
            self.ore_buttons.append(button)
            self.mining_progress[ore_name] = 0
            self.mining_in_progress[ore_name] = False

    def handle_event(self, event):

        if not hasattr(self, 'back_button') or self.back_button is None:
            # If the button doesn't exist, recreate the UI
            self.create_ui()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset()
                self.game.change_state("play")

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.game.change_state("play")

            else:
                for button in self.ore_buttons:
                    if event.ui_element == button:
                        ore_name = button.object_id.object_id
                        required_level = self.ores[ore_name]["required_level"]
                        current_level = self.game.player_data["skills"]["mining"]["level"]

                        if current_level >= required_level:
                            self.mining_in_progress[ore_name] = not self.mining_in_progress[ore_name]
                            if self.mining_in_progress[ore_name]:
                                self.mining_progress[ore_name] = 0
                                self.current_ore = ore_name
                                print(f"Started mining {ore_name}")
                            else:
                                print(f"Stopped mining {ore_name}")
                        else:
                            print(f"You need mining level {required_level} to mine {ore_name}")

    def update(self, time_delta):
        super().update(time_delta)
        self.ore_button_manager.update(time_delta)

        for ore_name, is_mining in self.mining_in_progress.items():
            if is_mining:
                ore_data = self.ores[ore_name]
                mining_time = ore_data["mining_time"]
                level_bonus = 1.0 + (self.game.player_data["skills"]["mining"]["level"] * 0.01)
                self.mining_progress[ore_name] += time_delta * level_bonus

                if self.mining_progress[ore_name] >= mining_time:
                    if ore_name not in self.game.player_data["inventory"]["ores"]:
                        self.game.player_data["inventory"]["ores"][ore_name] = 0
                    self.game.player_data["inventory"]["ores"][ore_name] += 1

                    if "mining" not in self.game.activity_data:
                        self.game.activity_data["mining"] = {"ores_mined": {}}
                    if "ores_mined" not in self.game.activity_data["mining"]:
                        self.game.activity_data["mining"]["ores_mined"] = {}
                    if ore_name not in self.game.activity_data["mining"]["ores_mined"]:
                        self.game.activity_data["mining"]["ores_mined"][ore_name] = 0
                    self.game.activity_data["mining"]["ores_mined"][ore_name] += 1

                    xp_reward = ore_data["xp_reward"]
                    self.game.add_skill_xp("mining", xp_reward)
                    self.mining_progress[ore_name] = 0

    def draw(self):
        super().draw()
        self.ore_button_manager.draw_ui(self.game.screen)


class Inventory(Play):
    def __init__(self, game):
        super().__init__(game)


class Combat(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.enemy = None
        self.enemy_list = []
        self.combat_in_progress = False
        self.player_attack_timer = 0
        self.player_attack_cooldown = 2.0  # Attack every 2 seconds
        self.enemy_attack_timer = 0
        self.enemy_attack_cooldown = 3.0  # Enemy attacks every 3 seconds
        self.combat_log = []  # Store combat messages
        self.max_log_entries = 8
        self.combat_manager = pygame_gui.UIManager((1280, 720), "combat_theme.json")
        self.attack_button = None
        self.retreat_button = None
        self.enemy_select_dropdown = None
        self.enemy_buttons = []
        self.ui_created = False

        self.message_timers = {}  # Track when messages should disappear
        self.message_duration = 3.0  # Messages last for 3 seconds

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "resources", "images", "rock.png")
        self.bg = pygame.image.load(bg_path).convert_alpha()

        # Initialize Combat skills if not present
        if "combat" not in self.game.player_data["skills"]:
            self.game.player_data["skills"]["combat"] = {
                "level": 1,
                "xp": 0
            }

        # Ensure player has combat stats
        if "combat_stats" not in self.game.player_data:
            self.game.player_data["combat_stats"] = {
                "max_hp": 100,
                "current_hp": 100,
                "attack": 10,
                "defense": 5,
                "accuracy": 70,  # Percentage chance to hit
                "dodge": 10  # Percentage chance to dodge
            }

        # Load enemy classes
        self.load_enemies()

    def reset(self):
        button_manager.clear_and_reset()
        panel_manager.clear_and_reset()  # Also reset panels if you use them
        # Reset any Mining-specific state variables here
        self.create_ui()  # Assuming you have this method to set up Mining UI

    def load_enemies(self):
        # Create a dictionary mapping names to enemy classes for easy instantiation
        self.enemy_classes = {
            "Chicken": Chicken,
            "Cow": Cow,
            "Boar": Boar,
            "Bear": Bear,
            "Great Bear": GreatBear,
            "Withered Husk": WitheredHusk,
            "Lone Wanderer": LoneWanderer,
            "Cursed Bandit": CursedBandit,
            "Cursed Elite Bandit": CursedEliteBandit,
            "Legondas, The Undead Bandit": LegrondasTheUndeadBandit,
            "Giant Leech": GiantLeech,
            "Foul Specter": FoulSpecter,
            "Bog Lurker": BogLurker,
            "Fetid Witch": FetidWitch,
            "The Grotesque Basilisk": TheGrotesqueBasilisk,
            "Servant Of The Blood": ServantOfTheBlood,
            "Bloodstained Soldier": BloodstainedSoldier,
            "Hemomancer": Hemomancer,
            "Crimson Knight": CrimsonKnight,
            "The Sanguine Lord": TheSanguineLord,
            "Shadow Swarmed Golem": ShadowSwarmedGolem,
            "Deathsworn Behemoth": DeathswornBehemoth,
            "Corrupted Wraith": CorruptedWraith,
            "Darkened Drake": DarkenedDrake,
            "Raviolios Protector Of The City": RavioliosProtectorOfTheCity,
            "Voidbound Knight": VoidboundKnight,
            "Void Stalker": VoidStalker,
            "Archmage Revenant": ArchmageRevenant,
            "Legion Of Darkness": LegionOfDarkness,
            "Yao Yao, Touched By The Void": YaoYaoTouchedByTheVoid,
            "Aeneas, Darkness Absolute": AeneasDarknessAbsolute
        }

        # Group enemies by area/difficulty for UI organization
        self.enemy_areas = {
            "The Village": ["Chicken", "Cow", "Boar", "Bear", "Great Bear"],
            "Withered Plains": ["Withered Husk", "Lone Wanderer", "Cursed Bandit", "Cursed Elite Bandit", "Legrondas, The Undead Bandit"],
            "The Swamp": ["Giant Leech", "Foul Specter", "Bog Lurker", "Fetid Witch", "The Grotesque Basilisk"],
            "Lords Manor": ["Servant Of The Blood", "Bloodstained Soldier", "Hemomancer", "Crimson Knight", "The Sanguine Lord"],
            "Corrupted Highlands": ["Shadow Swarmed Golem", "Deathsworn Behemoth", "Corrupted Wraith", "Darkened Drake", "Raviolios, Protector Of The City"],
            "City Of Lucretia": ["Voidbound Knight", "Void Stalker", "Archmage Revenant", "Legion Of Darkness", "Yao Yao Touched By The Void"],
            "The Palace": ["Aeneas, Darkness Absolute"]
        }

    def create_ui(self):

        self.screen.blit(pygame.transform.scale(self.bg, self.screen.get_size()), (0, 0))

        # Create combat UI elements
        button_width = 200
        button_height = 50

        button_manager.clear_and_reset()
        selection_list_manager.clear_and_reset()
        panel_manager.clear_and_reset()

        # Retreat button
        self.retreat_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((760, 600), (button_width, button_height)),
            text="Retreat",
            manager=self.combat_manager
        )

        # Area selection dropdown (for organizing enemies)
        self.area_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=list(self.enemy_areas.keys()),
            starting_option=list(self.enemy_areas.keys())[0],
            relative_rect=pygame.Rect((50, 50), (200, 30)),
            manager=self.combat_manager
        )

        # Create enemy selection buttons
        self.create_enemy_buttons(list(self.enemy_areas.keys())[0])

        self.ui_created = True

    def create_enemy_buttons(self, area):
        # Clear existing buttons
        if hasattr(self, 'enemy_buttons'):
            for button in self.enemy_buttons:
                button.kill()

        self.enemy_buttons = []

        # Make sure we're using a string, not a tuple
        if isinstance(area, tuple):
            area = area[0]

        # Create new buttons for enemies in this area
        if area in self.enemy_areas:
            enemies = self.enemy_areas[area]
            button_width = 200
            button_height = 40
            start_x = 50
            start_y = 100

            for i, enemy in enumerate(enemies):
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((start_x, start_y + i * (button_height + 10)),
                                              (button_width, button_height)),
                    text=enemy,
                    manager=self.combat_manager
                )
                self.enemy_buttons.append(button)


    def spawn_enemy(self, enemy_name):
        # Create an instance of the selected enemy
        if enemy_name in self.enemy_classes:
            self.enemy = self.enemy_classes[enemy_name]()
            self.combat_in_progress = True
            self.add_combat_log(f"You encounter a {enemy_name}!")

            # Reset combat timers
            self.player_attack_timer = 0
            self.enemy_attack_timer = 0

    def player_attack(self):
        if not self.enemy:
            return

        # Calculate hit chance based on player accuracy and enemy dodge
        hit_chance = self.game.player_data["combat_stats"]["accuracy"] - self.enemy.dodge_chance
        hit_chance = max(10, min(90, hit_chance))  # Clamp between 10% and 90%

        if random.randint(1, 100) <= hit_chance:
            # Calculate damage based on player attack and enemy defense
            base_damage = self.game.player_data["combat_stats"]["attack"]
            damage_reduction = self.enemy.defence / (self.enemy.defence + 50)  # Defense formula
            damage = max(1, int(base_damage * (1 - damage_reduction)))

            # Apply damage
            self.enemy.take_dmg(damage)
            self.add_combat_log(f"You hit the {self.enemy.name} for {damage} damage!")

            # Check if enemy is defeated
            if self.enemy.hp <= 0:
                self.enemy_defeated()
        else:
            self.add_combat_log(f"You missed the {self.enemy.name}!")

    def enemy_attack(self):
        if not self.enemy or self.enemy.hp <= 0:
            return

        # Calculate hit chance
        dodge_chance = self.game.player_data["combat_stats"]["dodge"]
        hit_chance = 100 - dodge_chance

        if random.randint(1, 100) <= hit_chance:
            # Calculate damage
            base_damage = self.enemy.ATK
            defense = self.game.player_data["combat_stats"]["defense"]
            damage_reduction = defense / (defense + 50)
            damage = max(1, int(base_damage * (1 - damage_reduction)))

            # Apply damage to player
            self.game.player_data["combat_stats"]["current_hp"] -= damage
            self.add_combat_log(f"The {self.enemy.name} hits you for {damage} damage!")

            # Check if player is defeated
            if self.game.player_data["combat_stats"]["current_hp"] <= 0:
                self.game.player_data["combat_stats"]["current_hp"] = 0
                self.player_defeated()
        else:
            self.add_combat_log(f"You dodge the {self.enemy.name}'s attack!")

    def enemy_defeated(self):
        # Get rewards from defeated enemy
        gold = self.enemy.gold_drop
        xp = self.enemy.xp_drop

        # Add rewards to player
        self.game.player_data["gold"] += gold
        level_up = self.game.add_skill_xp("combat", xp)

        # Add loot items to inventory
        for item, chance in self.enemy.loot.items():
            if random.random() * 100 <= chance:
                if item not in self.game.player_data["inventory"]:
                    self.game.player_data["inventory"][item] = 0
                self.game.player_data["inventory"][item] += 1
                self.add_combat_log(f"You found: {item}")

        # Add combat log entries
        self.add_combat_log(f"You defeated the {self.enemy.name}!")
        self.add_combat_log(f"You gained {gold} gold and {xp} combat XP!")

        if level_up:
            new_level = self.game.player_data["skills"]["combat"]["level"]
            self.add_combat_log(f"Combat level up! Now level {new_level}!")

        # End combat
        self.combat_in_progress = False
        self.enemy = None

    def player_defeated(self):
        self.add_combat_log("You have been defeated!")

        # Implement death penalty (e.g., lose some gold, return to a safe area)
        gold_loss = int(self.game.player_data["gold"] * 0.1)  # Lose 10% of gold
        self.game.player_data["gold"] -= gold_loss
        self.add_combat_log(f"You lost {gold_loss} gold.")

        # Restore some health
        self.game.player_data["combat_stats"]["current_hp"] = int(
            self.game.player_data["combat_stats"]["max_hp"] * 0.5)  # Restore to 50% health

        # End combat
        self.combat_in_progress = False
        self.enemy = None

    def add_combat_log(self, message):
        current_time = pygame.time.get_ticks() / 1000  # Current time in seconds
        self.combat_log.append(message)
        self.message_timers[len(self.combat_log) - 1] = current_time + self.message_duration

        # Limit the log size
        if len(self.combat_log) > self.max_log_entries:
            self.combat_log.pop(0)
            # Shift all timers down since we removed the first message
            new_timers = {}
            for idx, timer in self.message_timers.items():
                if idx > 0:  # Skip the one we're removing
                    new_timers[idx - 1] = timer
            self.message_timers = new_timers

    def handle_event(self, event):
        # Process UI events
        self.combat_manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Handle area dropdown
                if event.ui_element == self.area_dropdown:
                    selected_area = self.area_dropdown.selected_option
                    # Make sure we're using a string, not a tuple
                    if isinstance(selected_area, tuple):
                        selected_area = selected_area[0]
                    self.create_enemy_buttons(selected_area)

                # Handle enemy selection
                elif event.ui_element in self.enemy_buttons:
                    for i, button in enumerate(self.enemy_buttons):
                        if event.ui_element == button:
                            area = self.area_dropdown.selected_option
                            # Make sure we're using a string, not a tuple
                            if isinstance(area, tuple):
                                area = area[0]

                            # Safety check to ensure the area exists in enemy_areas
                            if area in self.enemy_areas and i < len(self.enemy_areas[area]):
                                enemy_name = self.enemy_areas[area][i]
                                self.start_stat_based_combat(enemy_name)
                            break

                # Handle return to area selection button (only visible after combat)
                # Changed from self.return_button to self.retreat_button
                elif event.ui_element == self.retreat_button and not self.combat_in_progress:
                    self.reset_combat_ui()

        # Handle back button to return to main menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.combat_in_progress:
                self.game.change_state("play")

    def reset_combat_ui(self):
        # Clear combat log
        self.combat_log = []

        # Hide the return button
        if hasattr(self, 'return_button'):
            self.return_button.hide()

        # Show area selection UI again
        for button in self.enemy_buttons:
            button.show()
        self.area_dropdown.show()

    def start_stat_based_combat(self, enemy_name):
        # Create an instance of the selected enemy
        if enemy_name in self.enemy_classes:
            # Initialize player stats if they don't exist
            if "combat_stats" not in self.game.player_data:
                self.game.player_data["combat_stats"] = {
                    "max_hp": 100,
                    "current_hp": 100,
                    "attack": 10 + self.game.player_data["skills"]["combat"]["level"] * 2,
                    "defense": 5 + self.game.player_data["skills"]["combat"]["level"]
                }

            # Create the enemy
            self.enemy = self.enemy_classes[enemy_name]()
            self.combat_in_progress = True

            # Log the encounter (this will now auto-disappear after 3 seconds)
            self.add_combat_log(f"You encounter a {enemy_name}!")

            # Get player stats for comparison
            player_attack = self.game.player_data["combat_stats"]["attack"]
            player_defense = self.game.player_data["combat_stats"]["defense"]

            # Get enemy stats
            enemy_attack = self.enemy.ATK
            enemy_defense = self.enemy.defence
            enemy_speed = getattr(self.enemy, "SPD", 5)  # Default to 5 if not defined

            # Log the stats comparison (these will auto-disappear)
            self.add_combat_log(f"Your Stats - ATK: {player_attack}, DEF: {player_defense}")
            self.add_combat_log(f"Enemy Stats - ATK: {enemy_attack}, DEF: {enemy_defense}, SPD: {enemy_speed}")

            # Calculate combat advantage scores (higher is better)
            player_score = (player_attack * 2) + player_defense
            enemy_score = (enemy_attack * 2) + enemy_defense + enemy_speed

            # Add some randomness (±10%)
            player_variance = random.uniform(0.9, 1.1)
            enemy_variance = random.uniform(0.9, 1.1)

            player_final_score = player_score * player_variance
            enemy_final_score = enemy_score * enemy_variance

            # Determine the winner
            if player_final_score >= enemy_final_score:
                # Player wins
                damage_taken = max(0, int((enemy_attack - player_defense * 0.5) * random.uniform(0.8, 1.2)))
                damage_taken = min(damage_taken,
                                   self.game.player_data["combat_stats"]["current_hp"] - 1)  # Prevent death

                self.game.player_data["combat_stats"]["current_hp"] -= damage_taken

                # Calculate experience gained
                xp_gained = self.enemy.XP_REWARD if hasattr(self.enemy, "XP_REWARD") else 10
                level_up = self.game.add_skill_xp("combat", xp_gained)

                # Log the results
                self.add_combat_log(f"You defeated the {enemy_name}!")
                self.add_combat_log(f"You took {damage_taken} damage in the fight.")
                self.add_combat_log(f"You gained {xp_gained} combat experience.")

                if level_up:
                    self.add_combat_log("You leveled up in combat!")

                # Check for drops
                if hasattr(self.enemy, "DROPS") and self.enemy.DROPS:
                    for item, chance in self.enemy.DROPS.items():
                        if random.random() < chance:
                            # Add item to inventory
                            # This is a placeholder - adjust based on your inventory system
                            if item not in self.game.player_data["inventory"]["equipment"]:
                                self.game.player_data["inventory"]["equipment"][item] = 0
                            self.game.player_data["inventory"]["equipment"][item] += 1
                            self.add_combat_log(f"You found: {item}")
            else:
                # Enemy wins
                damage_taken = max(1, int((enemy_attack - player_defense * 0.3) * random.uniform(0.9, 1.3)))
                damage_taken = min(damage_taken,
                                   self.game.player_data["combat_stats"]["current_hp"] - 1)  # Prevent death

                self.game.player_data["combat_stats"]["current_hp"] -= damage_taken

                # Calculate reduced experience for losing
                xp_gained = max(1, int((self.enemy.XP_REWARD if hasattr(self.enemy, "XP_REWARD") else 5) * 0.4))
                level_up = self.game.add_skill_xp("combat", xp_gained)

                # Log the results
                self.add_combat_log(f"You were defeated by the {enemy_name}!")
                self.add_combat_log(f"You took {damage_taken} damage in the fight.")
                self.add_combat_log(f"You gained {xp_gained} combat experience from the attempt.")

                if level_up:
                    self.add_combat_log("You leveled up in combat!")

            # Update HP display
            self.add_combat_log(
                f"Your HP: {self.game.player_data['combat_stats']['current_hp']}/{self.game.player_data['combat_stats']['max_hp']}")

            # Combat is now over, show the return button
            self.combat_in_progress = False
            self.show_return_button()

    def show_return_button(self):
        # Hide enemy selection UI
        for button in self.enemy_buttons:
            button.hide()
        self.area_dropdown.hide()

        # Create or show return button
        if not hasattr(self, 'return_button'):
            self.return_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() - 100),
                                          (200, 50)),
                text="Return to Areas",
                manager=self.combat_manager
            )
        else:
            self.return_button.show()

    def update(self, time_delta):
        # Update UI manager
        self.combat_manager.update(time_delta)

        # Create UI if not created yet
        if not self.ui_created:
            self.create_ui()

        current_time = pygame.time.get_ticks() / 1000
        to_remove = []
        for idx, expire_time in self.message_timers.items():
            if current_time >= expire_time and idx < len(self.combat_log):
                to_remove.append(idx)

        # Remove messages from the end first to preserve indices
        for idx in sorted(to_remove, reverse=True):
            if idx < len(self.combat_log):
                self.combat_log.pop(idx)
                # Remove the timer and adjust other timers
                new_timers = {}
                for timer_idx, timer_val in self.message_timers.items():
                    if timer_idx < idx:
                        new_timers[timer_idx] = timer_val
                    elif timer_idx > idx:
                        new_timers[timer_idx - 1] = timer_val
                self.message_timers = new_timers

        # Auto-combat logic when in combat
        if self.combat_in_progress and self.enemy and self.enemy.hp > 0:
            # Update player attack timer
            self.player_attack_timer += time_delta
            if self.player_attack_timer >= self.player_attack_cooldown:
                self.player_attack()
                self.player_attack_timer = 0

            # Update enemy attack timer
            self.enemy_attack_timer += time_delta
            if self.enemy_attack_timer >= self.enemy_attack_cooldown:
                self.enemy_attack()
                self.enemy_attack_timer = 0

        # Auto-heal when not in combat (slow regeneration)
        elif not self.combat_in_progress:
            max_hp = self.game.player_data["combat_stats"]["max_hp"]
            current_hp = self.game.player_data["combat_stats"]["current_hp"]

            if current_hp < max_hp:
                # Regenerate 1% of max HP per second
                regen_amount = max_hp * 0.01 * time_delta
                self.game.player_data["combat_stats"]["current_hp"] = min(
                    max_hp,
                    current_hp + regen_amount
                )

    def draw(self):
        # Draw UI
        self.combat_manager.draw_ui(self.screen)

        # Draw player stats
        hp = self.game.player_data["combat_stats"]["current_hp"]
        max_hp = self.game.player_data["combat_stats"]["max_hp"]
        hp_percent = hp / max_hp

        # HP bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (540, 50, 200, 30))
        # HP bar
        pygame.draw.rect(self.screen, (255, 0, 0), (540, 50, 200 * hp_percent, 30))

        # HP text
        hp_text = f"HP: {int(hp)}/{max_hp}"
        hp_surf = self.font.render(hp_text, True, (255, 255, 255))
        self.screen.blit(hp_surf, (590, 55))

        # Combat level
        level = self.game.player_data["skills"]["combat"]["level"]
        level_text = f"Combat Level: {level}"
        level_surf = self.font.render(level_text, True, (255, 255, 255))
        self.screen.blit(level_surf, (540, 20))

        # Draw enemy if in combat
        if self.combat_in_progress and self.enemy:
            # Enemy name
            name_surf = self.font.render(self.enemy.name, True, (255, 255, 255))
            self.screen.blit(name_surf, (800, 20))

            # Enemy HP bar background
            pygame.draw.rect(self.screen, (100, 100, 100), (800, 50, 200, 30))
            # Enemy HP bar
            hp_percent = max(0, self.enemy.hp / self.enemy.max_hp)
            pygame.draw.rect(self.screen, (255, 0, 0), (800, 50, 200 * hp_percent, 30))

            # Enemy HP text
            enemy_hp_text = f"HP: {self.enemy.hp}/{self.enemy.max_hp}"
            enemy_hp_surf = self.font.render(enemy_hp_text, True, (255, 255, 255))
            self.screen.blit(enemy_hp_surf, (850, 55))

            # Draw enemy image (placeholder)
            pygame.draw.rect(self.screen, (200, 200, 200), (800, 100, 200, 200))
            enemy_img_text = self.font.render("Enemy Image", True, (0, 0, 0))
            self.screen.blit(enemy_img_text, (850, 190))

        # Draw combat log
        log_y = 400
        for message in self.combat_log:
            log_surf = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(log_surf, (540, log_y))
            log_y += 25



class Smithing(Play):
    def __init__(self, game):
        super().__init__(game)


class Woodcutting(Play):
    def __init__(self, game):
        super().__init__(game)
        self.wc_button_1 = None
        self.wood_buttons = []
        self.wood_button_manager = pygame_gui.UIManager((1280, 720), "wood_button_theme.json")
        self.chopping_in_progress = {}  # Track which ores are being mined
        self.chopping_progress = {}  # Track progress for each ore (0-100%)
        self.placeholder_icon = None

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "resources", "images", "lake.png")
        self.bg = pygame.image.load(bg_path).convert_alpha()


    def create_ui(self):

        self.screen.blit(self.bg, (0, 0))

        # Properly clear any existing ore buttons - don't try to kill dictionaries
        self.wood_buttons = []  # Simply reset the list instead of trying to kill each element

        # Reset mining progress
        self.chopping_in_progress = {}
        self.chopping_progress = {}

        # Load placeholder icon (or create a simple surface if no image available)
        try:
            self.placeholder_icon = pygame.Surface((32, 32))
            self.placeholder_icon.fill((100, 100, 100))  # Gray background
            pygame.draw.circle(self.placeholder_icon, (200, 200, 200), (16, 16), 12)  # Light gray circle
            pygame.draw.circle(self.placeholder_icon, (150, 150, 150), (16, 16), 8)  # Medium gray inner circle
        except Exception as e:
            print(f"Could not create placeholder icon: {e}")

        # Get the ores from the game's activity_data
        wood_data = self.game.activity_data.get("woodcutting", {}).get("wood_chopped", {})
        wood_names = list(wood_data.keys())

        # If no ores found, use an empty list to avoid errors
        if not wood_names:
            print("Warning: No ores found in activity_data")
            return

        # Button size and grid parameters - larger to accommodate new elements
        button_width = 280
        button_height = 120
        grid_cols = 3
        padding = 30
        start_x = ((self.game.screen.get_width() - (grid_cols * button_width + (grid_cols - 1) * padding)) // 2 + 95)
        start_y = 180

        # Create a button for each ore in a grid layout
        for i, wood_name in enumerate(wood_names):
            row = i // grid_cols
            col = i % grid_cols

            x_pos = start_x + col * (button_width + padding)
            y_pos = start_y + row * (button_height + padding)

            # Create a custom button but don't use pygame_gui's button for this
            # Instead, track the rect, and we'll draw our own custom button
            button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)

            # Initialize progress for this ore
            self.chopping_progress[wood_name] = 0
            self.chopping_in_progress[wood_name] = False

            # Store button info
            self.wood_buttons.append({
                'rect': button_rect,
                'name': wood_name,
                'hovered': False,
                'xp_reward': 5 + i * 2  # Example XP reward based on ore index (can be customized)
            })

    def handle_event(self, event):

        self.wood_button_manager.process_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset()
                self.game.change_state("play")



        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()

            for button in self.wood_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    wood_name = button['name']
                    # Toggle mining status
                    self.chopping_in_progress[wood_name] = not self.chopping_in_progress[wood_name]

                    if self.chopping_in_progress[wood_name]:
                        print(f"Started mining {wood_name}...")
                        # Reset progress when starting
                        self.chopping_progress[wood_name] = 0
                    else:
                        print(f"Stopped mining {wood_name}.")

    def update(self, time_delta):
        super().update(time_delta)
        self.wood_button_manager.update(time_delta)

        # Update mining progress for active ores
        for ore_name, is_mining in self.chopping_in_progress.items():
            if is_mining:
                # Increase progress by a small amount
                self.chopping_progress[ore_name] += 25 * time_delta  # Adjust speed as needed

                # If completed a mining cycle
                if self.chopping_progress[ore_name] >= 100:
                    # Reset progress and process the mined ore
                    self.chopping_progress[ore_name] = 0
                    print(f"Successfully mined {ore_name}!")
                    # Here you would typically add the ore to inventory
                    # And award XP (but we're just showing the UI for now)

        # Apply hover effects for buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.wood_buttons:
            button['hovered'] = button['rect'].collidepoint(mouse_pos)

    def draw(self):
        super().draw()

        self.screen.blit(self.bg, (0, 0))

        # Title
        font_large = pygame.font.SysFont(self.font_name, 36)
        title = font_large.render("Mining", True, (255, 255, 255))
        self.game.screen.blit(title, ((self.game.screen.get_width() - title.get_width()) // 2, 100))

        # Draw custom buttons with progress bars
        font = pygame.font.SysFont(self.font_name, 22)
        small_font = pygame.font.SysFont(self.font_name, 16)

        for button in self.wood_buttons:
            rect = button['rect']
            name = button['name']
            xp_reward = button['xp_reward']
            is_mining = self.chopping_in_progress.get(name, False)
            progress = self.chopping_progress.get(name, 0)

            # Button background
            button_color = (70, 70, 80) if not button['hovered'] else (80, 80, 90)
            if is_mining:
                button_color = (80, 100, 80)  # Green tint when mining

            # Draw button with rounded corners
            pygame.draw.rect(self.game.screen, button_color, rect, border_radius=10)

            # Add a subtle border
            border_color = (100, 100, 110)
            pygame.draw.rect(self.game.screen, border_color, rect, width=2, border_radius=10)

            # Placeholder icon
            if self.placeholder_icon:
                icon_rect = pygame.Rect(rect.x + 15, rect.y + (rect.height - 32) // 2, 32, 32)
                self.game.screen.blit(self.placeholder_icon, icon_rect)

            # Ore name
            name_text = font.render(name, True, (230, 230, 230))
            self.game.screen.blit(name_text, (rect.x + 60, rect.y + 20))

            # XP reward
            xp_text = small_font.render(f"+{xp_reward} XP", True, (180, 220, 180))
            self.game.screen.blit(xp_text, (rect.x + 60, rect.y + 50))

            # Status text
            status_text = small_font.render("Click to " + ("stop" if is_mining else "start") + " mining",
                                            True, (200, 200, 200))
            self.game.screen.blit(status_text, (rect.x + 60, rect.y + 75))

            # Progress bar background
            progress_rect = pygame.Rect(rect.x + 10, rect.y + rect.height - 20, rect.width - 20, 10)
            pygame.draw.rect(self.game.screen, (50, 50, 50), progress_rect, border_radius=5)

            # Progress bar fill
            if progress > 0:
                fill_width = int((progress_rect.width * min(progress, 100)) / 100)
                fill_rect = pygame.Rect(progress_rect.x, progress_rect.y, fill_width, progress_rect.height)
                progress_color = (100, 200, 100) if is_mining else (150, 150, 200)
                pygame.draw.rect(self.game.screen, progress_color, fill_rect, border_radius=5)

        # Instructions
        instruction_font = pygame.font.SysFont(self.font_name, 20)
        instructions = instruction_font.render("Click on an ore to start mining. Click again to stop.",
                                               True, (200, 200, 200))
        self.game.screen.blit(instructions, (20, 50))


class SaveLoadMenu(GameState):
    def __init__(self, game):
        # Define class attributes before calling super().__init__
        self.save_slots = 3  # Number of save slots
        self.buttons = []
        self.back_button = None
        self.notification = None
        self.notification_timer = 0
        self.notification_duration = 2000  # Display notification for 2 seconds

        # Call the parent constructor
        super().__init__(game)

        # Set these after super().__init__
        self.font = pygame.font.SysFont("arial", 40)
        self.small_font = pygame.font.SysFont("arial", 20)

    def load_assets(self):
        # Don't create the UI here - just load background or other assets
        pass  # We'll create UI when needed, not at initialization

    def create_ui(self):
        # Create UI elements when specifically requested
        # This avoids creating UI elements during initialization
        # Clear existing UI elements
        button_manager.clear_and_reset()

        # Create back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 10, 100, 50),
            text="Back",
            manager=button_manager,
            object_id="#back_button"
        )

        # Create save slot buttons
        button_y = 150
        button_spacing = 100

        for i in range(1, self.save_slots + 1):
            # Save button
            save_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(400, button_y + ((i - 1) * button_spacing), 200, 70),
                text=f"Save Slot {i}",
                manager=button_manager,
                object_id=f"#save_slot_{i}"
            )

            # Load button
            load_btn = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(650, button_y + ((i - 1) * button_spacing), 200, 70),
                text=f"Load Slot {i}",
                manager=button_manager,
                object_id=f"#load_slot_{i}"
            )

            self.buttons.append((i, save_btn, load_btn))

    def reset(self):
        self.back_button = None
        self.buttons = []
        # Reset any other UI-related attributes

    def handle_event(self, event):
        # First check if it's a pygame_gui event
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.reset()  # Reset UI state
                self.game.change_state("menu")
                return

            # Process other UI button events
            for slot, save_btn, load_btn in self.buttons:
                if event.ui_element == save_btn:
                    if self.game.save_game(slot):
                        self.show_notification(f"Game saved to Slot {slot}!", (100, 255, 100))
                    else:
                        self.show_notification("Failed to save game!", (255, 100, 100))
                    return

                if event.ui_element == load_btn:
                    if self.game.load_game(slot):
                        self.show_notification(f"Game loaded from Slot {slot}!", (100, 255, 100))
                        # Reset UI for all activities after loading
                        for state_name, state in self.game.states.items():
                            if hasattr(state, 'ui_created'):
                                state.ui_created = False
                        self.game.change_state("menu")
                    else:
                        self.show_notification("Failed to load game!", (255, 100, 100))
                    return

        # Handle regular pygame events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.reset()
                self.game.change_state("menu")

    def show_notification(self, message, color):
        """Show a notification message"""
        self.notification = {
            "message": message,
            "color": color,
            "timer": pygame.time.get_ticks()
        }
        self.notification_timer = pygame.time.get_ticks()

    def update(self, time_delta):
        """Update the SaveLoadMenu state"""
        current_time = pygame.time.get_ticks()

        # Clear notification after duration
        if self.notification and current_time - self.notification_timer > self.notification_duration:
            self.notification = None

        # Update UI manager
        time_delta = self.clock.get_time() / 1000.0
        button_manager.update(time_delta)

    def draw(self):
        # Draw background
        self.screen.fill((50, 50, 70))  # Dark blue-gray background

        # Draw title
        title_text = self.font.render("Save / Load Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(640, 50))
        self.screen.blit(title_text, title_rect)

        # Draw back button - add check to avoid AttributeError
        if not self.back_button:
            # If back_button doesn't exist yet, create the UI
            self.create_ui()

        # Draw save slot info
        for slot, _, _ in self.buttons:
            # Check if save exists and show info
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
            save_path = os.path.join(save_dir, f"save_slot_{slot}.json")

            # Draw save slot status
            slot_y = 150 + ((slot - 1) * 100)
            slot_info_x = 200

            info_text = "Empty Slot"
            info_color = (150, 150, 150)

            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r') as save_file:
                        save_data = json.load(save_file)
                    timestamp = save_data.get("timestamp", "Unknown date")
                    # Format the timestamp nicely if it's ISO format
                    try:
                        dt = datetime.datetime.fromisoformat(timestamp)
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                        info_text = f"Saved: {formatted_time}"
                    except (ValueError, TypeError):
                        info_text = f"Saved: {timestamp}"
                    info_color = (255, 255, 255)
                except Exception as e:
                    info_text = "Error reading save"
                    info_color = (255, 100, 100)

            # Render slot info
            info_surf = self.small_font.render(info_text, True, info_color)
            self.screen.blit(info_surf, (slot_info_x, slot_y + 25))

        # Draw notification if active
        if self.notification:
            notification_surf = self.font.render(
                self.notification["message"], True, self.notification["color"])
            notification_rect = notification_surf.get_rect(center=(640, 650))

            # Draw a background for the notification
            bg_rect = notification_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (30, 30, 40), bg_rect, border_radius=5)
            pygame.draw.rect(self.screen, (80, 80, 100), bg_rect, width=2, border_radius=5)

            self.screen.blit(notification_surf, notification_rect)

        # Draw the UI manager elements
        button_manager.draw_ui(self.screen)