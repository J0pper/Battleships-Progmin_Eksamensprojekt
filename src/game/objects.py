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