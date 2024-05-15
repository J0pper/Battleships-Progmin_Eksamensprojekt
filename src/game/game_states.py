import pygame as pg
from widgets import Node, TexturedNode, ButtonNode
import os


gameScenes: dict = {}
currentScene = None


def get_scene():
    global currentScene
    return currentScene


def set_scene(new_scene):
    global currentScene
    if currentScene is not new_scene:
        currentScene = new_scene


def set_all_scenes(scenes):
    global gameScenes
    gameScenes = scenes


#  TITLE SCREEN CLASS
class TitleScreen:
    def __init__(self, surface):
        self.surface = surface

        background = TexturedNode(self.surface)
        title = TexturedNode(self.surface)
        startButton = ButtonNode(self.surface, action=lambda: set_scene(gameScenes["gameScreen"]))

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



# GAMESCREEN CLASS
class GameScreen:
    def __init__(self, surface):
        self.surface = surface

        gameScreen_bg = TexturedNode(self.surface)
        gameScreen_bg.set_texture("../../textures/elements/GUI_table.png")

        self.gamScrSpriteGroup = pg.sprite.Group()
        self.gamScrSpriteGroup.add(gameScreen_bg)
        board = self.make_board(self.gamScrSpriteGroup)
        self.move_board(board, (0, 0))


        self.ships = self.generate_ships("../../textures/boats")

    def draw(self):
        self.gamScrSpriteGroup.draw(self.surface)
        Ship.shipSpriteGroup.draw(self.surface)

        for ship in self.ships:
            if ship.hover:
                ship.move_ship()

    def make_board(self, sprite_group, rows: int = 10, columns: int = 10,
                   tile_size: tuple[int, int] = (25, 25), tile_spacing: tuple[int, int] = (50, 50)) -> list[dict]:
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
                sprite = Node(self.surface, tile_size,(column * tile_spacing[0], row * tile_spacing[1]))
                square: dict = {
                    "index": (column, row),
                    "rect_object": sprite,
                    "ship_state": "unoccupied",
                    "hit_state": None
                }
                sprite_group.add(sprite)
                board.append(square)
        return board

    def generate_ships(self, texture_directory):
        ships: list[Ship] = []
        shipTextures: list = os.listdir(texture_directory)
        for i in range(len(shipTextures)):
            ships.append(Ship(self.surface, f"{texture_directory}/{shipTextures[i]}",
                              ((i * 100)+100, 150)))
        return ships

    def move_board(self, board: list[dict], offset: tuple):
        for tile in board:
            for key, value in tile.items():
                if key != "rect_object":
                    continue
                pos = value.pos
                value.move([pos[0] + offset[0], pos[1] + offset[1]])


#  SHIP CLASS
class Ship:
    shipSpriteGroup = pg.sprite.Group()

    def __init__(self, surface, texture_path, start_pos):
        self.ship = ButtonNode(surface, z_index=1, action=lambda: self.toggle_hover())
        self.ship.set_texture(texture_path, linear_scaling=True, scale_by=3)
        self.ship.pos = start_pos
        self.hover = False
        self.shipSpriteGroup.add(self.ship)
        self.ship.update()

        self.offset = []

    def toggle_hover(self):
        if self.hover:
            self.hover = False
        else:
            self.offset = (pg.mouse.get_pos()[0] - self.ship.pos[0], pg.mouse.get_pos()[1] - self.ship.pos[1])
            self.hover = True

    def move_ship(self):
        self.ship.pos = (pg.mouse.get_pos()[0] - self.offset[0], pg.mouse.get_pos()[1] - self.offset[1])
        self.ship.update()

    def snap_ship(self, ):
        pass

    def get_pos(self):
        return self.ship.pos
