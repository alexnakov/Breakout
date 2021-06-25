import pygame
import sys
from pygame.locals import *
from constants import *


root = pygame.display.set_mode((924, 624))
root.fill(GRAY)

screen = pygame.Surface((900, 600))

box = pygame.Surface((90, 50))
box.fill(RED)

for i in range(1, 9):
    screen.blit(box, (-90 + 100*i, 24))

root.blit(screen, (12, 12))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()


