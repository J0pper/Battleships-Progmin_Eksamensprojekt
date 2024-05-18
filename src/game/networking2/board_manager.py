
class BoardManager:
    def __init__(self):
        self.player1Board = None
        self.player2Board = None

    def update_boards(self, player, board):
        if player == 0:
            self.player1Board = board
        else:
            self.player2Board = board
