import pygame as pg

from widgets import Button


pg.init()

res = [320, 180]
surface = pg.display.set_mode(res)

clock = pg.time.Clock()
FPS = 20

newButton = Button(surface, [100, 100], [100, 100])
newButton.set_texture("../textures/test/Marck_SUCK.png", linear_scaling=True, scale_by=(0.5))

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

    newButton.draw(with_texture=True)

    pg.display.flip()

pg.quit()
