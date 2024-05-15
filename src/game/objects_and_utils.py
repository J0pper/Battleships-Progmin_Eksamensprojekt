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


class Vec:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.vec: list[int] = [x, y]

    def __sub__(self, vec2):
        return [self.vec[0] - vec2[0], self.vec[1] - vec2[1]]

    def __str__(self):
        return f"x: ({self.x}, y: {self.y})"
