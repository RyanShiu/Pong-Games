import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH, HEIGHT = 600, 600

class Paddle:
    COLOR = CYAN
    VEL = 6

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
class Ball:
    SPEED = 6
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.SPEED
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.SPEED = 6
        if self.x_vel < 0:
            self.x_vel = self.SPEED
        else:
            self.x_vel = -self.SPEED

    def end_reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = 0

def handle_collision(ball, left_paddle, right_paddle, faster):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y  >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel = ball.SPEED

                if faster == True and ball.SPEED < 30:
                    ball.SPEED += 1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.SPEED

                y_vel = difference_in_y / reduction_factor

                ball.y_vel = y_vel * -1
    else:
        if ball.y  >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel = -ball.SPEED

                if faster == True and ball.SPEED < 30:
                    ball.SPEED += 1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.SPEED

                y_vel = difference_in_y / reduction_factor

                ball.y_vel = y_vel * -1



def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and  left_paddle.y - Paddle.VEL >=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + Paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - Paddle.VEL >=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + Paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def handle_paddle_movement_practice(keys, left_paddle):
    if keys[pygame.K_w] and  left_paddle.y - Paddle.VEL >=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + Paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)