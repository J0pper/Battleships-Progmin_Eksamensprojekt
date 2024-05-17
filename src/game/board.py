
from widgets import *
from objects_and_utils import midpoint


class Tile:
    def __init__(self, index: tuple[int, int], sprite):
        self.index: tuple[int, int] = index
        self.sprite = sprite
        self.shipState = "unoccupied"
        self.hitState = None

    def set_ship_state(self):
        pass

    def set_hit_state(self):
        pass


class Board:
    def __init__(self, surface, board_texture, board_pos, scale_factor, tile_click_action=lambda: 2+2):
        self.surface = surface
        self.boardSpriteGroup = pg.sprite.Group()
        self.scaleFactor = scale_factor
        self.action = tile_click_action

        self.boardTexture = TexturedNode(self.surface)
        self.boardTexture.set_texture(board_texture, linear_scaling=True, scale_by=self.scaleFactor[0])
        self.boardSpriteGroup.add(self.boardTexture)

        self.tileGrid: list[Tile] = self.make_board(scale_factor=self.scaleFactor)
        self.move_board(board_pos)

        self.hitMarkerTexturePath = "../../textures/elements/hit_marker.png"
        self.missMarkerTexturePath = "../../textures/elements/miss_marker.png"
        self.struckTiles: list[tuple[int, int]] = []
        self.struck = 0

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

                self.boardSpriteGroup.add(sprite)

                # Create an instance of the tile-class for each tile. The list with all tiles is what will be sent
                # between players.
                tile: Tile = Tile((column, row), sprite)
                board.append(tile)
        return board

    def move_board(self, new_pos: tuple[int, int]):
        centerPoint = midpoint(self.tileGrid[0].sprite.pos, self.tileGrid[-1].sprite.pos)
        offset = (new_pos[0] - centerPoint[0], new_pos[1] - centerPoint[1])

        for i, tile in enumerate(self.tileGrid):
            spritePos = tile.sprite.pos
            moveTo = (spritePos[0] + offset[0], spritePos[1] + offset[1])
            tile.sprite.move(moveTo)
        self.boardTexture.move(new_pos)

    def add_markers(self, clicked_tile):
        print("hello")
        if clicked_tile.index in self.struckTiles:
            return False
        sprite = TexturedNode(self.surface, default_texture=False)
        sprite.move(clicked_tile.sprite.pos)
        sprite.set_texture(self.hitMarkerTexturePath, linear_scaling=True, scale_by=self.scaleFactor[0])
        if clicked_tile.hitState == "hit":
            pass
        elif clicked_tile.hitState == "miss":
            sprite.set_texture(self.missMarkerTexturePath, linear_scaling=True, scale_by=self.scaleFactor[0])
        self.boardSpriteGroup.add(sprite)

    def get_tiles(self):
        return self.tileGrid

    def get_board_sprite_group(self):
        return self.boardSpriteGroup
