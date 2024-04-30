import pygame as pg


class Node:
    registry = []

    def __init__(self, surface, size: list = None, pos: list = None, corner_radius: int = 0,
                 z_index: int = 0, action=None):
        self.registry.append([self, z_index])
        print(self.registry)
        self.surface = surface

        if size is None:
            size = [100, 100]
        if pos is None:
            pos = [0, 0]
        self.size: list = size
        self.pos: list = pos
        self.corner_radius = corner_radius

        self.action = action

        self.color: list = [255, 255, 255]
        self.text: str = ""
        self.clickable: bool = False
        self.textAlignment: str = ""  # e, n, s, w, c

        self.buttonRect = pg.Rect(*self.pos, *self.size)

        self.defaultTexture = pg.image.load("../../textures/test/NO_TEXTURE.png")
        self.buttonTexture = self.defaultTexture
        self.set_texture("../../textures/test/NO_TEXTURE.png", scale_by=self.size)

    def draw(self, with_texture: bool = False):
        # pg.draw.rect(self.surface, self.color, self.buttonRect, border_radius=self.corner_radius)

        if with_texture:
            self.surface.blit(self.buttonTexture, self.pos)

    def on_click(self, mouse_pos) -> bool:
        if not self.clickable:
            return False
        if not self.buttonRect.collidepoint(mouse_pos):
            return False
        # self.buttonTexture = self.defaultTexture
        print(self.action())
        return True

    def set_texture(self, texture_path: str, linear_scaling: bool = False, scale_by=None,
                    prioritize_texture_size: bool = False):
        self.buttonTexture = pg.image.load(texture_path)

        if scale_by is None:
            scale_by = self.size
        if not prioritize_texture_size:
            self.buttonTexture = pg.transform.scale(self.buttonTexture, self.size)

        if linear_scaling:
            self.buttonTexture = pg.transform.scale_by(self.buttonTexture, scale_by)
        else:
            self.buttonTexture = pg.transform.scale(self.buttonTexture, scale_by)
        self.size[0] = self.size[0] * scale_by if linear_scaling else scale_by[0]
        self.size[1] = self.size[1] * scale_by if linear_scaling else scale_by[1]

        if prioritize_texture_size:
            self.size = list(self.buttonTexture.get_size())

        self.update()

    def update(self):
        self.buttonRect = pg.Rect(*self.pos, *self.size)

    def remove_texture(self):
        self.buttonTexture = self.defaultTexture


class Ship(Node):
    def __init__(self, surface, size: list = None, pos: list = None, corner_radius: int = 0, z_index: int = 0):
        super().__init__(surface, size, pos, corner_radius, z_index)
