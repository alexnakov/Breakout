import pygame
import sys
from pygame.locals import *
from constants import *


root = pygame.display.set_mode((1020, 624))
root.fill(GRAY)

screen = pygame.Surface((996, 600))

box = pygame.Surface((60, 30))
box.fill(RED)

for j in range(1, 9):
    for i in range(1, 16):
        screen.blit(box, (-60 + 66*i, -6 + 36*j))

root.blit(screen, (12, 12))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
