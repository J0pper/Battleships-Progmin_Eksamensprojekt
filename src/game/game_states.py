import pygame as pg
from widgets import Node, TexturedNode, ButtonNode
from objects_and_utils import Tile
import os
import math


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
        mid = (res[0] / 2, res[1] / 2)

        background.set_texture("../../textures/title_screen/background.png", linear_scaling=True,
                               scale_by=scaleFactor[0], prioritize_texture_size=True)
        title.set_texture("../../textures/title_screen/title.png", linear_scaling=True,
                          scale_by=scaleFactor[0],  prioritize_texture_size=True)
        startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)

        background.move(mid)
        title.move(mid)
        startButton.move((mid[0], mid[1] * 1.5))

        self.titScrSpriteGroup = pg.sprite.Group()
        self.titScrSpriteGroup.add(background, title, startButton)

    def draw(self):
        self.titScrSpriteGroup.draw(self.surface)


# GAME SCREEN CLASS
class GameScreen:
    def __init__(self, surface):
        self.surface = surface

        self.boardSpriteGroup = pg.sprite.Group()

        gameScreen_bg = TexturedNode(self.surface)
        gameScreen_bg.set_texture("../../textures/elements/GUI_table.png")
        self.boardSpriteGroup.add(gameScreen_bg)

        res = self.surface.get_size()
        scaleFactor: tuple = (res[0] / 320, res[1] / 180)
        mid = (res[0] / 2, res[1] / 2)

        self.boardTexture = TexturedNode(self.surface)
        self.boardTexture.set_texture("../../textures/elements/spillerpladeWgrid_you.png", linear_scaling=True,
                                      scale_by=scaleFactor[0], prioritize_texture_size=True)
        self.boardSpriteGroup.add(self.boardTexture)

        self.boardTileGrid = self.make_board(self.boardSpriteGroup, scale_factor=scaleFactor)
        self.move_board(self.boardTileGrid, self.boardTexture, mid)

        self.ships = self.generate_ships("../../textures/boats")

    def draw(self):
        self.boardSpriteGroup.draw(self.surface)
        Ship.shipSpriteGroup.draw(self.surface)

        for ship in self.ships:
            if ship.hover:
                ship.move_ship(ship.follow_cursor())

    def make_board(self, sprite_group, rows: int = 10, columns: int = 10,
                   tile_size: tuple[int, int] = (8, 8), tile_spacing: tuple[int, int] = (10, 10),
                   border_offset = (4, 4), scale_factor: tuple = (1, 1)) -> list[Tile]:
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
        :param scale_factor: Scale the sizing of the tiles to fit the screen resolution.
        :return: A board-structure with all information for each tile.
        """

        board: list[Tile] = []
        for row in range(rows):
            for column in range(columns):
                sprite = Node(self.surface, (tile_size[0] * scale_factor[0], tile_size[1] * scale_factor[1]),
                              ((column * tile_spacing[0] + border_offset[0]) * scale_factor[0],
                               (row * tile_spacing[1] + border_offset[1]) * scale_factor[1]))
                tile: Tile = Tile((column, row), sprite)
                sprite.withColor = False

                sprite_group.add(sprite)
                board.append(tile)
        return board

    def generate_ships(self, texture_directory):
        ships: list[Ship] = []
        shipTextures: list = os.listdir(texture_directory)
        for i in range(len(shipTextures)):
            ships.append(Ship(self.surface, f"{texture_directory}/{shipTextures[i]}",
                              ((i * 100) + 100, 150), self.boardTileGrid))
        return ships

    def move_board(self, board: list[Tile], board_texture: TexturedNode, new_pos: tuple[int, int]):
        centerPoint = self.midpoint(board[0].sprite.pos, board[-1].sprite.pos)
        offset = (new_pos[0] - centerPoint[0], new_pos[1] - centerPoint[1])

        for i, tile in enumerate(board):
            spritePos = tile.sprite.pos
            moveTo = (spritePos[0] + offset[0], spritePos[1] + offset[1])
            tile.sprite.move(moveTo)
        board_texture.move(new_pos)

    def midpoint(self, vec1: tuple[int, int], vec2: tuple[int, int]) -> tuple[float, float]:
        return (vec2[0] - vec1[0]) / 2 + vec1[0], (vec2[1] - vec1[1]) / 2 + vec1[1]


#  SHIP CLASS
class Ship:
    shipSpriteGroup = pg.sprite.Group()

    def __init__(self, surface, texture_path, start_pos, board):
        res = surface.get_size()
        scaleFactor = [res[0] / 320, res[1] / 180]
        mid = (res[0] / 2, res[1] / 2)

        self.ship = ButtonNode(surface, z_index=1, action=lambda: self.toggle_hover())
        self.ship.set_texture(texture_path, linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)
        self.ship.pos = start_pos
        self.hover = False
        self.shipSpriteGroup.add(self.ship)
        self.ship.update()

        self.board = board

        self.offset = []

    def toggle_hover(self):
        if self.hover:
            self.hover = False
            self.snap_ship(self.board)
        else:
            self.offset = (pg.mouse.get_pos()[0] - self.ship.pos[0], pg.mouse.get_pos()[1] - self.ship.pos[1])
            self.hover = True

    def move_ship(self, new_pos):
        self.ship.move(new_pos)
        self.ship.update()

    def follow_cursor(self) -> tuple[int, int]:
        return pg.mouse.get_pos()[0] - self.offset[0], pg.mouse.get_pos()[1] - self.offset[1]

    def snap_ship(self, board: list[Tile]):
        targetTile = self.generate_distance_array(board)[0]
        targetTilePos = 0
        for tile in board:
            if tile.index != targetTile[0]:
                continue
            targetTilePos = tile.sprite.pos
            break
        self.move_ship(tuple(targetTilePos))

    def generate_distance_array(self, board: list[Tile]) -> list[tuple[tuple, float]]:
        tileDistances: list[tuple[tuple, float]] = []

        for tile in board:
            tileDistances.append((tile.index, self.calc_tile_distance(tile.sprite.pos)))
        sortedTileDistances = sorted(tileDistances, key=lambda distance: distance[1])
        return sortedTileDistances

    def calc_tile_distance(self, tile_pos: tuple[int, int]) -> float:
        shipPos = self.ship.pos
        return math.sqrt((shipPos[0] - tile_pos[0])**2 + (shipPos[1] - tile_pos[1])**2)

    def calc_tile_from_distance(self):
        pass

    def get_pos(self):
        return self.ship.pos
