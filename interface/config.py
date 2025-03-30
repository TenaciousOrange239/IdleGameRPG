import pygame_gui
import os
import pygame
import sys

# Initialize pygame first
pygame.init()

# Get the absolute path to the theme file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
theme_path = os.path.join(base_dir, "interface", "button_theme.json")

# Create a simple UI manager without a theme initially
manager = pygame_gui.UIManager((1280, 720))

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
    manager.get_theme().load_theme(theme_path)
except Exception as e:
    print(f"Warning: Could not load theme: {e}")
    print("Continuing with default theme")

# Preload the font we know exists
manager.preload_fonts([{'name': default_font, 'point_size': 14, 'style': 'regular'},
                       {'name': default_font, 'point_size': 50, 'style': 'regular'},
                       {'name': default_font, 'point_size': 100, 'style': 'regular'}])