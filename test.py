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
        x_new, y_new = round(self.x), round(self.y)
        pygame.draw.circle(root, RED, (x_new, y_new), self.radius)

    def check_for_collision_with_paddle(self, paddle_object):
        shortest_possible_distance_between_ball_paddle = (paddle_object.height / 2) + self.radius
        if (paddle_object.centre_y - self.y) <= shortest_possible_distance_between_ball_paddle:
            self.colliding = True
            self.velocity[1] = -self.velocity[1]



class Paddle:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.centre_x = self.x + (self.width / 2)
        self.centre_y = self.y + (self.height / 2)

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
    ball.check_for_collision_with_paddle(paddle)
    paddle.update()
    ball.update()
    pygame.display.update()
    clock.tick(30)
