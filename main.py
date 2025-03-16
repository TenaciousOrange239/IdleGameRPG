import os
from sys import displayhook

import pygame
import time

pygame.init()

rect_color = (255,0,0)

canvas = pygame.display.set_mode((1280,720), pygame.RESIZABLE)

pygame.display.set_caption("Lol")
image = pygame.image.load("bh.png")

leave = False

while not leave:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leave = True

    pygame.display.update()

    canvas.blit(image,(0,0))
    pygame.display.flip()

