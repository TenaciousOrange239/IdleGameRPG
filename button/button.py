import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Button")
main_font = pygame.font.SysFont("arial", 50)

class Button:
    def __init__(self, image, x_pos, y_pos, txt_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.txt = main_font.render(self.txt_input, True, "white")
        self.txt_input = txt_input
        self.txt_rect = self.txt.get_rect(center=(self.x_pos,self.y_pos))

        def update(self):
            screen.blit(self.image, self.rect)
            screen.blit(self.txt, self.txt_rect)

        def checkforInput(position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                print("Button Pressed!")

        def changeColour(position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.txt = main_font.render(self.txt_input, True, "green")
            else:
                self.txt = main_font.render(self.txt_input, True, "white")

button_surface = pygame.image.load("")
button_surface = pygame.transform.scale(button_surface, (400,150))

button = Button(button_surface, 400, 300, "Click")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.checkforInput(pygame.mouse.get_pos())




