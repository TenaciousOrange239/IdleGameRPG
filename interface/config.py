import pygame_gui

manager = pygame_gui.UIManager((1280, 720), theme_path="button_theme.json", enable_live_theme_updates=True)
manager.preload_fonts([{'name': 'arial', 'point_size': 14, 'style': 'regular'}])