import os

import pygame
import pygame_gui

from .config import button_manager, selection_list_manager, panel_manager


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
        self.title_rect = self.title_surf.get_rect(center=(640, 150))

        # Play button
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 275), (230, 100)), text='PLAY',
                                                        manager=button_manager)

        # Options button
        self.options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 400), (230, 100)),
                                                           text='OPTIONS', manager=button_manager)

        # Quit button
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 525), (230, 100)), text='QUIT',
                                                        manager=button_manager)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.game.change_state("play")
            elif event.ui_element == self.options_button:
                self.game.change_state("options")
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


class Play(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 50)
        self.selection_list = None
        self.back_button = None
        self.ui_created = False  # Track if UI has been created
        self.load_assets()

    def reset(self):
        button_manager.clear_and_reset()
        selection_list_manager.clear_and_reset()
        self.ui_created = False
        self.create_ui()

    def load_assets(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "resources", "images", "lake.png")

        # Load background (this happens on init)
        self.bg = pygame.image.load(bg_path).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1280, 720))

    def create_ui(self):
        item_list = ["Combat", "", "Mining", "Smithing", "Hunting", "Woodcutting", "Cooking", "Magic"]
        select_list_rect = pygame.Rect(-1, 101, 200, 620)
        self.selection_list = pygame_gui.elements.UISelectionList(
            relative_rect=select_list_rect,
            item_list=item_list,
            manager=selection_list_manager,
            object_id=pygame_gui.core.ObjectID(class_id="@button", object_id="#unique_button")
        )

        self.ui_created = True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selection_list_manager.clear_and_reset()
                button_manager.clear_and_reset()
                self.game.change_state("menu")

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if hasattr(self, 'back_button') and event.ui_element == self.back_button:
                selection_list_manager.clear_and_reset()
                button_manager.clear_and_reset()
                self.game.change_state("menu")

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if hasattr(self, 'selection_list') and event.ui_element == self.selection_list:
                print(f"Selected: {event.text}")

                activity_map = {
                    "Combat": "combat",
                    "Mining": "mining",
                    "Smithing": "smithing",
                    "Hunting": "hunting",
                    "Woodcutting": "woodcutting",
                    "Cooking": "cooking",
                    "Magic": "magic"
                }

                selected_activity = activity_map.get(event.text)
                if selected_activity:
                    # Use change_activity instead of change_state
                    self.game.change_activity(selected_activity)

    def update(self, time_delta):
        pass

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        button_manager.draw_ui(self.screen)
        selection_list_manager.draw_ui(self.screen)
        panel_manager.draw_ui(self.screen)


class Mining(Play):
    def __init__(self, game):
        super().__init__(game)
        self.m_button_1 = None
        self.ore_buttons = []
        self.ore_button_manager = pygame_gui.UIManager((1280, 720), "ore_button_theme.json")
        self.mining_in_progress = {}  # Track which ores are being mined
        self.mining_progress = {}  # Track progress for each ore (0-100%)
        self.placeholder_icon = None  # Will hold the placeholder ore icon

    def create_ui(self):
        super().create_ui()

        # Properly clear any existing ore buttons - don't try to kill dictionaries
        self.ore_buttons = []  # Simply reset the list instead of trying to kill each element

        # Reset mining progress
        self.mining_in_progress = {}
        self.mining_progress = {}

        # Load placeholder icon (or create a simple surface if no image available)
        try:
            self.placeholder_icon = pygame.Surface((32, 32))
            self.placeholder_icon.fill((100, 100, 100))  # Gray background
            pygame.draw.circle(self.placeholder_icon, (200, 200, 200), (16, 16), 12)  # Light gray circle
            pygame.draw.circle(self.placeholder_icon, (150, 150, 150), (16, 16), 8)  # Medium gray inner circle
        except Exception as e:
            print(f"Could not create placeholder icon: {e}")

        # Get the ores from the game's activity_data
        ores_data = self.game.activity_data.get("mining", {}).get("ores_mined", {})
        ore_names = list(ores_data.keys())

        # If no ores found, use an empty list to avoid errors
        if not ore_names:
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
        for i, ore_name in enumerate(ore_names):
            row = i // grid_cols
            col = i % grid_cols

            x_pos = start_x + col * (button_width + padding)
            y_pos = start_y + row * (button_height + padding)

            # Create a custom button but don't use pygame_gui's button for this
            # Instead, track the rect and we'll draw our own custom button
            button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)

            # Initialize progress for this ore
            self.mining_progress[ore_name] = 0
            self.mining_in_progress[ore_name] = False

            # Store button info
            self.ore_buttons.append({
                'rect': button_rect,
                'name': ore_name,
                'hovered': False,
                'xp_reward': 5 + i * 2  # Example XP reward based on ore index (can be customized)
            })

    def handle_event(self, event):
        super().handle_event(event)

        self.ore_button_manager.process_events(event)

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()

            for button in self.ore_buttons:
                if button['rect'].collidepoint(mouse_pos):
                    ore_name = button['name']
                    # Toggle mining status
                    self.mining_in_progress[ore_name] = not self.mining_in_progress[ore_name]

                    if self.mining_in_progress[ore_name]:
                        print(f"Started mining {ore_name}...")
                        # Reset progress when starting
                        self.mining_progress[ore_name] = 0
                    else:
                        print(f"Stopped mining {ore_name}.")

    def update(self, time_delta):
        super().update(time_delta)
        self.ore_button_manager.update(time_delta)

        # Update mining progress for active ores
        for ore_name, is_mining in self.mining_in_progress.items():
            if is_mining:
                # Increase progress by a small amount
                self.mining_progress[ore_name] += 25 * time_delta  # Adjust speed as needed

                # If completed a mining cycle
                if self.mining_progress[ore_name] >= 100:
                    # Reset progress and process the mined ore
                    self.mining_progress[ore_name] = 0
                    print(f"Successfully mined {ore_name}!")
                    # Here you would typically add the ore to inventory
                    # And award XP (but we're just showing the UI for now)

        # Apply hover effects for buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.ore_buttons:
            button['hovered'] = button['rect'].collidepoint(mouse_pos)

    def draw(self):
        super().draw()

        # Title
        font_large = pygame.font.SysFont(self.font_name, 36)
        title = font_large.render("Mining", True, (255, 255, 255))
        self.game.screen.blit(title, ((self.game.screen.get_width() - title.get_width()) // 2, 100))

        # Draw custom buttons with progress bars
        font = pygame.font.SysFont(self.font_name, 22)
        small_font = pygame.font.SysFont(self.font_name, 16)

        for button in self.ore_buttons:
            rect = button['rect']
            name = button['name']
            xp_reward = button['xp_reward']
            is_mining = self.mining_in_progress.get(name, False)
            progress = self.mining_progress.get(name, 0)

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





class Combat(Play):
    def __init__(self, game):
        super().__init__(game)


class Smithing(Play):
    def __init__(self, game):
        super().__init__(game)


class Hunting(Play):
    def __init__(self, game):
        super().__init__(game)


class Woodcutting(Play):
    def __init__(self, game):
        super().__init__(game)


class Cooking(Play):
    def __init__(self, game):
        super().__init__(game)


class Magic(Play):
    def __init__(self, game):
        super().__init__(game)


class Options(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("arial", 50)
        self.load_assets()

    def load_assets(self):
        # Load game assets here
        pass

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")

    def update(self, time_delta):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Options Screen - Press ESC to return to menu", True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        button_manager.draw_ui(self.screen)
        selection_list_manager.draw_ui(self.screen)
