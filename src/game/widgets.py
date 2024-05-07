import pygame as pg


class Node(pg.sprite.Sprite):
    def __init__(self, surface, size: list = None, pos: list = None, color=None, corner_radius: int = 0):
        pg.sprite.Sprite.__init__(self)

        # To get around the "Default argument value is mutable" warning:
        if size is None:
            size = [100, 100]
        if pos is None:
            pos = [0, 0]
        if color is None:
            color = [255, 255, 255]

        self.surface = surface
        self.size: list = size
        self.pos: list = pos
        self.color: list = color
        self.corner_radius: int = corner_radius

        self.buttonRect = pg.Rect(*self.pos, *self.size)
        self.image = self.buttonRect
        self.rect = self.buttonRect

    def draw(self):
        self.update()
        pg.draw.rect(self.surface, self.color, self.buttonRect)

    def update(self):
        self.buttonRect = pg.Rect(*self.pos, *self.size)


class TexturedNode(Node):
    def __init__(self, surface, pos=None):
        super().__init__(surface=surface, pos=pos)
        pg.sprite.Sprite.__init__(self)

        self.defaultTexture = pg.image.load("../../textures/test/NO_TEXTURE.png")
        self.buttonTexture = self.defaultTexture
        self.set_texture("../../textures/test/NO_TEXTURE.png", scale_by=self.size)
        self.image = self.buttonTexture
        self.rect = self.defaultTexture.get_rect()

    def texture_draw(self):
        self.surface.blit(self.buttonTexture, self.pos)

    def set_texture(self, texture_path: str, linear_scaling: bool = False, scale_by=None,
                    prioritize_texture_size: bool = True):
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

        self.image = self.buttonTexture
        self.update()


class ButtonNode(TexturedNode):
    registry = []

    def __init__(self, surface, z_index: int = None, action=None):
        super().__init__(surface=surface)
        pg.sprite.Sprite.__init__(self)

        self.registry.append([self, z_index])

        self.clickable = True
        self.action = action

    def on_click(self, mouse_pos) -> bool:
        if not self.clickable:
            return False
        if not self.buttonRect.collidepoint(mouse_pos):
            return False
        if self.action[1]() != self.action[2]:
            return False

        self.action[0]()
        return True


class SpriteClass(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("../../textures/test/NO_TEXTURE.png")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)


"""

class Node:
    registry = []

    def __init__(self, surface, size: list = None, pos: list = None, corner_radius: int = 0,
                 z_index: int = 0, action=None):
        self.registry.append([self, z_index])
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

        self.defaultTexture = pg.image.load("../../textures/test/NO_TEXTURE.png").convert()
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
        if self.action[1]() != self.action[2]:
            return False

        self.action[0]()
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
"""
