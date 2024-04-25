import pygame as pg


class Button:
    def __init__(self, surface, size: list, pos: list, color: tuple = (255, 255, 255)):
        self.surface = surface

        self.size: list = size
        self.pos: list = pos
        self.color: tuple = color
        self.text: str = ""
        self.clickable: bool = True
        self.textAlignment: str = ""  # e, n, s, w, c

        self.buttonRect = pg.Rect(*self.size, *self.pos)

    def draw_button(self):
        pg.draw.rect(self.surface, self.color, self.buttonRect)

    def on_click(self):
        print("hej med dig")