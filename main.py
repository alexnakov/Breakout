import pygame
import sys
from pygame.locals import *
from constants import *


class RedBrick:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height


class Ball:
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x, self.y = x, y


class Paddle:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height


root = pygame.display.set_mode((1020, 624))
root.fill(GRAY)

screen = pygame.Surface((996, 600))

box = pygame.Surface((60, 30))
box.fill(RED)

paddle = pygame.Surface((180, 20))
paddle.fill(NAVY)

for j in range(1, 9):
    for i in range(1, 16):
        screen.blit(box, (-60 + 66*i, -6 + 36*j))

screen.blit(paddle, (500, 560))

root.blit(screen, (12, 12))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()


