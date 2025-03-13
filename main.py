import os
import pygame
import time

pygame.init()

canvas = pygame.display.set_mode((1280,720))

pygame.display.set_caption("Lol")
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()

