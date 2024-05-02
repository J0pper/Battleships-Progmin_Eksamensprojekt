import pygame as pg
import sys

from widgets import Node
from game_states import set_scene, get_scene, set_all_scenes, TitleScreen, GameScreen

pg.init()

# DISPLAY
RES = pg.display.Info().current_w, pg.display.Info().current_h
surface = pg.display.set_mode((RES[0]/2, RES[1]/2), pg.RESIZABLE)
pg.display.set_caption("Ships & Explosions")
# surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# SPEED/FPS
clock = pg.time.Clock()
FPS = 20

titleScreen = TitleScreen(surface)
gameScreen = GameScreen(surface)
set_all_scenes({"titleScreen": titleScreen, "gameScreen": gameScreen})
set_scene(titleScreen)


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
            zSortedButtons = sorted(Node.registry, key=lambda z_index: z_index[-1])
            for button in zSortedButtons:
                if button[0].on_click(mousePos):
                    break

    get_scene().draw()

    pg.display.flip()

pg.quit()
sys.exit()
