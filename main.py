import pygame
import sys
from pygame.locals import *
from constants import *
import numpy
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


class Brick:
    def __init__(self, x, y, length, height, super_surface, collision_object, colour):
        """
        :param x: x coord of the top left corner
        :param y: y coord of the top right corner
        :param length: horizontal length
        :param height: vertical length
        """
        self.x, self.y = x, y
        self.length, self.height = length, height
        self.super_surface = super_surface
        self.collision_object = collision_object
        self.colour = colour
        self.collided = False
        self.update()

    def check_for_collisions(self):
        for x_coord, y_coord in self.collision_object.outline_coords_list:
            if y_coord == self.y + self.height and self.x <= x_coord <= self.x + self.length:
                self.collision_object.velocity[1] = abs(self.collision_object.velocity[1])
                self.collided = True
            elif y_coord == self.y and self.x <= x_coord <= self.x + self.length:
                self.collision_object.velocity[1] = -abs(self.collision_object.velocity[1])
                self.collided = True
            elif x_coord == self.x and self.y <= y_coord <= self.y + self.height:
                self.collision_object.velocity[0] = -abs(self.collision_object.velocity[0])
                self.collided = True
            elif x_coord == self.x + self.length and self.y <= y_coord <= self.y + self.height:
                self.collision_object.velocity[0] = abs(self.collision_object.velocity[0])
                self.collided = True

    def update(self):
        self.check_for_collisions()
        pygame.draw.rect(self.super_surface, self.colour, (self.x, self.y, self.length, self.height))


class Paddle(Brick):
    def __init__(self, x, y, length, height, super_surface, collision_object, colour):
        super().__init__(x, y, length, height, super_surface, collision_object, colour)
        self.prev_x = None

    def check_for_collisions(self):
        for x_coord, y_coord in self.collision_object.outline_coords_list:
            if y_coord == self.y and self.x <= x_coord <= self.x + self.length:
                self.collision_object.velocity[0] = random.uniform(-1.4, 1.4)
                self.collision_object.velocity[1] = -abs(self.collision_object.velocity[1])
                self.collided = True
            elif x_coord == self.x and self.y <= y_coord <= self.y + self.height:
                self.collision_object.velocity[0] = -abs(self.collision_object.velocity[0])
                self.collided = True
            elif x_coord == self.x + self.length and self.y <= y_coord <= self.y + self.height:
                self.collision_object.velocity[0] = abs(self.collision_object.velocity[0])
                self.collided = True

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.prev_x = self.x
        self.x = mouse_x - self.length / 2
        self.check_for_collisions()
        pygame.draw.rect(self.super_surface, BLACK, (self.prev_x, self.y, self.length, self.height))
        pygame.draw.rect(self.super_surface, self.colour, (self.x, self.y, self.length, self.height))


class Ball:
    def __init__(self, centre_x, centre_y, radius, initial_velocity, super_surface, speed):
        self.radius = radius
        self.centre_x, self.centre_y = centre_x, centre_y
        self.prev_centre_x, self.prev_centre_y = None, None
        self.super_surface = super_surface
        self.speed = speed
        self.velocity = pygame.Vector2(initial_velocity)
        self.in_collision = False
        self.outline_coords_list = None
        self.update_outline_coords()

    def update_outline_coords(self):
        array1 = numpy.array([[0, 0] for _ in range((self.radius + 1) * 2)])
        array2 = numpy.array([[0, 0] for _ in range((self.radius + 1) * 2)])
        for i in range(-self.radius, self.radius + 1):
            array1[i + self.radius] = [i + self.centre_x, self.centre_y - ((self.radius**2 - i**2)**0.5)]
        for i in range(-self.radius, self.radius + 1):
            array2[i + self.radius] = [i + self.centre_x, self.centre_y + ((self.radius**2 - i**2)**0.5)]
        self.outline_coords_list = numpy.concatenate((array1[:-1], array2[:-1]), axis=0)

    def update(self):
        self.velocity = self.velocity.normalize()
        self.prev_centre_x, self.prev_centre_y = self.centre_x, self.centre_y
        self.centre_x += self.velocity[0] * self.speed
        self.centre_y += self.velocity[1] * self.speed
        self.update_outline_coords()
        pygame.draw.circle(self.super_surface, BLACK, (self.prev_centre_x, self.prev_centre_y), self.radius)
        pygame.draw.circle(self.super_surface, FUCHSIA, (self.centre_x, self.centre_y), self.radius)


def main_menu():
    """ When the game is run, this menu is the first thing displayed. Rules of the game could be added here """
    background = pygame.image.load("Assets/startMenuBackground.png")
    main_menu_surface = pygame.Surface((1020, 654))
    start_button = Button(background, 510 - 150, 475, "Assets/playButton_U.png", "Assets/playButton_C.png")
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
            root.fill(BLACK)
            return
        pygame.display.update()


def game():
    lives, points = 5, 0

    ball = Ball(500, 600, 10, (random.uniform(-2, 2), -1), root, 2)
    left_wall = Brick(0, 0, 12, 600, root, ball, GRAY)
    top_wall = Brick(0, 0, 1020, 12, root, ball, GRAY)
    right_wall = Brick(1008, 0, 12, 600, root, ball, GRAY)
    paddle = Paddle(500, 600, 200, 30, root, ball, BLUE)

    bricks = []
    loop_colour = [RED, RED, ORANGE, ORANGE, YELLOW, YELLOW, GREEN, GREEN]
    for j in range(1, 9):
        for i in range(1, 16):
            bricks.append(Brick(-48 + 66 * i, 24 + 36 * j, BRICK_LENGTH, BRICK_HEIGHT, root, ball, loop_colour[j - 1]))
    number_green_bricks, no_green_bricks_left = 30, False
    number_yellow_bricks, no_yellow_bricks_left = 30, False
    number_orange_bricks, no_orange_bricks_left = 30, False
    number_red_bricks, no_red_bricks_left = 30, False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if points == HIGHSCORE:
            congratulations_screen()

        ball.update()
        left_wall.update()
        right_wall.update()
        top_wall.update()
        paddle.update()

        last_brick = bricks[-1]
        if last_brick.y + last_brick.height + ball.radius + 5 < ball.centre_y:
            pass
        else:
            for brick in bricks:
                brick.update()
                if brick.collided:
                    if brick.colour == GREEN:
                        points += 5
                        number_green_bricks -= 1
                        if number_green_bricks == 0 and no_green_bricks_left is False:
                            points += 250
                            no_green_bricks_left = True
                            ball.speed = 3
                    elif brick.colour == YELLOW:
                        points += 10
                        number_yellow_bricks -= 1
                        if number_yellow_bricks == 0 and no_yellow_bricks_left is False:
                            points += 500
                            no_yellow_bricks_left = True
                            ball.speed = 4
                    elif brick.colour == ORANGE:
                        points += 15
                        number_orange_bricks -= 1
                        if number_orange_bricks == 0 and no_orange_bricks_left is False:
                            points += 750
                            no_orange_bricks_left = True
                            ball.speed = 5
                    elif brick.colour == RED:
                        points += 20
                        number_red_bricks -= 1
                        if number_red_bricks == 0 and no_red_bricks_left is False:
                            points += 1000
                            no_red_bricks_left = True
                            ball.speed = 7
                    root.fill(BLACK, [brick.x, brick.y, brick.length, brick.height])
                    bricks.remove(bricks[bricks.index(brick)])

        if ball.centre_y - ball.radius > ROOT_SIZE[1]:
            lives -= 1
            if lives == 0:
                game_over_menu(points)
                break
            ball.centre_y = 500
            ball.centre_x = random.randint(100, 900)
            ball.velocity[0], ball.velocity[1] = random.uniform(-1.2, 1.2), -1
        lives_text_surf = font1.render(f"Lives left: {lives}  ", True, WHITE, BLACK)
        points_text_surf = font1.render(f"Points: {points}  ", True, WHITE, BLACK)
        root.blit(lives_text_surf, (20, 17))
        root.blit(points_text_surf, (ROOT_SIZE[0] - 12 - 200, 17))

        pygame.display.update()
        clock.tick(120)


def game_over_menu(points):
    """ Screen to be displayed when player loses all lives """
    player_score = font3.render(f"{points}", True, RED)
    game_over_surface = pygame.image.load("Assets/gameOverBackground.png")
    start_again_button = Button(game_over_surface, 289, 475, "Assets/startAgain_U.png",
                                "Assets/startAgain_C.png")
    game_over_surface.blit(player_score, (root.get_size()[0] / 2 - player_score.get_size()[0] / 2, 280))

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


def congratulations_screen():
    """ Screen to be displayed when the player breaks all bricks """
    game_over_surface = pygame.image.load("Assets/congratsBackground.png")
    root.blit(game_over_surface, (0, 0))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        root.blit(game_over_surface, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    root = pygame.display.set_mode(ROOT_SIZE)
    clock = pygame.time.Clock()
    font1 = pygame.font.SysFont("Comic Sans MS", 30)
    font2 = pygame.font.SysFont("Comic Sans MS", 50)
    font3 = pygame.font.SysFont("Commons", 140)

    while True:
        main_menu()
        game()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(120)
