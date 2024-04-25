import pygame as pg

from widgets import Button


pg.init()

res = [800, 800]
surface = pg.display.set_mode(res)

clock = pg.time.Clock()
FPS = 20

newButton = Button(surface, [100, 100], [100, 100], (255, 0, 0))


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

    newButton.draw_button()
    newButton.on_click()
    pg.display.flip()

pg.quit()
