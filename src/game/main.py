import pygame as pg
import sys

from widgets import Node, Dims, TexturedDims
from game_states import set_scene, get_scene, set_all_scenes, TitleScreen, GameScreen

pg.init()

# DISPLAY
RES = pg.display.Info().current_w, pg.display.Info().current_h
surface = pg.display.set_mode((RES[0], RES[1]), pg.RESIZABLE)
pg.display.set_caption("Ships & Explosions")
# surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# SPEED/FPS
clock = pg.time.Clock()
FPS = 200

titleScreen = TitleScreen(surface)
gameScreen = GameScreen(surface)
set_all_scenes({"titleScreen": titleScreen, "gameScreen": gameScreen})
set_scene(titleScreen)

nyDims = Dims(surface)
nyTexturedDims = TexturedDims(surface)
nyTexturedDims.set_texture("../../textures/test/Marck_SUCK.png")

vel = 1

running = True
while running:
    surface.fill((34, 34, 34))

    # clock.tick(FPS)

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

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        nyTexturedDims.pos[0] -= vel

    if keys[pg.K_RIGHT]:
        nyTexturedDims.pos[0] += vel

    if keys[pg.K_UP]:
        nyTexturedDims.pos[1] -= vel

    if keys[pg.K_DOWN]:
        nyTexturedDims.pos[1] += vel

    get_scene().draw()
    nyDims.draw()
    nyTexturedDims.pos = pg.mouse.get_pos()
    nyTexturedDims.texture_draw()
    pg.display.flip()

pg.quit()
sys.exit()
