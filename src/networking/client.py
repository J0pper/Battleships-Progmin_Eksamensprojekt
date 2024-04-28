import pygame
from network import Network
import sys

print("I GOT THIS FAR")

RESOLUTION: list[int, int] = [500, 500]
window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(position: str):
    position = position.split(",")
    return int(position[0]), int(position[1])


def make_pos(position: tuple):
    return f"{position[0]}, {position[1]}"


def redraw_window(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    network = Network()
    startPos = read_pos(network.get_pos())
    player = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    opponent = Player(0, 0, 100, 100, (255, 0, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        opponent.x, opponent.y = read_pos(network.send(make_pos((player.x, player.y))))
        opponent.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.move()
        redraw_window(window, player, opponent)

    pygame.quit()
    sys.exit()


main()
