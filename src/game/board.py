
from widgets import *
from utils import midpoint


class Tile:
    def __init__(self, index: tuple[int, int], sprite: ButtonNode):
        self.index: tuple[int, int] = index
        self.sprite: ButtonNode = sprite
        self.touched: bool = False
        self.shipState: int = 0  # 0 = unoccupied, 1 = occupied


class Board:
    def __init__(self, surface: pg.Surface, board_texture: str, board_pos, scale_factor: tuple[float, float],
                 tile_click_action=lambda: 2+2):
        self.surface: pg.Surface = surface
        self.boardSpriteGroup: pg.sprite.Group = pg.sprite.Group()
        self.markersSpriteGroup: pg.sprite.Group = pg.sprite.Group()
        self.scaleFactor: tuple[float, float] = scale_factor
        self.action = tile_click_action

        self.boardTexture = TexturedNode(self.surface)
        self.boardTexture.set_texture(board_texture, linear_scaling=True, scale_by=self.scaleFactor[0])
        self.boardSpriteGroup.add(self.boardTexture)

        self.tileGrid: list[Tile] = self.make_board(scale_factor=self.scaleFactor)
        self.move_board(board_pos)

        self.hitMarkerTexturePath = "../../textures/elements/hit_marker.png"
        self.missMarkerTexturePath = "../../textures/elements/miss_marker.png"
        self.alreadyTexturized: list[Tile] = []

        self.shipReady = False

    def make_board(self, rows: int = 10, columns: int = 10,
                   tile_size: tuple[int, int] = (10, 10), tile_spacing: tuple[int, int] = (10, 10),
                   border_offset: tuple[int, int] = (4, 4), scale_factor: tuple = (1, 1)) -> list[Tile]:
        """
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
                # Create a sprite for each tile. What you'll be interacting with.
                sprite = ButtonNode(self.surface, default_texture=False, z_index=10, action=self.action)
                sprite.re_size((tile_size[0] * scale_factor[0], tile_size[1] * scale_factor[1]))
                sprite.move(((column * tile_spacing[0] + border_offset[0]) * scale_factor[0],
                             (row * tile_spacing[1] + border_offset[1]) * scale_factor[1]))

                self.markersSpriteGroup.add(sprite)

                # Create an instance of the tile-class for each tile. The list with all tiles is what will be sent
                # between players.
                tile: Tile = Tile((column, row), sprite)
                board.append(tile)
        return board

    def move_board(self, new_pos: tuple[int, int]) -> NoReturn:
        centerPoint = midpoint(self.tileGrid[0].sprite.pos, self.tileGrid[-1].sprite.pos)
        offset = (new_pos[0] - centerPoint[0], new_pos[1] - centerPoint[1])

        for i, tile in enumerate(self.tileGrid):
            spritePos = tile.sprite.pos
            moveTo = (spritePos[0] + offset[0], spritePos[1] + offset[1])
            tile.sprite.move(moveTo)
        self.boardTexture.move(new_pos)

    def touch_tile(self, clicked_tile: Tile) -> bool:
        if clicked_tile.touched:
            return False
        clicked_tile.touched = True

    def get_tiles(self) -> list[Tile]:
        return self.tileGrid

    def get_board_sprite_group(self) -> tuple[pg.sprite.Group, pg.sprite.Group]:
        return self.boardSpriteGroup, self.markersSpriteGroup

    def update_textures(self) -> NoReturn:
        for tile in self.tileGrid:
            if not tile.touched:
                continue
            if tile in self.alreadyTexturized:
                continue
            if tile.shipState == 1:
                tile.sprite.set_texture(self.hitMarkerTexturePath, linear_scaling=True,
                                        scale_by=self.scaleFactor[0])
            elif tile.shipState == 0:
                tile.sprite.set_texture(self.missMarkerTexturePath, linear_scaling=True,
                                        scale_by=self.scaleFactor[0])
            self.alreadyTexturized.append(tile)

    def update_touched_tiles(self, other_board) -> NoReturn:
        for i, tile in enumerate(other_board):
            self.tileGrid[i].touched = tile[0]

    def update_ship_state(self, other_board_ship_states) -> NoReturn:
        for tile in other_board_ship_states:
            self.tileGrid[tile].shipState = 1

    def get_occupied_tiles(self) -> list[Tile]:
        occupiedTiles: list = []
        for i, tile in enumerate(self.tileGrid):
            if tile.shipState == 1:
                occupiedTiles.append(i)
        return occupiedTiles

    def get_formatted_tiles(self) -> list[tuple[bool, int]]:
        formattedTiles: list = []
        for tile in self.tileGrid:
            formattedTiles.append((tile.touched, tile.shipState))
        return formattedTiles

    def get_hit(self) -> int:
        hit: int = 0
        for tile in self.tileGrid:
            if tile.touched and tile.shipState == 1:
                hit += 1
        return hit
