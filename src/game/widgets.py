import pygame as pg


class Node(pg.sprite.Sprite):
    def __init__(self, surface, size: tuple[int, int] = None, pos: tuple[int, int] = None,
                 color: tuple[int, int, int] = None, corner_radius: int = 0):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface

        if size is None:
            size = (100, 100)
        if pos is None:
            pos = (0, 0)
        if color is None:
            color = (0, 255, 0)

        self.size: list[int] = list(size)
        self.pos: list[int] = list(pos)
        self.color: list[int] = list(color)
        self.corner_radius: int = corner_radius

        self.nodeRect = pg.Rect(*self.pos, *self.size)
        self.image = pg.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    """
    def draw(self):
        self.update()
        pg.draw.rect(self.surface, self.color, self.buttonRect)
    """

    def update(self):
        self.nodeRect = pg.Rect(*self.pos, *self.size)
        self.rect.center = self.pos
        self.image.fill(self.color)

    def move(self, new_pos):
        self.pos = new_pos
        self.update()


class TexturedNode(Node):
    def __init__(self, surface):
        super().__init__(surface=surface)
        pg.sprite.Sprite.__init__(self)

        self.defaultTexture = pg.image.load("../../textures/test/NO_TEXTURE.png")
        self.buttonTexture = self.defaultTexture
        self.set_texture("../../textures/test/NO_TEXTURE.png", scale_by=self.size)
        self.image = self.buttonTexture
        self.rect = self.buttonTexture.get_rect()

    def update(self):
        self.nodeRect.center = self.pos
        self.rect = self.nodeRect
        self.image.fill((0, 0, 255))
        self.image = self.buttonTexture

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

        self.nodeRect.size = self.size
        self.update()


class ButtonNode(TexturedNode):
    registry: list[tuple] = []

    def __init__(self, surface, z_index: int = 0, action=None):
        super().__init__(surface=surface)
        pg.sprite.Sprite.__init__(self)

        self.registry.append((self, z_index))

        self.clickable = True
        self.action = action

    def on_click(self, mouse_pos) -> bool:
        if not self.clickable:
            return False
        if not self.nodeRect.collidepoint(mouse_pos):
            return False
        # TO DO ADD SOUND HERE
        shipHit_sfx = pg.mixer.Sound("SHIP HIT.m4a")
        youMissed_sfx = pg.mixer.Sound("YOU MISSED.m4a")
        boom_sfx = pg.mixer.Sound("BOOM 1.m4a")
        kaboom_sfx = pg.mixer.Sound("KABOOM.m4a")
        wompWomp_sfx = pg.mixer.Sound("WOMPWOMP.m4a")
        wow_sfx = pg.mixer.Sound("WOW.m4a")
        yyo_sfx = pg.mixer.Sound("YARR YEBEE OVERBOARF.m4a")
        weSinkin_sfx = pg.mixer.Sound("CAPTAIN WE SINKIN.m4a")






        self.action()
        return True
