import pygame as pg
import sys

from widgets import Button
from game_states import TitleScreen

pg.init()

# DISPLAY
surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# SPEED/FPS
clock = pg.time.Clock()
FPS = 20


# BUTTONS
newButton: Button = Button(surface, [100, 100], [100, 100], z_index=0)
newButton.set_texture("../textures/test/Marck_SUCK.png", linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)
newButton2: Button = Button(surface, [100, 100], [300, 100], z_index=1)
newButton2.set_texture("../textures/test/Marck_SUCK.png", linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)
newButton3: Button = Button(surface, [100, 100], [500, 100], z_index=2)
newButton3.set_texture("../textures/test/Marck_SUCK.png", linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)

titleScreen = TitleScreen(surface)

running = True
while running:

    surface.fill((34, 34, 34))
    clock.tick(FPS)

    # Listen for key events to QUIT the game and close upgrading screen.
    for event in pg.event.get():
        # QUIT GAME
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            zSortedButtons = sorted(Button.registry, key=lambda z_index: z_index[1])
            for button in reversed(zSortedButtons):
                if button[0].on_click(mousePos):
                    break

    # DRAW BUTTONS
    """
    newButton.draw(with_texture=True)
    newButton2.draw(with_texture=True)
    newButton3.draw(with_texture=True)
    """

    titleScreen.draw()

    pg.display.flip()

pg.quit()
sys.exit()


