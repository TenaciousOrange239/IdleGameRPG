import pygame_gui
import os
import pygame
import sys

# Initialize pygame first
pygame.init()

# Get the absolute path to the theme file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
button_theme_path = os.path.join(base_dir, "interface", "button_theme.json")
selection_list_theme_path = os.path.join(base_dir, "interface", "selection_list_theme.json")

# Create a simple UI manager without a theme initially
button_manager = pygame_gui.UIManager((1280, 720),"button_theme.json")
selection_list_manager = pygame_gui.UIManager((1280,720),"selection_list_theme.json")
panel_manager = pygame_gui.UIManager((1280,720), "panel_theme.json")
ore_button_manager = pygame_gui.UIManager((1280, 720), "ore_button_theme.json")


# Override the default font with a system font
available_fonts = pygame.font.get_fonts()
if 'arial' in available_fonts:
    default_font = 'arial'
elif len(available_fonts) > 0:
    default_font = available_fonts[0]
else:
    print("No system fonts available!")
    pygame.quit()
    sys.exit()

# Now try to load the theme
try:
    button_manager.get_theme().load_theme(button_theme_path)
    selection_list_manager.get_theme().load_theme(selection_list_theme_path)
except Exception as e:
    print(f"Warning: Could not load themes: {e}")
    print("Continuing with default theme")

# Preload the font we know exists
button_manager.preload_fonts([{'name': default_font, 'point_size': 14, 'style': 'regular'},
                       {'name': default_font, 'point_size': 50, 'style': 'regular'},
                       {'name': default_font, 'point_size': 100, 'style': 'regular'}])