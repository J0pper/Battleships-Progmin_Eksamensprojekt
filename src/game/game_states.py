from widgets import Button


class GameStateManager:
    def __init__(self, current_state):
        self.currentState = current_state

    def get_state(self):
        return self.currentState

    def set_state(self, new_state):
        self.currentState = new_state


class TitleScreen:
    def __init__(self, surface):
        self.background = Button(surface, [320, 180], [0, 0], z_index=0)
        self.title = Button(surface, [320, 180], [0, 0], z_index=1)
        self.startButton = Button(surface, [320, 180], [0, 0], z_index=2)

        self.background.clickable = False
        self.title.clickable = False

        res = surface.get_size()
        scaleFactor = [res[0] / 320, res[1] / 180]

        self.background.set_texture("../textures/title_screen/background.png", linear_scaling=True, scale_by=scaleFactor[0], prioritize_texture_size=True)
        self.title.set_texture("../textures/title_screen/start_button.png", linear_scaling=True, scale_by=scaleFactor[0],  prioritize_texture_size=True)
        self.startButton.set_texture("../textures/title_screen/title.png", linear_scaling=True, scale_by=scaleFactor[0],  prioritize_texture_size=True)

    def draw(self):
        self.background.draw(with_texture=True)
        self.title.draw(with_texture=True)
        self.startButton.draw(with_texture=True)


class Table:
    def __init__(self):
        raise NotImplementedError("Class Table is missing code")
