class GameStateManager:
    def __init__(self, current_state):
        self.currentState = current_state

    def get_state(self):
        return self.currentState

    def set_state(self, new_state):
        self.currentState = new_state


class TitleScreen:
    def __init__(self):
        raise NotImplementedError("Class TitleScreen is missing code")


class Table:
    def __init__(self):
        raise NotImplementedError("Class Table is missing code")