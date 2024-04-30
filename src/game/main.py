import pygame as pg
import sys

from widgets import Node
from game_states import TitleScreen

pg.init()

# DISPLAY
RES = pg.display.Info().current_w, pg.display.Info().current_h
surface = pg.display.set_mode((RES[0]/2, RES[1]/2), pg.RESIZABLE)
pg.display.set_caption("Ships & Explosions")
# surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)

# SPEED/FPS
clock = pg.time.Clock()
FPS = 20


# NodeS
newButton: Node = Node(surface, [100, 100], [100, 100], z_index=0)
newButton.set_texture("../../textures/test/Marck_SUCK.png",
                      linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)
newButton2: Node = Node(surface, [100, 100], [300, 100], z_index=1)
newButton2.set_texture("../../textures/test/Marck_SUCK.png",
                       linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)
newButton3: Node = Node(surface, [100, 100], [500, 100], z_index=2)
newButton3.set_texture("../../textures/test/Marck_SUCK.png",
                       linear_scaling=True, scale_by=0.5, prioritize_texture_size=True)

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
            zSortedButtons = sorted(Node.registry, key=lambda z_index: z_index[1])
            for Node in reversed(zSortedButtons):
                if Node[0].on_click(mousePos):
                    break

    # DRAW NodeS
    """
    newButton.draw(with_texture=True)
    newButton2.draw(with_texture=True)
    newButton3.draw(with_texture=True)
    """

    titleScreen.draw()

    pg.display.flip()

pg.quit()
sys.exit()
