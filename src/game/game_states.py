from widgets import Node


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

        self.background = Node(self.surface, [320, 180], [0, 0], z_index=0)
        self.title = Node(self.surface, [320, 180], [0, 0], z_index=1)
        self.startButton = Node(self.surface, [320, 180], [0, 0], z_index=0,
                                action=[lambda: set_scene(gameScenes["gameScreen"]),
                                        get_scene,
                                        self])

        self.startButton.clickable = True

        res = surface.get_size()
        self.scaleFactor = [res[0] / 320, res[1] / 180]

        self.background.set_texture("../../textures/title_screen/background.png", linear_scaling=True,
                                    scale_by=self.scaleFactor[0], prioritize_texture_size=True)
        self.title.set_texture("../../textures/title_screen/title.png", linear_scaling=True,
                               scale_by=self.scaleFactor[0],  prioritize_texture_size=True)
        self.startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                     linear_scaling=True, scale_by=self.scaleFactor[0], prioritize_texture_size=True)

    def draw(self):
        self.background.draw(with_texture=True)
        self.title.draw(with_texture=True)
        self.startButton.draw(with_texture=True)


class GameScreen:
    def __init__(self, surface):
        self.number = 10
        self.surface = surface

        self.test = Node(surface, [320, 180], [200, 0], z_index=0)
        self.test.set_texture("../../textures/test/Marck_SUCK.png")

    def draw(self):
        self.test.draw(with_texture=True)
