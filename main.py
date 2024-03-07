import math
import random
import pygame
import sys
from pygame import Vector2

pygame.init()

# Game screen
cell_size = 65
board_size = 15
screen = pygame.display.set_mode((cell_size * board_size, cell_size * board_size))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 24)


# Assets
donut = pygame.image.load("assets/images/donut.png").convert_alpha()
new_width = cell_size
new_height = cell_size
donut_resized = pygame.transform.scale(donut, (new_width, new_height))


class Donut:
    def __init__(self) -> None:
        # Position
        self.get_random_pos([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])

    def render(self):
        rect = pygame.Rect(
            self.position.x * cell_size,
            self.position.y * cell_size,
            cell_size,
            cell_size,
        )
        screen.blit(donut_resized, rect)

    def get_random_pos(self, snake_pos):
        self.position = Vector2(
            random.randint(0, board_size - 5), random.randint(0, board_size - 5)
        )

        # Check if the generated position conflicts with the snake's body positions
        while self.position in snake_pos:
            # If the position conflicts with the snake's body, generate a new position
            self.position = Vector2(
                random.randint(0, board_size - 5), random.randint(0, board_size - 5)
            )


class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.is_icr_size = False

        # Snake assets
        # Load head images
        self.head_up = pygame.image.load("assets/images/head_up.png").convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (cell_size, cell_size))

        self.head_down = pygame.image.load(
            "assets/images/head_down.png"
        ).convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down, (cell_size, cell_size))

        self.head_right = pygame.image.load(
            "assets/images/head_right.png"
        ).convert_alpha()
        self.head_right = pygame.transform.scale(
            self.head_right, (cell_size, cell_size)
        )

        self.head_left = pygame.image.load(
            "assets/images/head_left.png"
        ).convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left, (cell_size, cell_size))

        # Load and scale the tail images
        self.tail_up = pygame.image.load("assets/images/tail_up.png").convert_alpha()
        self.tail_up = pygame.transform.scale(self.tail_up, (cell_size, cell_size))

        self.tail_down = pygame.image.load(
            "assets/images/tail_down.png"
        ).convert_alpha()
        self.tail_down = pygame.transform.scale(self.tail_down, (cell_size, cell_size))

        self.tail_right = pygame.image.load(
            "assets/images/tail_right.png"
        ).convert_alpha()
        self.tail_right = pygame.transform.scale(
            self.tail_right, (cell_size, cell_size)
        )

        self.tail_left = pygame.image.load(
            "assets/images/tail_left.png"
        ).convert_alpha()
        self.tail_left = pygame.transform.scale(self.tail_left, (cell_size, cell_size))

        # Load and scale the body images
        self.body_vertical = pygame.image.load(
            "assets/images/body_vertical.png"
        ).convert_alpha()
        self.body_vertical = pygame.transform.scale(
            self.body_vertical, (cell_size, cell_size)
        )

        self.body_horizontal = pygame.image.load(
            "assets/images/body_horizontal.png"
        ).convert_alpha()
        self.body_horizontal = pygame.transform.scale(
            self.body_horizontal, (cell_size, cell_size)
        )

        # Load and scale the corner body images
        self.body_tr = pygame.image.load(
            "assets/images/body_topright.png"
        ).convert_alpha()
        self.body_tr = pygame.transform.scale(self.body_tr, (cell_size, cell_size))

        self.body_tl = pygame.image.load(
            "assets/images/body_topleft.png"
        ).convert_alpha()
        self.body_tl = pygame.transform.scale(self.body_tl, (cell_size, cell_size))

        self.body_br = pygame.image.load(
            "assets/images/body_bottomright.png"
        ).convert_alpha()
        self.body_br = pygame.transform.scale(self.body_br, (cell_size, cell_size))

        self.body_bl = pygame.image.load(
            "assets/images/body_bottomleft.png"
        ).convert_alpha()
        self.body_bl = pygame.transform.scale(self.body_bl, (cell_size, cell_size))

        self.head = self.head_down
        self.tail = self.tail_down

    def render(self):
        self.update_graphic_head()
        self.update_graphic_tail()

        for index, body in enumerate(self.body):
            x_pos = body.x * cell_size
            y_pos = body.y * cell_size
            rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, rect)
            else:
                prev_body = self.body[index + 1] - body
                next_body = self.body[index - 1] - body

                if prev_body.x == next_body.x:
                    screen.blit(self.body_vertical, rect)
                elif prev_body.y == next_body.y:
                    screen.blit(self.body_horizontal, rect)
                else:
                    # Handle diagonal movement
                    if (prev_body.x == -1 and next_body.y == -1) or (
                        prev_body.y == -1 and next_body.x == -1
                    ):
                        # Diagonal movement towards top-left
                        screen.blit(self.body_tl, rect)
                    elif (prev_body.x == -1 and next_body.y == 1) or (
                        prev_body.y == 1 and next_body.x == -1
                    ):
                        # Diagonal movement towards bottom-left
                        screen.blit(self.body_bl, rect)
                    elif (prev_body.x == 1 and next_body.y == -1) or (
                        prev_body.y == -1 and next_body.x == 1
                    ):
                        # Diagonal movement towards top-right
                        screen.blit(self.body_tr, rect)
                    elif (prev_body.x == 1 and next_body.y == 1) or (
                        prev_body.y == 1 and next_body.x == 1
                    ):
                        # Diagonal movement towards bottom-right
                        screen.blit(self.body_br, rect)

    def move(self):
        # Move snake
        body_copy = self.body if self.is_icr_size else self.body[:-1]
        self.is_icr_size = False
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def icr_size(self):
        self.is_icr_size = True

    def update_graphic_head(self):
        direction = self.body[1] - self.body[0]
        if direction == Vector2(1, 0):
            self.head = self.head_left
        elif direction == Vector2(-1, 0):
            self.head = self.head_right
        elif direction == Vector2(0, 1):
            self.head = self.head_up
        elif direction == Vector2(0, -1):
            self.head = self.head_down

    def update_graphic_tail(self):
        direction = self.body[-2] - self.body[-1]
        if direction == Vector2(1, 0):
            self.tail = self.tail_left
        elif direction == Vector2(-1, 0):
            self.tail = self.tail_right
        elif direction == Vector2(0, 1):
            self.tail = self.tail_up
        elif direction == Vector2(0, -1):
            self.tail = self.tail_down


class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.donut = Donut()
        self.score = 0

    def update(self):
        self.snake.move()
        self.resolve_collision()
        self.check_game_state()

    def render(self):
        self.draw_grass_grid()
        self.snake.render()
        self.donut.render()
        self.calc_score()

    def resolve_collision(self):
        # Reset donut + increase snake size
        if self.donut.position == self.snake.body[0]:
            self.donut.get_random_pos(self.snake.body)
            self.snake.icr_size()

    def check_game_state(self):
        head = self.snake.body[0]

        # Snake hits wall
        if not (0 <= head.x < board_size and 0 <= head.y < board_size):
            self.snake.reset()
            return

        if head in self.snake.body[1:]:
            self.snake.reset()
            return

    def calc_score(self):
        score = len(self.snake.body) - 3
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(
            score_text, (cell_size * board_size - score_text.get_width() - 10, 10)
        )

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass_grid(self):
        for row in range(board_size):
            if row % 2 == 0:
                for col in range(board_size):
                    if col % 2 == 0:
                        rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, (80, 200, 120), rect)
            else:
                for col in range(board_size):
                    if col % 2 != 0:
                        rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, (80, 200, 120), rect)


# Game config
clock = pygame.time.Clock()
main = Main()

# Check for User event
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            main.game_over()

        # Move snake event
        if event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 70)
            main.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main.snake.direction != Vector2(0, 1):
                main.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and main.snake.direction != Vector2(0, -1):
                main.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and main.snake.direction != Vector2(1, 0):
                main.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and main.snake.direction != Vector2(-1, 0):
                main.snake.direction = Vector2(1, 0)

    screen.fill(((144, 224, 72)))

    main.render()

    # Draw element
    pygame.display.update()

    # Set frame per second (120 fps)
    clock.tick(200)
