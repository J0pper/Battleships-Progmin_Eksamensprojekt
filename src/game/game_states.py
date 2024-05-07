import pygame as pg
from widgets import Node, TexturedNode, ButtonNode, SpriteClass


gameScenes: dict = {}
currentScene = None


def get_scene():
    global currentScene
    return currentScene


def set_scene(new_scene):
    global currentScene
    currentScene = new_scene


def set_all_scenes(scenes):
    global gameScenes
    gameScenes = scenes


class TitleScreen:
    def __init__(self, surface):
        self.surface = surface

        self.background = TexturedNode(self.surface, [0, 0])
        self.title = TexturedNode(self.surface, [0, 0])
        self.startButton = ButtonNode(self.surface, action=[lambda: set_scene(gameScenes["gameScreen"]), get_scene, self])

        self.startButton.clickable = True

        res = self.surface.get_size()
        scaleFactor = [res[0] / 320, res[1] / 180]

        self.background.set_texture("../../textures/title_screen/background.png", linear_scaling=True,
                                    scale_by=scaleFactor[0], prioritize_texture_size=True)
        self.title.set_texture("../../textures/title_screen/title.png", linear_scaling=True,
                               scale_by=scaleFactor[0],  prioritize_texture_size=True)
        self.startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                     linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)

        self.titScrSpriteGroup = pg.sprite.Group()
        self.titScrSpriteGroup.add(self.background, self.title, self.startButton)

    def draw(self):
        self.titScrSpriteGroup.draw(self.surface)


class GameScreen:
    def __init__(self, surface):
        self.test = TexturedNode(surface, pos=[234, 100])
        self.test.set_texture("../../textures/test/Marck_SUCK.png")

    def draw(self):
        self.test.texture_draw()
