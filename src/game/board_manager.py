
class BoardManager:
    def __init__(self):
        self.player1Board: list = []
        self.player1ShipStates: list = []
        self.player2Board: list = []
        self.player2ShipStates: list = []
        self.connectReady: bool = False
        self.p1ShipReady: bool = False
        self.p2ShipReady: bool = False
        self.shipReady: bool = False
        self.playerTurn = 0  # player 0 or 1

    def update_boards(self, player, board):
        if player == 0:
            self.player1Board = board
        elif player == 1:

            self.player2Board = board

    def ready(self, player, ship_states):
        if player == 0:
            self.p1ShipReady = True
            self.player1ShipStates = ship_states
        elif player == 1:
            self.p2ShipReady = True
            self.player2ShipStates = ship_states

        if self.p1ShipReady and self.p2ShipReady:
            self.shipReady = True

    def flip_turn(self):
        print("i am flipping")
        if self.playerTurn == 0:
            self.playerTurn = 1
        elif self.playerTurn == 1:
            self.playerTurn = 0
