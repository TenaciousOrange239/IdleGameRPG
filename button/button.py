import pygame
import sys

class Button:
    def __init__(self, image, x_pos, y_pos, txt_input, base_colour, hovering_colour, font_name=None, font_size=50):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.base_colour = base_colour
        self.hovering_colour = hovering_colour
        self.txt_input = txt_input
        self.font_name = font_name
        self.font_size = font_size
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.txt = self.font.render(self.txt_input, True, base_colour)
        self.txt_rect = self.txt.get_rect(center=(self.x_pos, self.y_pos))
        if self.image is None:
            self.image = self.txt

    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.txt, self.txt_rect)

    def checkforInput(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    def changeColour(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.txt = self.font.render(self.txt_input,True,self.hovering_colour)
        else:
            self.txt = self.font.render(self.txt_input,True,self.base_colour)

    def set_font_size(self, new_size):
        self.font_size = new_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Button")

    button_surface = pygame.image.load("images/bh.png")
    button_surface = pygame.transform.scale(button_surface, (400,150))

    button = Button(button_surface, 400, 300, "Click", "white", "green", "arial", 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.checkforInput(pygame.mouse.get_pos())

        button.update()
        button.changeColour(pygame.mouse.get_pos())
        pygame.display.update()

