import pygame as pg
from widgets import Node, TexturedNode, ButtonNode


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

        background = TexturedNode(self.surface, [0, 0])
        title = TexturedNode(self.surface, [0, 0])
        startButton = ButtonNode(self.surface, action=[lambda: set_scene(gameScenes["gameScreen"]), get_scene, self])

        startButton.clickable = True

        res = self.surface.get_size()
        scaleFactor = [res[0] / 320, res[1] / 180]

        background.set_texture("../../textures/title_screen/background.png", linear_scaling=True,
                               scale_by=scaleFactor[0], prioritize_texture_size=True)
        title.set_texture("../../textures/title_screen/title.png", linear_scaling=True,
                          scale_by=scaleFactor[0],  prioritize_texture_size=True)
        startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)

        self.titScrSpriteGroup = pg.sprite.Group()
        self.titScrSpriteGroup.add(background, title, startButton)

    def draw(self):
        self.titScrSpriteGroup.draw(self.surface)


class GameScreen:
    def __init__(self, surface):
        self.surface = surface
        self.test = TexturedNode(self.surface, pos=[234, 100])
        self.test.set_texture("../../textures/test/Marck_SUCK.png")

        self.gamScrSpriteGroup = pg.sprite.Group()
        board = self.make_board(self.gamScrSpriteGroup)
        self.move_board(board, (0, 0))

        """
        for i, tile in enumerate(board):
            print(i)
            for key, value in tile.items():
                if key == "rect_object":
                    print(key, value)
            print(" ")
        """

    def draw(self):
        self.gamScrSpriteGroup.draw(self.surface)

    def make_board(self, sprite_group, rows: int = 10, columns: int = 10,
                   tile_size: list[int, int] = (25, 25), tile_spacing: list[int, int] = (50, 50)) -> list[dict]:
        """
        [{
            "index": (),
            "rect_object": pg.Rect(),
            "ship-state": "occupied" , "unoccupied"
            "hit-state": "hit", "miss", "none"
        }]

        :param sprite_group:
        :param rows: Amount of vertical tiles in the board.
        :param columns: Amount of horizontal tiles in the board.
        :param tile_size: Size of each tile in pixels.
        :param tile_spacing: Spacing between each tile.
        :return: A board-structure with all information for each tile.
        """
        board: list[dict] = [{}]
        for row in range(rows):
            for column in range(columns):
                sprite = Node(self.surface, tile_size,
                              [column * tile_spacing[0], row * tile_spacing[1]])
                square: dict = {
                    "index": (column, row),
                    "rect_object": sprite,
                    "ship-state": "unoccupied",
                    "hit-state": None
                }
                sprite_group.add(sprite)
                board.append(square)
        return board

    def move_board(self, board: list[dict], offset: tuple):
        for tile in board:
            for key, value in tile.items():
                if key != "rect_object":
                    continue
                pos = value.pos
                value.move([pos[0] + offset[0], pos[1] + offset[1]])
