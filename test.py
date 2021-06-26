import pygame
import sys
from pygame.locals import *
from constants import *


class RightToLeftVerticalCollisionLine:
    """ This is a vertical which allows balls incoming from the right ot re-bounce to the left. """

    def __init__(self, length, x, y):
        """
        The vertical line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.colliding = False

    def draw(self):
        pygame.draw.line(root, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length \
                and ball_object.centre_x + ball_object.radius >= self.top_x:
            ball_object.velocity[0] = -ball_object.velocity[0]
            self.colliding = True
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_x + ball_object.radius >= self.top_y):
            self.colliding = False

    def update(self):

        self.check_collision(ball)
        self.draw()


class LeftToRightVerticalCollisionLine:
    """ This is a vertical line which will act as the paddle to test collisions. """

    def __init__(self, length, x, y):
        """
        The vertical line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.colliding = False

    def draw(self):
        pygame.draw.line(root, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length \
                and ball_object.centre_x - ball_object.radius <= self.top_x:
            ball_object.velocity[0] = -ball_object.velocity[0]
            self.colliding = True
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_y + ball_object.radius >= self.top_y):
            self.colliding = False

    def update(self):

        self.check_collision(ball)
        self.draw()


class DownToUpHorizontalCollisionLine:
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

    def draw(self):
        pygame.draw.line(root, BLUE, (self.left_x, self.left_y), (self.left_x + self.length, self.left_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.left_x + self.length \
                and ball_object.centre_y + ball_object.radius >= self.left_y:
            ball_object.velocity[1] = -ball_object.velocity[1]
            self.colliding = True
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.left_x + self.length) \
                or not (ball_object.centre_y + ball_object.radius >= self.left_y):
            self.colliding = False

    def update(self):
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

    def draw(self):
        pygame.draw.circle(root, RED, (self.centre_x, self.centre_y), self.radius)

    def update(self):
        dx, dy = pygame.Vector2.normalize(self.velocity)
        # distance = speed * time
        self.centre_x += dx * self.time
        self.centre_y += dy * self.time
        x_new, y_new = round(self.centre_x), round(self.centre_y)
        pygame.draw.circle(root, RED, (x_new, y_new), self.radius)


root = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
ball = Ball(200, 35, 10, (10, 10), 2)

v1 = LeftToRightVerticalCollisionLine(500, 200, 50)
v2 = RightToLeftVerticalCollisionLine(500, 250, 50)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Screen updates here
    root.fill(BLACK)

    v1.update()
    v2.update()

    ball.update()

    pygame.display.update()
    clock.tick(90)
