import pygame
import sys
from pygame.locals import *
from constants import *
import random


class RightToLeftVerticalCollisionLine:
    """ This is a vertical which allows balls incoming from the right ot re-bounce to the left. """

    def __init__(self, length, x, y, surface):
        """
        The vertical line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the coordinates to act on the walls to be blit
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.surface = surface
        self.colliding = False
        self.number_collisions = 0

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length \
                and ball_object.centre_x + ball_object.radius >= self.top_x >= ball_object.centre_x:
            ball_object.velocity[0] = -ball_object.velocity[0]
            self.colliding = True
            self.number_collisions += 1
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_x + ball_object.radius >= self.top_x):
            self.colliding = False

    def update(self):

        self.check_collision(ball)
        self.draw()


class LeftToRightVerticalCollisionLine:
    """ This is a vertical line which will act as the paddle to test collisions. """

    def __init__(self, length, x, y, surface):
        """
        The vertical line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
                :param surface: The surface on which the coordinates to act on the walls to be blit
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.surface = surface
        self.colliding = False
        self.number_collisions = 0

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length and \
                ball_object.centre_x - ball_object.radius <= self.top_x <= ball_object.centre_x:
            ball_object.velocity[0] = -ball_object.velocity[0]
            self.colliding = True
            self.number_collisions += 1
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_x - ball_object.radius <= self.top_x <= ball_object.centre_x):
            self.colliding = False

    def update(self):
        self.check_collision(ball)
        self.draw()


class DownToUpHorizontalCollisionLine:
    """ This is a horizontal line which will act as the paddle to test collisions. """

    def __init__(self, length, x, y, surface, change_colliding_object_velocity=None):
        """
        The horizontal line will be 1 px long for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the coordinates to act on the walls to be blit
        """
        self.length = length
        self.left_x, self.left_y = x, y
        self.surface = surface
        self.change_colliding_object_velocity = change_colliding_object_velocity
        self.colliding = False
        self.number_collisions = 0

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.left_x, self.left_y), (self.left_x + self.length, self.left_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.left_x + self.length \
                and ball_object.centre_y + ball_object.radius >= self.left_y >= ball_object.centre_y:
            if not self.change_colliding_object_velocity:
                ball_object.velocity[1] = -ball_object.velocity[1]
            else:
                ball_object.velocity[0], ball_object.velocity[1] = random.uniform(-1.2, 1.2), -1
            self.colliding = True
            self.number_collisions += 1
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.left_x + self.length) \
                or not (ball_object.centre_y + ball_object.radius >= self.left_y):
            self.colliding = False

    def update(self):
        self.check_collision(ball)
        self.draw()


class UpToDownHorizontalCollisionLine:
    """ This is a horizontal line which allows balls income from beneath to re-bounce back down """

    def __init__(self, length, x, y, surface):
        """
        The horizontal line will be 1 px wide for now
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the coordinates to act on the walls to be blit
        """
        self.length = length
        self.left_x, self.left_y = x, y
        self.surface = surface
        self.colliding = False
        self.number_collisions = 0

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.left_x, self.left_y), (self.left_x + self.length, self.left_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.left_x + \
                self.length and ball_object.centre_y - ball_object.radius <= self.left_y <= ball_object.centre_y:
            ball_object.velocity[1] = -ball_object.velocity[1]
            self.colliding = True
            self.number_collisions += 1
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.left_x + self.length) \
                or not (ball_object.centre_y - ball_object.radius <= self.left_y):
            self.colliding = False

    def update(self):
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

    def update(self):
        dx, dy = pygame.Vector2.normalize(self.velocity)
        self.centre_x += dx * self.time
        self.centre_y += dy * self.time
        pygame.draw.circle(screen, GREEN, (round(self.centre_x), round(self.centre_y)), self.radius)


class Brick:
    """ This will be a rectangle where collisions with a ball is possible """

    def __init__(self, x, y, length, height, surface):
        """
        :param x: x coord of the top left corner
        :param y: y coord of the top right corner
        :param length: horizontal length
        :param height: vertical length
        """
        self.x, self.y = x, y
        self.length, self.height = length, height
        self.surface = surface

        self.right_wall = LeftToRightVerticalCollisionLine(self.height, self.x + self.length, self.y, screen)
        self.left_wall = RightToLeftVerticalCollisionLine(self.height, self.x, self.y, screen)
        self.top_wall = DownToUpHorizontalCollisionLine(self.length, self.x, self.y, screen)
        self.bottom_wall = UpToDownHorizontalCollisionLine(self.length, self.x, self.y + self.height, screen)

    def draw(self):
        pygame.draw.rect(self.surface, RED, (self.x, self.y, self.length, self.height))

    def update(self):
        self.draw()
        self.left_wall.update()
        self.right_wall.update()
        self.top_wall.update()
        self.bottom_wall.update()


class Paddle:
    def __init__(self, x, y, length, height, surface):
        """
        :param x: x coord of the top left corner
        :param y: y coord of the top right corner
        :param length: horizontal length
        :param height: vertical length
        """
        self.x, self.y = x, y
        self.length, self.height = length, height
        self.surface = surface

        self.right_wall = LeftToRightVerticalCollisionLine(self.height, self.x + self.length, self.y, screen)
        self.left_wall = RightToLeftVerticalCollisionLine(self.height, self.x, self.y, screen)
        self.top_wall = DownToUpHorizontalCollisionLine(self.length, self.x, self.y, screen, True)
        self.bottom_wall = UpToDownHorizontalCollisionLine(self.length, self.x, self.y + self.height, screen)

    def draw(self):
        pygame.draw.rect(self.surface, RED, (self.x, self.y, self.length, self.height))

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.x = mouse_x - self.length / 2
        self.top_wall.left_x = mouse_x - self.length / 2
        self.left_wall.top_x = mouse_x - self.length / 2
        self.bottom_wall.left_x = mouse_x - self.length / 2
        self.right_wall.top_x = mouse_x + self.length / 2

        self.draw()
        self.left_wall.update()
        self.right_wall.update()
        self.top_wall.update()
        self.bottom_wall.update()


root = pygame.display.set_mode((1020, 624))
clock = pygame.time.Clock()

root.fill(GRAY)

screen = pygame.Surface((996, 600))
root.blit(screen, (12, 12))

screen_left_wall = LeftToRightVerticalCollisionLine(600, 0, 0, screen)
screen_right_wall = RightToLeftVerticalCollisionLine(600, 995, 0, screen)
screen_top_wall = UpToDownHorizontalCollisionLine(996, 0, 0, screen)

ball = Ball(600, 500, 10, (-10, -10), 3)
paddle = Paddle(300, 475, 200, 50, screen)

bricks = []

for j in range(1, 9):
    for i in range(1, 16):
        bricks.append(Brick(-60 + 66*i, -6 + 36*j, BRICK_LENGTH, BRICK_HEIGHT, screen))


def update_screen():
    screen.fill(BLACK)
    screen_right_wall.update()
    screen_left_wall.update()
    screen_top_wall.update()
    paddle.update()
    for brick in bricks:
        brick.update()
        if any([brick.bottom_wall.number_collisions, brick.top_wall.number_collisions,
                brick.left_wall.number_collisions, brick.right_wall.number_collisions]):
            bricks.remove(bricks[bricks.index(brick)])
    ball.update()
    root.blit(screen, (12, 12))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    update_screen()
    pygame.display.update()
    clock.tick(50)
