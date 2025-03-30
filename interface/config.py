import pygame_gui
import os

# Get the absolute path to the theme file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
theme_path = os.path.join(base_dir, "interface", "button_theme.json")

manager = pygame_gui.UIManager((1280, 720),theme_path=theme_path,enable_live_theme_updates=True)
manager.preload_fonts([{'name': 'arial', 'point_size': 14, 'style': 'regular'}])