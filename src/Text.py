import pygame as pg


class Text:
    def __init__(self, text, font, size, color, x, y):
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.surface = pg.font.Font(self.font, self.size).render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
