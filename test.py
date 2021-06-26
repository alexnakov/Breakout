import pygame
import sys
from pygame.locals import *
from constants import *


class HorizontalCollisionOuterSurface:
    """ This is a horizontal line which will act as the paddle to test collisions. """

    def __init__(self, length, x, y):
        """
        The horizontal line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        """
        self.length = length
        self.left_x, self.left_y = x, y
        self.colliding = False

        self.right_x, self.right_y = self.length + self.left_x, self.left_y
        self.centre_x = (self.right_x + self.left_x) / 2

    def draw(self):
        pygame.draw.line(root, BLUE, (self.left_x, self.left_y), (self.right_x, self.right_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.right_x \
                and ball_object.bottom_y >= self.left_y:  # Any y coord will do
            ball_object.velocity[1] = -ball_object.velocity[1]
            self.colliding = True
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.right_x) \
                or not (ball_object.bottom_y >= self.left_y):
            self.colliding = False

    def update(self):
        self.right_x, self.right_y = self.length + self.left_x, self.left_y
        self.centre_x = (self.right_x + self.left_x) / 2

        mouse_x = pygame.mouse.get_pos()[0]
        self.left_x = mouse_x - self.length / 2

        self.check_collision(ball)
        self.draw()


class Ball:
    """ The ball which will be flying and colliding with the bricks & paddle """

    def __init__(self, centre_x, centre_y, radius, initial_velocity, time):
        """
        :param tuple initial_velocity: Starting velocity of the ball as tuple of x and y components.
                                       The size of this tuple does not affect the actual speed of the ball.
        :param float time: The faster the time, the faster the ball move
        """
        self.radius = radius
        self.centre_x, self.centre_y = centre_x, centre_y
        self.time = time
        self.velocity = pygame.Vector2(initial_velocity)

        self.bottom_y = self.centre_y + self.radius
        self.top_y = self.centre_y - self.radius
        self.right_x = self.centre_x + self.radius
        self.left_x = self.centre_x - self.radius

    def draw(self):
        pygame.draw.circle(root, RED, (self.centre_x, self.centre_y), self.radius)

    def update(self):
        self.bottom_y = self.centre_y + self.radius
        self.top_y = self.centre_y - self.radius
        self.right_x = self.centre_x + self.radius
        self.left_x = self.centre_x - self.radius

        dx, dy = pygame.Vector2.normalize(self.velocity)
        # distance = speed * time
        self.centre_x += dx * self.time
        self.centre_y += dy * self.time
        x_new, y_new = round(self.centre_x), round(self.centre_y)
        pygame.draw.circle(root, RED, (x_new, y_new), self.radius)


root = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
ball = Ball(200, 200, 20, (10, 20), 3)
collision_line = HorizontalCollisionOuterSurface(100, 350, 600)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Screen updates here
    root.fill(BLACK)

    collision_line.update()
    ball.update()

    pygame.display.update()
    clock.tick(90)
