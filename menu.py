import pygame
import sys
from pygame import RESIZABLE

pygame.init()
screen = pygame.display.set_mode((1280,720),RESIZABLE)
pygame.display.set_caption("Idle Game")
clock = pygame.time.Clock()
#pygame.display.set_icon()
game_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
