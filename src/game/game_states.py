import pygame as pg
from widgets import Node, TexturedNode, ButtonNode
from objects_and_utils import *
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
        startButton = ButtonNode(self.surface, action=lambda: set_scene(gameScenes["connectionScreen"]))

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

        self.ipText = Node(self.surface, pos=(100, 100), text="hello")
        print(self.ipText.withText)

    def draw(self):
        self.titScrSpriteGroup.draw(self.surface)
        self.ipText.draw_text()


class ConnectionScreen:
    def __init__(self, surface):
        self.surface = surface

        self.conScrSpriteGroup = pg.sprite.Group()

        res = self.surface.get_size()
        scaleFactor = [res[0] / 320, res[1] / 180]
        mid = (res[0] / 2, res[1] / 2)

        startButton = ButtonNode(self.surface, action=lambda: set_scene(gameScenes["gameScreen"]))
        startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)

        self.conScrSpriteGroup.add(startButton)

    def draw(self):
        self.surface.fill((34, 34, 34))
        self.conScrSpriteGroup.draw(self.surface)


# GAME SCREEN CLASS
class GameScreen:
    def __init__(self, surface):
        self.surface = surface

        self.boardSpriteGroup = pg.sprite.Group()
        self.gridGroup = pg.sprite.Group()

        res = self.surface.get_size()
        scaleFactor: tuple = (res[0] / 320, res[1] / 180)
        mid = (res[0] / 2, res[1] / 2)
        quarterLeft = (res[0] * 6/20, res[1] / 2)
        quarterRight = (res[0] * 14/20, res[1] / 2)

        guiRemaining = TexturedNode(self.surface)
        guiRemaining.set_texture("../../textures/elements/GUI_remaining106x35.png", True,
                                 scale_by=scaleFactor[0], prioritize_texture_size=False)

        gameScreen_bg = TexturedNode(self.surface)
        gameScreen_bg.set_texture("../../textures/elements/GUI_table.png", True,
                                  scale_by=scaleFactor[0], prioritize_texture_size=True)
        self.boardSpriteGroup.add(gameScreen_bg)
        gameScreen_bg.move(mid)
        guiRemaining.move(mid)

        self.playerBoardTexture = TexturedNode(self.surface)
        self.playerBoardTexture.set_texture("../../textures/elements/spillerpladeWgrid_you.png", linear_scaling=True,
                                            scale_by=scaleFactor[0])

        self.enemyBoardTexture = TexturedNode(self.surface)
        self.enemyBoardTexture.set_texture("../../textures/elements/spillerpladeWgrid_enemy.png", linear_scaling=True,
                                           scale_by=scaleFactor[0])

        self.boardSpriteGroup.add(self.playerBoardTexture)
        self.boardSpriteGroup.add(self.enemyBoardTexture)

        self.playerBoardTileGrid = self.make_board(self.gridGroup, scale_factor=scaleFactor)
        self.move_board(self.playerBoardTileGrid, self.playerBoardTexture, quarterLeft)

        self.enemyBoardTileGrid = self.make_board(self.gridGroup, scale_factor=scaleFactor)
        self.move_board(self.enemyBoardTileGrid, self.enemyBoardTexture, quarterRight)

        self.ships = self.generate_ships("../../textures/boats")

    def draw(self):
        self.boardSpriteGroup.draw(self.surface)
        Ship.shipSpriteGroup.draw(self.surface)
        self.gridGroup.draw(self.surface)

        for ship in self.ships:
            if ship.hover:
                ship.move_ship(ship.follow_cursor())
                if pg.key.get_pressed()[pg.K_r]:
                    if ship.allowRotate:
                        ship.allowRotate = False
                        ship.rotate_ship()
                else:
                    ship.allowRotate = True

    def make_board(self, sprite_group, rows: int = 10, columns: int = 10,
                   tile_size: tuple[int, int] = (10, 10), tile_spacing: tuple[int, int] = (10, 10),
                   border_offset: tuple[int, int] = (4, 4), scale_factor: tuple = (1, 1)) -> list[Tile]:
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
        :param border_offset:
        :return: A board-structure with all information for each tile.
        """

        board: list[Tile] = []
        for row in range(rows):
            for column in range(columns):
                sprite = Node(self.surface, (tile_size[0] * scale_factor[0], tile_size[1] * scale_factor[1]),
                              ((column * tile_spacing[0] + border_offset[0]) * scale_factor[0],
                               (row * tile_spacing[1] + border_offset[1]) * scale_factor[1]))
                tile: Tile = Tile((column, row), sprite)
                # sprite.withColor = False
                sprite_group.add(sprite)
                board.append(tile)
        return board

    def generate_ships(self, texture_directory):
        ships: list[Ship] = []
        shipTextures: list = os.listdir(texture_directory)
        for i in range(len(shipTextures)):
            ships.append(Ship(self.surface, f"{texture_directory}/{shipTextures[i]}",
                              ((i * 100) + 100, 150), self.playerBoardTileGrid))
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
    shipMoving: bool = False

    def __init__(self, surface, texture_path, start_pos, board: tuple[Tile]):
        res = surface.get_size()
        self.scaleFactor = [res[0] / 320, res[1] / 180]
        mid = (res[0] / 2, res[1] / 2)

        self.ship: ButtonNode = ButtonNode(surface, z_index=1, action=lambda: self.toggle_hover())
        self.ship.set_texture(texture_path, linear_scaling=True, scale_by=self.scaleFactor[0], prioritize_texture_size=True)
        self.ship.pos = start_pos
        self.shipSpriteGroup.add(self.ship)
        self.ship.update()
        self.ship.color = (255, 0, 0)
        self.coveredTiles: list[Tile] = []
        self.board: tuple[Tile] = board

        self.hover: bool = False

        self.offset: tuple = ()

        self.allowRotate: bool = True

    def toggle_hover(self):
        if self.hover:
            if self.snap_ship():
                self.hover = False
                Ship.shipMoving = False
                self.update_tile_occupancy()
                for tile in self.board:
                    if tile.shipState == "occupied":
                        print(tile.index)
                print("")
            return
        if Ship.shipMoving:
            return
        self.update_tile_occupancy(clear=True)
        self.offset = (pg.mouse.get_pos()[0] - self.ship.pos[0], pg.mouse.get_pos()[1] - self.ship.pos[1])
        Ship.shipMoving = True
        self.hover = True

    def move_ship(self, new_pos):
        self.ship.move(new_pos)
        self.ship.update()

    def follow_cursor(self) -> tuple[int, int]:
        return pg.mouse.get_pos()[0] - self.offset[0], pg.mouse.get_pos()[1] - self.offset[1]

    def snap_ship(self) -> bool:
        targetTile = self.generate_distance_array()[0]
        targetTilePos = []
        for tile in self.board:
            if tile.index != targetTile[0]:
                continue
            targetTilePos = tile.sprite.pos
            break
        if not first_n_digits(max(*self.ship.size) / self.scaleFactor[0], 1) % 2:
            targetTilePos = (targetTilePos[0], targetTilePos[1] + self.board[0].sprite.size[0] / 2)

        if not self.inside_borders(targetTilePos):
            return False
        if self.ships_touching():
            return False

        self.move_ship(tuple(targetTilePos))
        return True

    def generate_distance_array(self) -> list[tuple[tuple, float]]:
        tileDistances: list[tuple[tuple, float]] = []

        for tile in self.board:
            tileDistances.append((tile.index, self.calc_tile_distance(tile.sprite.pos)))
        sortedTileDistances = sorted(tileDistances, key=lambda distance: distance[1])
        return sortedTileDistances

    def calc_tile_distance(self, tile_pos: tuple[int, int]) -> float:
        shipPos = self.ship.pos
        return math.sqrt((shipPos[0] - tile_pos[0])**2 + (shipPos[1] - tile_pos[1])**2)

    def inside_borders(self, target_tile_pos: tuple) -> bool:
        shipTopLeft = (target_tile_pos[0] - self.ship.size[0] / 2, target_tile_pos[1] - self.ship.size[1] / 2)
        shipBottomRight = (target_tile_pos[0] + self.ship.size[0] / 2, target_tile_pos[1] + self.ship.size[1] / 2)
        edgePair1: tuple = (*shipTopLeft, *self.board[-1].sprite.nodeRect.bottomright)
        edgePair2: tuple = (*self.board[0].sprite.nodeRect.topleft, *shipBottomRight)

        for i, edge_val in enumerate(edgePair1):
            if edgePair1[i] < edgePair2[i]:
                self.hover = True
                return False
        return True

    def ships_touching(self) -> bool:
        affectedTiles = self.get_touching_tiles()
        for tile in affectedTiles:
            if tile.shipState == "occupied":
                return True
        for tile in self.coveredTiles:
            tile.shipState = "unoccupied"
        return False

    def update_tile_occupancy(self, clear: bool = False):
        affectedTiles: list[Tile] = self.get_touching_tiles()
        self.coveredTiles = affectedTiles
        for tile in affectedTiles:
            if clear:
                tile.shipState = "unoccupied"
                self.coveredTiles = []
                continue
            tile.shipState = "occupied"

    def get_touching_tiles(self) -> list[Tile]:
        affectedTiles: list[Tile] = []
        shipEdges: tuple = (*self.ship.nodeRect.topleft, *self.ship.nodeRect.bottomright)
        for tile in self.board:
            tilePos = tile.sprite.pos
            tile.sprite.withColor = True
            if shipEdges[0] > tilePos[0]:
                continue
            if shipEdges[2] < tilePos[0]:
                continue
            if shipEdges[1] > tilePos[1]:
                continue
            if shipEdges[3] < tilePos[1]:
                continue
            affectedTiles.append(tile)
        return affectedTiles

    def rotate_ship(self):
        self.offset = self.offset[::-1]
        self.move_ship(self.follow_cursor())
        self.ship.rotate_image()
