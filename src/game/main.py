import sys
from game_states import *

pg.init()
pg.font.init()

# DISPLAY
RES = pg.display.Info().current_w, pg.display.Info().current_h
surface = pg.display.set_mode((RES[0] / 2, RES[1] / 2), pg.RESIZABLE)
print(RES)
pg.display.set_caption("Ships & Explosions")
# surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# SPEED/FPS
clock = pg.time.Clock()
FPS = 200

#  DEFINING SCREENS
titleScreen = TitleScreen(surface)
connectScreen = ConnectScreen(surface)
gameScreen = GameScreen(surface)
set_all_scenes({"titleScreen": titleScreen, "connectScreen": connectScreen, "gameScreen": gameScreen})
set_scene(titleScreen)


#  GAME RUN
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
            zSortedButtons = sorted(ButtonNode.registry, key=lambda z_index: z_index[1], reverse=True)
            for button in zSortedButtons:
                if button[0].on_click(mousePos):
                    break

    get_scene().draw()
    pg.display.flip()

pg.quit()
sys.exit()
