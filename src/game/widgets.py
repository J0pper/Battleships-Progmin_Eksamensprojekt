import pygame as pg


class Node(pg.sprite.Sprite):
    def __init__(self, surface, size: tuple[int, int] = None, pos: tuple[int, int] = None,
                 color: tuple[int, int, int] = None, corner_radius: int = 0, text: str = None):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface

        if size is None:
            size = (100, 100)
        if pos is None:
            pos = (0, 0)
        if color is None:
            color = (0, 255, 0)
        if text is None:
            text = "No text."
            self.withText: bool = False
        else:
            self.withText = True

        self.size: list[int] = list(size)
        self.pos: list[int] = list(pos)
        self.color: list[int] = list(color)
        self.corner_radius: int = corner_radius
        self.text = text
        self.font = pg.font.SysFont('Arial', 30)
        self.textSurface = self.font.render(text, 1, (255, 255, 255))
        self.withColor: bool = False

        self.nodeRect = pg.Rect(*self.pos, *self.size)
        self.image = pg.Surface(self.size)
        self.image.set_alpha(0)
        self.rect = self.nodeRect

    def update(self):
        self.nodeRect.size = self.size
        self.nodeRect.center = self.pos
        self.rect = self.nodeRect
        if self.withColor:
            self.image.set_alpha(255)
            self.image.fill(self.color)

    def move(self, new_pos):
        self.pos = new_pos
        self.update()

    def draw_text(self):
        if self.withText:
            self.surface.blit(self.textSurface, self.nodeRect.center)

    def rotate_rect(self):
        self.size = self.size[::-1]
        self.update()


class TexturedNode(Node):
    def __init__(self, surface, default_texture: bool = True):
        super().__init__(surface=surface)
        pg.sprite.Sprite.__init__(self)

        self.angle = 0

        if default_texture:
            self.defaultTexture = pg.image.load("../../textures/test/NO_TEXTURE.png")
            self.buttonTexture = self.defaultTexture
            self.set_texture("../../textures/test/NO_TEXTURE.png", scale_by=self.size)
            self.update()

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

    def rotate_image(self):
        self.angle += 90
        if self.angle > 270:
            self.angle = 0
        self.image = pg.transform.rotate(self.buttonTexture, -self.angle)
        self.rotate_rect()


class ButtonNode(TexturedNode):
    registry: list[tuple] = []

    def __init__(self, surface, z_index: int = 0, action=None, default_texture: bool = True):
        super().__init__(surface=surface, default_texture=default_texture)
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
        """
        shipHit_sfx = pg.mixer.Sound("../../audio/SHIP HIT.mp3")
        youMissed_sfx = pg.mixer.Sound("../../audio/YOU MISSED.mp3")
        splash_sfx = shipHit_sfx = pg.mixer.Sound("../../audio/SPLASH 1.mp3")
        boom_sfx = pg.mixer.Sound("../../audio/BOOM 1.mp3")
        kaboom_sfx = pg.mixer.Sound("../../audio/KABOOM.mp3")
        wompWomp_sfx = pg.mixer.Sound("../../audio/WOMPWOMP.mp3")
        wow_sfx = pg.mixer.Sound("../../audio/WOW.mp3")
        yyo_sfx = pg.mixer.Sound("../../audio/YARR YEBEE OVERBOARF.mp3")
        weSinkin_sfx = pg.mixer.Sound("../../audio/CAPTAIN WE SINKIN.mp3")
        shipSunk_sfx = pg.mixer.Sound("../../audio/SHIP SUNK.mp3")
        """

        self.action()
        return True
