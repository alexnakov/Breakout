import pygame
import sys
from pygame.locals import *
from constants import *
import random
pygame.init()


class Button:
    """ This template will be used to create buttons """
    def __init__(self, super_surface, x, y, path_unclicked, path_clicked):
        """
        :param super_surface: The surface on which the button will be blit on
        :param x: the x-coord of the top-left corner of the button
        :param y: the y-coord of the top-left corner of the button
        :param path_unclicked: The path to the image of the button in its normal state
        :param path_clicked:  The path to the image of the button when is clicked
        """
        self.super_surf = super_surface
        self.x, self.y = x, y
        self.unclicked_img = pygame.image.load(path_unclicked)
        self.clicked_img = pygame.image.load(path_clicked)
        self.length, self.height = self.unclicked_img.get_size()
        self.clicked = False
        self.super_surf.blit(self.unclicked_img, (self.x, self.y))

    def collide_point(self, x, y):
        if self.x <= x <= self.x + self.length and self.y <= y <= self.y + self.height:
            return True
        else:
            return False

    def update(self, events):
        self.clicked = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.collide_point(mouse_x, mouse_y):
                    self.super_surf.blit(self.clicked_img, (self.x, self.y))
            elif event.type == MOUSEBUTTONUP:
                if self.collide_point(mouse_x, mouse_y):
                    self.super_surf.blit(self.unclicked_img, (self.x, self.y))
                    self.clicked = True
            elif True:
                self.super_surf.blit(self.unclicked_img, (self.x, self.y))


class RightToLeftVerticalCollisionLine:
    """ This is a vertical line which allows balls incoming from the left ot re-bounce back. """

    def __init__(self, length, x, y, surface):
        """
        :param length: Length of line in pixels
        :param x: The x coord of the top end
        :param y: The y coord of the top end
        :param surface: The surface on which the colliding object acts by
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.surface = surface
        self.colliding = False

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        """ Change the ball's velocity if the ball intersects the line from the left """
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length \
                and ball_object.centre_x + ball_object.radius >= self.top_x >= ball_object.centre_x:
            ball_object.velocity[0] = -abs(ball_object.velocity[0])
            self.colliding = True
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_x + ball_object.radius >= self.top_x):
            self.colliding = False

    def update(self):
        """ To be called once every game loop """
        self.check_collision(ball)


class LeftToRightVerticalCollisionLine:
    """ This is a vertical line which allows incoming balls from the right to re-bounce back"""

    def __init__(self, length, x, y, surface):
        """
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the colliding object acts by
        """
        self.length = length
        self.top_x, self.top_y = x, y
        self.surface = surface
        self.colliding = False

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.top_x, self.top_y), (self.top_x, self.top_y + self.length))

    def check_collision(self, ball_object):
        if not self.colliding and self.top_y <= ball_object.centre_y <= self.top_y + self.length and \
                ball_object.centre_x - ball_object.radius <= self.top_x <= ball_object.centre_x:
            ball_object.velocity[0] = abs(ball_object.velocity[0])
            self.colliding = True
        elif self.colliding and not (self.top_y <= ball_object.centre_y <= self.top_y + self.length) \
                or not (ball_object.centre_x - ball_object.radius <= self.top_x <= ball_object.centre_x):
            self.colliding = False

    def update(self):
        self.check_collision(ball)


class DownToUpHorizontalCollisionLine:
    """ This is a horizontal line which allows balls incoming from above to re-bounce back up. """

    def __init__(self, length, x, y, surface, change_colliding_object_velocity=None):
        """
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the colliding object acts by
        """
        self.length = length
        self.left_x, self.left_y = x, y
        self.surface = surface
        self.change_colliding_object_velocity = change_colliding_object_velocity
        self.colliding = False

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.left_x, self.left_y), (self.left_x + self.length, self.left_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.left_x + self.length \
                and ball_object.centre_y + ball_object.radius >= self.left_y >= ball_object.centre_y:
            if not self.change_colliding_object_velocity:
                ball_object.velocity[1] = -abs(ball_object.velocity[1])
            else:
                ball_object.velocity[0], ball_object.velocity[1] = random.uniform(-1.2, 1.2), -1
            self.colliding = True
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.left_x + self.length) \
                or not (ball_object.centre_y + ball_object.radius >= self.left_y):
            self.colliding = False

    def update(self):
        self.check_collision(ball)


class UpToDownHorizontalCollisionLine:
    """ This is a horizontal line which allows balls incoming from beneath to re-bounce back down """

    def __init__(self, length, x, y, surface):
        """
        :param length: Length of line in pixels
        :param x: The x coord of the left end
        :param y: The y coord of the left end
        :param surface: The surface on which the colliding object acts by
        """
        self.length = length
        self.left_x, self.left_y = x, y
        self.surface = surface
        self.colliding = False

    def draw(self):
        pygame.draw.line(self.surface, YELLOW, (self.left_x, self.left_y), (self.left_x + self.length, self.left_y))

    def check_collision(self, ball_object):
        if not self.colliding and self.left_x <= ball_object.centre_x <= self.left_x + \
                self.length and ball_object.centre_y - ball_object.radius <= self.left_y <= ball_object.centre_y:
            ball_object.velocity[1] = abs(ball_object.velocity[1])
            self.colliding = True
        elif self.colliding and not (self.left_x <= ball_object.centre_x <= self.left_x + self.length) \
                or not (ball_object.centre_y - ball_object.radius <= self.left_y):
            self.colliding = False

    def update(self):
        self.check_collision(ball)


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
        pygame.draw.circle(screen, FUCHSIA, (round(self.centre_x), round(self.centre_y)), self.radius)


class Brick:
    """ This will be a rectangle where collisions with a ball is possible """
    number_red_bricks = 30  # To be used for rewarding when a player eliminates a colour
    number_orange_bricks = 30
    number_yellow_bricks = 30
    number_green_bricks = 30

    def __init__(self, x, y, length, height, surface, colour):
        """
        :param x: x coord of the top left corner
        :param y: y coord of the top right corner
        :param length: horizontal length
        :param height: vertical length
        """
        self.x, self.y = x, y
        self.length, self.height = length, height
        self.surface = surface
        self.colour = colour
        brick_colours = [GREEN, YELLOW, ORANGE, RED]
        self.reward_points = (brick_colours.index(self.colour) + 1) * 5

        self.right_wall = LeftToRightVerticalCollisionLine(self.height, self.x + self.length, self.y, screen)
        self.left_wall = RightToLeftVerticalCollisionLine(self.height, self.x, self.y, screen)
        self.top_wall = DownToUpHorizontalCollisionLine(self.length, self.x, self.y, screen)
        self.bottom_wall = UpToDownHorizontalCollisionLine(self.length, self.x, self.y + self.height, screen)

    def draw(self):
        pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.length, self.height))

    def update(self):
        self.draw()
        self.left_wall.update()
        self.right_wall.update()
        self.top_wall.update()
        self.bottom_wall.update()

    def remove_colour(self):
        if self.colour == RED and Brick.number_red_bricks is not None:
            Brick.number_red_bricks -= 1
        elif self.colour == ORANGE and Brick.number_orange_bricks is not None:
            Brick.number_orange_bricks -= 1
        elif self.colour == YELLOW and Brick.number_yellow_bricks is not None:
            Brick.number_yellow_bricks -= 1
        elif self.colour == GREEN and Brick.number_green_bricks is not None:
            Brick.number_green_bricks -= 1

    @staticmethod
    def count_bricks_left():
        """ Gives points to the player for every colour eliminated """
        if Brick.number_green_bricks is not None:
            if Brick.number_green_bricks <= 0:
                Brick.number_green_bricks = None
                return 250
            else:
                return 0
        elif Brick.number_yellow_bricks is not None:
            if Brick.number_yellow_bricks <= 0:
                Brick.number_yellow_bricks = None
                return 500
            else:
                return 0
        elif Brick.number_orange_bricks is not None:
            if Brick.number_orange_bricks <= 0:
                Brick.number_orange_bricks = None
                return 750
            else:
                return 0
        elif Brick.number_red_bricks is not None:
            if Brick.number_red_bricks <= 0:
                Brick.number_red_bricks = None
                return 1000
            else:
                return 0
        else:
            return 0


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

        # A paddle is a box made from collision walls
        self.right_wall = LeftToRightVerticalCollisionLine(self.height, self.x + self.length, self.y, screen)
        self.left_wall = RightToLeftVerticalCollisionLine(self.height, self.x, self.y, screen)
        self.top_wall = DownToUpHorizontalCollisionLine(self.length, self.x, self.y, screen, True)
        self.bottom_wall = UpToDownHorizontalCollisionLine(self.length, self.x, self.y + self.height, screen)

    def draw(self):
        pygame.draw.rect(self.surface, BLUE, (self.x, self.y, self.length, self.height))

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.x = mouse_x - self.length / 2  # Moves the x position for the rectangle

        self.top_wall.left_x = mouse_x - self.length / 2  # Moves the x position for the Collision Walls
        self.left_wall.top_x = mouse_x - self.length / 2
        self.bottom_wall.left_x = mouse_x - self.length / 2
        self.right_wall.top_x = mouse_x + self.length / 2

        self.draw()
        self.left_wall.update()
        self.right_wall.update()
        self.top_wall.update()
        self.bottom_wall.update()


def main_menu():
    """ When the game is run, this menu is the first thing displayed. Rules of the game could be added here """
    background = pygame.image.load("startMenuBackground.png")
    main_menu_surface = pygame.Surface((1020, 654))
    start_button = Button(background, 510 - 150, 400, "playButton_U.png", "playButton_C.png")
    root.blit(main_menu_surface, (0, 0))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        start_button.update(events)
        main_menu_surface.blit(background, (0, 0))
        root.blit(main_menu_surface, (0, 0))
        if start_button.clicked:
            return
        pygame.display.update()


if __name__ == '__main__':
    font1 = pygame.font.SysFont("Comic Sans MS", 30)
    font2 = pygame.font.SysFont("Comic Sans MS", 70)
    font3 = pygame.font.SysFont("Comic Sans MS", 50)

    root = pygame.display.set_mode(ROOT_SIZE)
    clock = pygame.time.Clock()

    while True:
        main_menu()

        # Game set up
        root.fill(GRAY)
        screen = pygame.Surface(SCREEN_SIZE)
        root.blit(screen, (WALL_WIDTH, WALL_WIDTH))
        screen_left_wall = LeftToRightVerticalCollisionLine(SCREEN_HEIGHT, 0, 0, screen)
        screen_right_wall = RightToLeftVerticalCollisionLine(SCREEN_HEIGHT, SCREEN_WIDTH - 1, 0, screen)
        screen_top_wall = UpToDownHorizontalCollisionLine(SCREEN_WIDTH, 0, 0, screen)
        ball = Ball(600, 500, 10, (-10, -10), 5)
        paddle = Paddle(300, 600, 200, 20, screen)
        bricks = []
        loop_colour = [RED, RED, ORANGE, ORANGE, YELLOW, YELLOW, GREEN, GREEN]
        for j in range(1, 9):
            for i in range(1, 16):
                bricks.append(Brick(-60 + 66*i, 24 + 36*j, BRICK_LENGTH, BRICK_HEIGHT, screen, loop_colour[j-1]))
        lives = 5  # TODO change this later for actual game
        points = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if ball.centre_y > SCREEN_HEIGHT:
                lives -= 1
                if lives == 0:
                    def game_over_menu():
                        """ Screen to be displayed when player loses all lives """
                        player_score = font1.render(f"{points}", True, WHITE)
                        game_over_surface = pygame.image.load("gameOverBackground.png")
                        start_again_button = Button(game_over_surface, 289, 475, "startAgain_U.png",
                                                    "startAgain_C.png")
                        game_over_surface.blit(player_score, (875, 150))

                        while True:
                            events = pygame.event.get()
                            for event in events:
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()

                            start_again_button.update(events)
                            root.blit(game_over_surface, (0, 0))
                            if start_again_button.clicked:
                                return
                            pygame.display.update()
                    break
                ball.centre_y = 500
                ball.centre_x = random.randint(100, 900)
                ball.velocity[0], ball.velocity[1] = random.uniform(-1.2, 1.2), -1
            lives_text_surf = font1.render(f"Lives left: {lives}", True, WHITE, BLACK)
            points_text_surf = font1.render(f"Points: {points}", True, WHITE, BLACK)

            screen.fill(BLACK)
            screen_right_wall.update()
            screen_left_wall.update()
            screen_top_wall.update()
            screen.blit(lives_text_surf, (10, 5))
            screen.blit(points_text_surf, (800, 5))
            paddle.update()
            to_break_loop = False
            for brick in bricks:
                brick.update()
                if any([brick.bottom_wall.colliding, brick.top_wall.colliding,
                        brick.left_wall.colliding, brick.right_wall.colliding]):
                    brick.remove_colour()
                    points += Brick.count_bricks_left()
                    points += brick.reward_points
                    if points == HIGHSCORE:  # TODO change for the actual game
                        def congratulations_screen():
                            """ Screen to be displayed when the player breaks all bricks """
                            game_over_surface = pygame.image.load("congratsBackground.png")
                            root.blit(game_over_surface, (0, 0))
                            while True:
                                events = pygame.event.get()
                                for event in events:
                                    if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()

                                root.blit(game_over_surface, (0, 0))
                                pygame.display.update()

                        to_break_loop = True
                        break
                    bricks.remove(bricks[bricks.index(brick)])
            if to_break_loop:
                break
            ball.update()
            root.blit(screen, (12, 12))

            pygame.display.update()
            clock.tick(50)

        if points == HIGHSCORE:
            # noinspection PyUnboundLocalVariable
            congratulations_screen()
        else:
            # noinspection PyUnboundLocalVariable
            game_over_menu()
