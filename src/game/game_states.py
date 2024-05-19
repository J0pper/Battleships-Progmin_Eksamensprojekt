import os
import sys
import socket
from typing import Union, NoReturn, Any, Self

import pygame as pg

from widgets import Node, TexturedNode, ButtonNode
from utils import *
from board import Board, Tile

from networking.network import Network
from board_manager import BoardManager


gameScenes: dict[str, Any] = {}
currentScene: Union = None

network: Union[Network, None] = None
playerNumber: int = 0
boardManager: Union[BoardManager, None] = None


def get_scene():
    global currentScene
    return currentScene


def set_scene(new_scene):
    global currentScene
    currentScene = new_scene


def set_all_scenes(scenes):
    global gameScenes
    gameScenes = scenes


def button_validater(from_scene, action):
    if gameScenes[from_scene] != currentScene:
        return False
    action()
    return True


#  TITLE SCREEN CLASS
class TitleScreen:
    def __init__(self, surface: pg.Surface):
        self.surface: pg.Surface = surface

        background: TexturedNode = TexturedNode(self.surface)
        title: TexturedNode = TexturedNode(self.surface)
        startButton: ButtonNode = ButtonNode(self.surface,
                                             action=lambda: button_validater("titleScreen",
                                                                             lambda: set_scene(gameScenes["connectScreen"])))

        res: tuple[int, int] = self.surface.get_size()
        scaleFactor: tuple[float, float] = (res[0] / 320, res[1] / 180)
        mid: tuple[float, float] = (res[0] / 2, res[1] / 2)

        background.set_texture("../../textures/title_screen/background.png", linear_scaling=True,
                               scale_by=scaleFactor[0], prioritize_texture_size=True)
        title.set_texture("../../textures/title_screen/title.png", linear_scaling=True,
                          scale_by=scaleFactor[0],  prioritize_texture_size=True)
        startButton.set_texture("../../textures/title_screen/NORMAL_Start.png",
                                linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)

        background.move(mid)
        title.move(mid)
        startButton.move((mid[0], mid[1] * 1.5))

        self.titScrSpriteGroup: pg.sprite.Group = pg.sprite.Group()
        self.titScrSpriteGroup.add(background, title, startButton)

    def draw(self):
        self.titScrSpriteGroup.draw(self.surface)


class ConnectScreen:
    def __init__(self, surface):
        self.firstRun = True

        self.surface = surface

        ipAddress: str = socket.gethostbyname(socket.gethostname())

        titleText: Node = Node(self.surface, pos=(100, 40), text="Waiting for players...")
        ipText1: Node = Node(self.surface, pos=(100, 80), text="Your local IP-address is:")
        ipText2: Node = Node(self.surface, pos=(100, 110), text=f"{ipAddress}")
        bottomText: Node = Node(self.surface, pos=(100, 140), text="Share it with your friend to play!")
        self.text: list[Node] = [titleText, ipText1, ipText2, bottomText]

    def draw(self):
        self.surface.fill((34, 34, 34))
        for text in self.text:
            text.draw_text()

        global network, playerNumber, boardManager
        if self.firstRun:
            network = Network()
            playerNumber = int(network.get_connection_message())
            print("playerNumber", playerNumber)
            self.firstRun = False
        try:
            boardManager = network.send("get")
        except:
            print("Couldn't get board manager")
            pg.quit()
            sys.exit()

        if boardManager.connectReady:
            print("2 PLAYS CONNECTED")
            button_validater("connectScreen", set_scene(gameScenes["gameScreen"]))


# GAME SCREEN CLASS
class GameScreen:
    def __init__(self, surface: pg.Surface):
        self.surface: pg.Surface = surface

        # CREATE DIFFERENT VARIABLES USED FOR SCALING AND POSITIONING NODES
        res: tuple[int, int] = self.surface.get_size()
        scaleFactor: tuple[float, float] = (res[0] / 320, res[1] / 180)
        mid: tuple[float, float] = (res[0] / 2, res[1] / 2)
        leftBoardPos = (res[0] * 6/20, res[1] / 2)
        rightBoardPos = (res[0] * 14/20, res[1] / 2)

        self.otherSprites = pg.sprite.Group()

        self.playerBoard = Board(self.surface, "../../textures/elements/spillerpladeWgrid_you.png",
                                 leftBoardPos, scaleFactor)
        self.enemyBoard = Board(self.surface, "../../textures/elements/spillerpladeWgrid_enemy.png",
                                rightBoardPos, scaleFactor,
                                tile_click_action=lambda: button_validater("gameScreen",
                                                                           lambda: self.attempt_strike()))

        # CREATE GAME SCREEN NODES.
        gameScreenBG = TexturedNode(self.surface)
        self.shipCompartment = TexturedNode(self.surface)
        self.readyButton = ButtonNode(self.surface, z_index=20,
                                      action=lambda: button_validater("gameScreen",
                                                                      lambda: self.ready_up()))
        self.winText = Node(self.surface, pos=(mid[0]*0.8, mid[1]*0.15), text="")

        # LOAD TEXTURES FOR GAME SCREEN NODES.
        gameScreenBG.set_texture("../../textures/elements/GUI_table.png", linear_scaling=True,
                                 scale_by=scaleFactor[0])
        self.shipCompartment.set_texture("../../textures/elements/GUI_remaining106x35.png",
                                         linear_scaling=True, scale_by=scaleFactor[0])
        self.shipCompartment.rotate_image()

        self.readyButton.set_texture("../../textures/elements/ready.png", linear_scaling=True,
                                     scale_by=scaleFactor[0])

        # MOVE SCREEN NODES.
        gameScreenBG.move(mid)
        self.shipCompartment.move((self.shipCompartment.size[0] / 2, mid[1]))
        self.readyButton.move((mid[0], mid[1]*1.75))

        # ADD SCREEN NODES TO THE SPRITE-GROUPS.
        self.otherSprites.add(gameScreenBG, self.shipCompartment, self.readyButton)

        # GENERATE THE SHIPS.
        self.ships: list[Ship] = self.generate_ships("../../textures/boats", self.playerBoard.get_tiles())

        self.playerTurn: int = 0

    def draw(self) -> NoReturn:
        global network, boardManager
        try:
            boardManager = network.send("get")
            network.send(self.enemyBoard.get_formatted_tiles())
        except:
            print("Couldn't get board manager")
            pg.quit()
            sys.exit()

        self.otherSprites.draw(self.surface)
        self.playerBoard.get_board_sprite_group()[0].draw(self.surface)
        self.enemyBoard.get_board_sprite_group()[0].draw(self.surface)
        Ship.shipSpriteGroup.draw(self.surface)
        self.playerBoard.get_board_sprite_group()[1].draw(self.surface)
        self.enemyBoard.get_board_sprite_group()[1].draw(self.surface)
        self.winText.draw_text()

        if not self.enemyBoard.shipReady:
            for ship in self.ships:
                if ship.hover:
                    ship.move_ship(ship.follow_cursor())
                    if pg.mouse.get_pressed()[2]:
                        if ship.allowRotate:
                            ship.allowRotate = False
                            ship.rotate_ship()
                        continue
                    else:
                        ship.allowRotate = True

        if boardManager.shipReady:
            if playerNumber == 0:
                self.playerBoard.update_touched_tiles(boardManager.player2Board)
                self.enemyBoard.update_ship_state(boardManager.player2ShipStates)
            elif playerNumber == 1:
                self.playerBoard.update_touched_tiles(boardManager.player1Board)
                self.enemyBoard.update_ship_state(boardManager.player1ShipStates)

        self.playerBoard.update_textures()
        self.enemyBoard.update_textures()

        self.playerTurn = boardManager.playerTurn

        winner = self.check_for_winner()
        if winner[0]:
            self.winText.update_text(winner[1])

    def generate_ships(self, texture_directory: str, tile_grid: list[Tile]) -> list['Ship']:
        ships: list[Ship] = []
        shipTextures: list = os.listdir(texture_directory)

        # This is absolutely atrocious and disgusting and honestly must be a crime, but it was what was easiest :sob:.
        containerPos = self.shipCompartment.pos
        containerSize = self.shipCompartment.size
        leftRowX = containerPos[0] - containerSize[0] / 4
        rightRowX = containerPos[0] + containerSize[0] / 4
        topRowY = tile_grid[20].sprite.pos[1]
        midRowY = ((tile_grid[60].sprite.pos[1] - tile_grid[50].sprite.pos[1]) / 2
                   + tile_grid[50].sprite.pos[1])
        botRowY = tile_grid[80].sprite.pos[1]

        startPositions = [(rightRowX, midRowY), (rightRowX, botRowY), (leftRowX, topRowY),
                          (leftRowX, midRowY), (rightRowX, topRowY)]
        for i in range(len(shipTextures)):
            ships.append(Ship(self.surface, f"{texture_directory}/{shipTextures[i]}",
                              startPositions[i], tile_grid))
        return ships

    def ready_up(self) -> NoReturn:
        global network
        coveredTiles: int = 0
        for tile in self.playerBoard.get_tiles():
            if tile.shipState == 1:
                coveredTiles += 1
        if coveredTiles == 17:
            self.playerBoard.shipReady = True
            self.enemyBoard.shipReady = True
            network.send(("ready", self.playerBoard.get_occupied_tiles()))

    def attempt_strike(self) -> None:
        global boardManager, playerNumber
        if not boardManager.shipReady:
            return
        if self.playerTurn != playerNumber:
            return
        network.send("flip_turn")

        for tile in self.enemyBoard.get_tiles():
            if tile.sprite != ButtonNode.lastClicked[0]:
                continue
            self.enemyBoard.touch_tile(tile)

    def check_for_winner(self) -> tuple[bool, str]:
        if self.playerBoard.get_hit() == 17:
            return True, "You lost :("
        if self.enemyBoard.get_hit() == 17:
            return True, "You won!"
        else:
            return False, ""


# SHIP CLASS
class Ship:
    shipSpriteGroup = pg.sprite.Group()
    shipMoving: bool = False

    def __init__(self, surface: pg.Surface, texture_path: str, start_pos: tuple[float, float], board: list[Tile]):
        res: tuple[int, int] = surface.get_size()
        self.scaleFactor: tuple[float, float] = (res[0] / 320, res[1] / 180)

        self.ship: ButtonNode = ButtonNode(surface, z_index=20, action=lambda: self.toggle_hover())
        self.ship.set_texture(texture_path, linear_scaling=True,
                              scale_by=self.scaleFactor[0], prioritize_texture_size=True)
        self.ship.pos = start_pos
        self.shipSpriteGroup.add(self.ship)
        self.ship.update()

        self.coveredTiles: list[Tile] = []
        self.board: list[Tile] = board
        self.shipLengthInTiles: int = first_n_digits(max(*self.ship.size) / self.scaleFactor[0], 1)

        self.hover: bool = False

        self.offset: tuple[int, int] = (0, 0)

        self.allowRotate: bool = True

    def toggle_hover(self) -> None:
        if self.hover:
            if self.snap_ship():
                self.hover = False
                Ship.shipMoving = False
                self.update_tile_occupancy()
            return
        if Ship.shipMoving:
            return
        self.update_tile_occupancy(clear=True)
        self.offset = [pg.mouse.get_pos()[0] - self.ship.pos[0], pg.mouse.get_pos()[1] - self.ship.pos[1]]
        Ship.shipMoving = True
        self.hover = True

    def move_ship(self, new_pos: tuple[int, int]):
        self.ship.move(new_pos)
        self.ship.update()

    def follow_cursor(self) -> tuple[int, int]:
        return pg.mouse.get_pos()[0] - self.offset[0], pg.mouse.get_pos()[1] - self.offset[1]

    def snap_ship(self) -> bool:
        targetTile = self.generate_distance_array()[0]
        targetTilePos: tuple[int, int] = (0, 0)
        for tile in self.board:
            if tile.index != targetTile[0]:
                continue
            targetTilePos = tile.sprite.pos
            break
        # Grabs the first size of whatever is the ships largest dimension (makes sure it works for all directions) and
        # checks if its odd or even. If its even we know it a 2 or 4 tile long ship, and we can treat it differently.
        if not self.shipLengthInTiles % 2:
            if self.ship.size[0] > self.ship.size[1]:
                targetTilePos = (targetTilePos[0] - self.board[0].sprite.size[0] / 2, targetTilePos[1])
            elif self.ship.size[0] < self.ship.size[1]:
                targetTilePos = (targetTilePos[0], targetTilePos[1] + self.board[0].sprite.size[0] / 2)

        if not self.inside_borders(targetTilePos):
            return False
        if self.ships_touching():
            return False

        self.move_ship(targetTilePos)
        return True

    def generate_distance_array(self) -> list[tuple[tuple[int, int], float]]:
        tileDistances: list[tuple[tuple[int, int], float]] = []

        shipPos: tuple[int, int] = (self.ship.pos[0], self.ship.pos[1])
        # Offset the position of the 2 and 4 tile long ships. If we don't do this, it calculated the distance based
        # of the center of the ship, which works fine for the 3 and 5 tile long ships since their center will be
        # centered in the tile no matter what. But for the ships with even tile length, their center is in the middle
        # of two tiles. Therefore, we offset the center of the ship towards the middle of one of the ships halves. This
        # is the position that should be in the center of the tile and is what we will use to calculate the distance
        # to a specified tile.
        if not self.shipLengthInTiles % 2:
            if self.ship.size[0] > self.ship.size[1]:
                shipPos = (shipPos[0] + max(self.ship.size) / 4, shipPos[1])
            elif self.ship.size[0] < self.ship.size[1]:
                shipPos = (shipPos[0], shipPos[1] - max(self.ship.size) / 4)

        for tile in self.board:
            tileDistances.append((tile.index, calc_vec_distance(shipPos, tile.sprite.pos)))
        sortedTileDistances = sorted(tileDistances, key=lambda distance: distance[1])
        return sortedTileDistances

    def inside_borders(self, target_tile_pos: tuple[int, int]) -> bool:
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
        affectedTiles: list[Tile] = self.get_touching_tiles()
        for tile in affectedTiles:
            if tile.shipState == 1:
                return True
        for tile in self.coveredTiles:
            tile.shipState = 0
        return False

    def update_tile_occupancy(self, clear: bool = False):
        affectedTiles: list[Tile] = self.get_touching_tiles()
        self.coveredTiles = affectedTiles
        for tile in affectedTiles:
            if clear:
                tile.shipState = 0
                self.coveredTiles = []
                continue
            tile.shipState = 1

    def get_touching_tiles(self) -> list[Tile]:
        affectedTiles: list[Tile] = []
        shipEdges: tuple[Union[Any, tuple[int, int]], Union[Any, tuple[int, int]]] =\
            (*self.ship.nodeRect.topleft, *self.ship.nodeRect.bottomright)
        for tile in self.board:
            tilePos = tile.sprite.pos
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

    def rotate_ship(self) -> NoReturn:
        self.offset = self.offset[::-1]
        self.move_ship(self.follow_cursor())
        self.ship.rotate_image()
