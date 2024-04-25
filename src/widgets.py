import pygame as pg


class Button:
    def __init__(self, surface, size: list, pos: list):
        self.surface = surface

        self.size: list = size
        self.pos: list = pos
        self.color: tuple = (255, 255, 255)
        self.text: str = ""
        self.clickable: bool = True
        self.textAlignment: str = ""  # e, n, s, w, c

        self.buttonRect = pg.Rect(*self.size, *self.pos)

        self.prioritize_texture_size: bool = False
        self.defaultTexture = pg.image.load("../textures/test/NO_TEXTURE.png")
        self.buttonTexture = self.defaultTexture
        self.set_texture("../textures/test/NO_TEXTURE.png", scale_by=self.size)

    def draw(self, with_texture: bool = False):
        pg.draw.rect(self.surface, self.color, self.buttonRect)

        if with_texture:
            self.surface.blit(self.buttonTexture, self.pos)

    def on_click(self):
        print("hej med dig")

    def set_texture(self, texture_path: str, linear_scaling: bool = False, scale_by=None):
        # tager en texture.
        # scaler til at passe med knappens størrelse
        # placér samme sted som knap
        self.buttonTexture = pg.image.load(texture_path)

        if scale_by is None:
            scale_by = self.size

        if linear_scaling:
            self.buttonTexture = pg.transform.scale_by(self.buttonTexture, scale_by)
        else:
            self.buttonTexture = pg.transform.scale(self.buttonTexture, scale_by)

    def remove_texture(self):
        self.buttonTexture = self.defaultTexture
