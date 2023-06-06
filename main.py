# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.f
import pygame
from pygame.locals import *
from handle_controls import handle_collision, handle_paddle_movement_practice, handle_paddle_movement

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WIN_POINT = 11

FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("lato", 60)
WIN_FONT = pygame.font.SysFont("helvetica", 50)
LEVEL_FONT = pygame.font.SysFont("helvetica", 40)




def get_mode_name(rect, buttons):
    # Returns the name of the mode associated with the given rectangle
    for mode, mode_rect in buttons.items():
        if mode_rect == rect:
            return mode
    return None


def draw_menu_buttons(screen, modes):
    # Draws the menu buttons on the screen and returns a dictionary mapping the mode name to its rectangle
    button_width = 400
    button_height = 50
    button_padding = 20
    mode_buttons = {}
    total_height = (button_height + button_padding) * len(modes)
    start_y = (screen.get_height() - total_height) // 2

    for mode in modes:
        button_rect = pygame.Rect(
            (screen.get_width() - button_width) // 2,
            start_y,
            button_width,
            button_height
        )
        pygame.draw.rect(screen, (255, 255, 255), button_rect)

        # Add text to the button
        font = pygame.font.Font(None, 36)
        text = font.render(mode, True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        mode_buttons[mode] = button_rect
        start_y += button_height + button_padding

    return mode_buttons



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




def draw(win, paddles, ball, left_score, right_score, speed_pong, practice):
    win.fill(BLACK)



    if speed_pong == True:
        speed_text = LEVEL_FONT.render(f"Level: " + f"{ball.SPEED - 5}", 1, WHITE)
        win.blit(speed_text, (WIDTH // 2 - speed_text.get_width()//2,  HEIGHT - speed_text.get_height()))

    if practice == False:
        left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        win.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

        if left_score == WIN_POINT:
            player_text = WIN_FONT.render(f"WIN", 1, GREEN)
            player_text2 = WIN_FONT.render(f"LOSS", 1, RED)
            win.blit(player_text, (WIDTH // 4 - player_text.get_width() // 2, HEIGHT//2 - player_text.get_height()))
            win.blit(player_text2, (WIDTH * 3 // 4 - player_text2.get_width() // 2, HEIGHT//2 - player_text2.get_height()))
        elif right_score == WIN_POINT:
            player_text = WIN_FONT.render(f"LOSS", 1, RED)
            player_text2 = WIN_FONT.render(f"WIN", 1, GREEN)
            win.blit(player_text, (WIDTH // 4 - player_text.get_width() // 2, HEIGHT // 2 - player_text.get_height()))
            win.blit(player_text2, (WIDTH * 3 // 4 - player_text2.get_width() // 2, HEIGHT // 2 - player_text2.get_height()))

    #if speed_pong == True:
    #    levels_text = SCORE_FONT.render(f"Level: " + f"{ball.SPEED - 3}", 1, WHITE)
    #    win.blit(levels_text, (WIDTH // 2 - levels_text.get_width() // 2, HEIGHT - levels_text.get_height()))

    for paddle in paddles:
        paddle.draw(win)

    counter = 0
    for i in range(10, HEIGHT, HEIGHT//24):
        counter += 1
        if i % 2 == 1 or (counter == 23 and i % 2 == 0 and speed_pong == True):
            continue
        pygame.draw.rect(win, CYAN, (WIDTH//2 - 2, i, 4, HEIGHT//24))

    ball.draw(win)
    pygame.display.update()







#Paddle controls for a 4-player game
'''def handle_paddle_movement_4player(keys, left_paddle, right_paddle, top_paddle, bot_paddle):
    if keys[pygame.K_q] and  left_paddle.y - Paddle.VEL >=0:
        left_paddle.move(up=True)
    if keys[pygame.K_a] and left_paddle.y + Paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - Paddle.VEL >=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + Paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

    if keys[pygame.K_c] and top_paddle.x - Paddle.VEL >=0:
        top_paddle.move(up=True)
    if keys[pygame.K_v] and top_paddle.x + Paddle.VEL + top_paddle.width <= HEIGHT:
        top_paddle.move(up=False)

    if keys[pygame.K_m] and bot_paddle.x - Paddle.VEL >=0:
        bot_paddle.move(up=True)
    if keys[pygame.K_COMMA] and bot_paddle.x + Paddle.VEL + bot_paddle.width <= HEIGHT:
        bot_paddle.move(up=False)
'''
def main():
    pygame.display.set_caption("Main Menu")

    # Define game modes and their corresponding actions
    game_modes = {
        "Player Vs. Player": "start_mode_1",
        "Practice": "start_mode_2",
        "Speed Pong DeathMatch": "start_mode_3"
    }

    mode_buttons = {}



    running = True
    while running:
        for event in pygame.event.get():
            selected_mode = ""
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Check if the user clicked on a game mode button
                mouse_pos = pygame.mouse.get_pos()
                for mode_rect in mode_buttons.values():
                    if mode_rect.collidepoint(mouse_pos):
                        mode_name = get_mode_name(mode_rect, mode_buttons)
                        if mode_name in game_modes:
                            selected_mode = game_modes[mode_name]
                            # Transition to the selected game mode
                            running = False  # Exit the main menu loop

        WIN.fill((0, 0, 0))

        # Draw your menu elements here
        # Draw the game mode buttons
        mode_buttons = draw_menu_buttons(WIN, game_modes.keys())

        pygame.display.flip()

    if selected_mode == "start_mode_1":
        classic()
    elif selected_mode == "start_mode_2":
        practice()
    elif selected_mode == "start_mode_3":
        speedPongDeathmatch()
    else:
        print("Exit")
        pygame.quit()


def classic():
    pygame.display.set_caption("Player Vs. Player")
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, False, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle, False)

        if not (ball.x >= 0 and ball.x <= WIDTH):
            if not (right_score == WIN_POINT or left_score == WIN_POINT):
                if ball.x < 0:
                    right_score += 1
                elif ball.x > WIDTH:
                    left_score += 1

            if (right_score == WIN_POINT or left_score == WIN_POINT):
                ball.end_reset()
            else:
                ball.reset()

            left_paddle.reset()
            right_paddle.reset()

    pygame.quit()
def practice():
    pygame.display.set_caption("Practice")
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, 0, PADDLE_WIDTH, HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, False, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle, False)

        if not (ball.x >= 0 and ball.x <= WIDTH):

            ball.reset()
            left_paddle.reset()



    pygame.quit()
def speedPongDeathmatch():
    pygame.display.set_caption("Speed Pong DeathMatch")
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10- PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)

        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, True, False)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle, True)

        if not(ball.x >= 0 and ball.x <= WIDTH):
            if not(right_score == WIN_POINT or left_score == WIN_POINT):
                if ball.x < 0:
                    right_score += 1
                elif ball.x > WIDTH:
                    left_score += 1

            if (right_score == WIN_POINT or left_score == WIN_POINT):
                ball.end_reset()
            else:
                ball.reset()

            left_paddle.reset()
            right_paddle.reset()






    pygame.quit()

if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
