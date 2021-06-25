import pygame
import sys
from pygame.locals import *
from constants import *


class Ball:
    def __init__(self, radius, centre, initial_velocity):
        self.radius = radius
        self.x, self.y = centre
        self.velocity = pygame.Vector2(initial_velocity)

    def update(self):
        normalised_vector = pygame.Vector2.normalize(self.velocity)
        dx, dy = normalised_vector[0], normalised_vector[1]
        self.x += dx
        self.y += dy
        x_new, y_new = int(self.x), int(self.y)
        pygame.draw.circle(root, RED, (x_new, y_new), self.radius)



class Paddle:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def update(self):
        pygame.draw.rect(root, NAVY, Rect(self.x, self.y, self.width, self.height))


root = pygame.display.set_mode((800, 800))
paddle = Paddle(350,650,200,50)
ball = Ball(5, (5,5), (0.3,0.3))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    root.fill(BLACK)
    paddle.update()
    ball.update()
    pygame.display.update()
