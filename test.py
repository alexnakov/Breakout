import pygame
import sys
from pygame.locals import *
from constants import *


class Ball:
    def __init__(self, x, y, radius, initial_velocity, time):
        self.x, self.y = x, y
        self.radius = radius
        self.velocity = pygame.Vector2(initial_velocity)
        self.time = time
        self.colliding = False

    def draw(self):
        pygame.draw.circle(root, RED, (self.x, self.y), self.radius)

    def update(self):
        normalised_vector = pygame.Vector2.normalize(self.velocity)
        dx, dy = normalised_vector[0], normalised_vector[1]
        self.x += dx * self.time
        self.y += dy * self.time
        x_new, y_new = int(self.x), int(self.y)
        pygame.draw.circle(root, RED, (x_new, y_new), self.radius)


class Paddle:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def update(self):
        pygame.draw.rect(root, NAVY, Rect(self.x, self.y, self.width, self.height))


root = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

paddle = Paddle(350, 650, 200, 50)
ball = Ball(400, 400, 10, (0, 10), 5)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    root.fill(BLACK)
    paddle.update()
    ball.update()
    pygame.display.update()
    clock.tick(30)
