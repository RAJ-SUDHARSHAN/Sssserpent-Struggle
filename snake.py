'''
Copyright 2023 Raj Sudharshan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
BLOCK_SIZE = 20
PLAYER_COLOR = 'green'
ENEMY_COLOR1 = 'red'
ENEMY_COLOR2 = 'blue'
ENEMY_COLOR3 = 'white'
ENEMY_COLOR4 = 'magenta'
FOOD_COLOR = 'yellow'
CLOCK = pygame.time.Clock()
FPS = 10


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Enhanced Snake Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.setup()

    def setup(self):
        self.game_over = False
        self.game_pause = False
        self.restart = True
        self.timer = pygame.time.get_ticks()
        self.score = 0
        self.player_snake = Snake(self.screen)
        self.player_snake.draw(PLAYER_COLOR)
        self.foods = [Food(self.screen)]
        self.blocks = [
            Block(self.screen, [self.player_snake], self.foods) for _ in range(8)]
        self.enemy_snakes = [
            Snake(self.screen, is_enemy=True, foods=self.foods) for _ in range(1)]
        self.food_spawn_times = [40000, 90000]
        self.enemy_snake_spawn_time = [20000, 40000, 130000]

    def play_game(self):
        self.player_snake.move()
        self.screen.fill((0, 0, 0))

        for block in self.blocks:
            block.draw()

        self.player_snake.draw(PLAYER_COLOR)

        for i, snake in enumerate(self.enemy_snakes):
            snake.move()
            color = eval(f'ENEMY_COLOR{i+2}')
            snake.draw(color)

        for food in self.foods:
            food.draw(FOOD_COLOR)

        for enemy_snake in self.enemy_snakes:
            self.snake_collision(self.player_snake, enemy_snake)
            self.consume_food(self.player_snake)
            self.consume_food(enemy_snake)
            if self.block_collision(enemy_snake, self.blocks):
                self.enemy_snakes.remove(enemy_snake)
                self.spawn_new_snake()

        if self.block_collision(self.player_snake, self.blocks):
            self.show_game_over()

        self.display_time()
        self.display_score()
        pygame.display.update()
        CLOCK.tick(FPS)

    def consume_food(self, snake):
        for food in self.foods:
            if snake.x[0] == food.x and snake.y[0] == food.y:
                snake.length += 1
                snake.x.append(snake.x[-1] - BLOCK_SIZE)
                snake.y.append(snake.y[-1])
                self.foods.remove(food)
                self.foods.append(Food(self.screen))
                self.score += 10
                for enemy_snake in self.enemy_snakes:
                    enemy_snake.foods = self.foods

    def head_collide(self, player_snake, enemy_snake):
        return (abs(player_snake.x[0] - enemy_snake.x[0]) < BLOCK_SIZE and
                abs(player_snake.y[0] - enemy_snake.y[0]) < BLOCK_SIZE)

    def body_collide(self, snake1, snake2, index):
        return (snake1.x[index] == snake2.x[0] and snake1.y[index] == snake2.y[0])

    def handle_head_collision(self, player_snake, enemy_snake):
        if player_snake.length <= enemy_snake.length:
            self.show_game_over()
            return True
        else:
            enemy_snake.length = 0
            enemy_snake.x.clear()
            enemy_snake.y.clear()
            enemy_snake.__init__(self.screen)
            return False

    def handle_body_collision(self, player_snake, enemy_snake, index):
        if player_snake == enemy_snake:
            if index < player_snake.length - 2:
                self.show_game_over()
                return True
            else:
                return False
        else:
            if index < player_snake.length - 2:
                if enemy_snake.length > player_snake.length - index - 1:
                    player_snake.length -= index + 1
                    self.score -= 5
                else:
                    new_length = enemy_snake.length - \
                        (player_snake.length - index - 1)
                    enemy_snake.x = enemy_snake.x[:new_length]
                    enemy_snake.y = enemy_snake.y[:new_length]
                    enemy_snake.length = new_length
                    self.score += 10
                return False
            else:
                return False

    def self_collision(self, player_snake):
        for i in range(2, player_snake.length):
            if player_snake.x[0] == player_snake.x[i] and player_snake.y[0] == player_snake.y[i]:
                return True
        return False

    def snake_collision(self, player_snake, enemy_snake):
        if self.self_collision(player_snake):
            self.show_game_over()
            return True

        if self.block_collision(player_snake, self.blocks):
            self.show_game_over()
            return True

        for i in range(1, player_snake.length):
            if self.body_collide(player_snake, enemy_snake, i):
                if enemy_snake.length > player_snake.length - i:
                    player_snake.length = i
                    self.score -= 5
                    return False
                else:
                    new_player_length = i + enemy_snake.length
                    player_snake.x = player_snake.x[:new_player_length]
                    player_snake.y = player_snake.y[:new_player_length]
                    player_snake.length = new_player_length
                    enemy_snake.length = 0
                    enemy_snake.x.clear()
                    enemy_snake.y.clear()
                    enemy_snake.__init__(self.screen)
                    self.score += 10
                    return False

        for i in range(1, enemy_snake.length):
            if self.body_collide(enemy_snake, player_snake, i):
                if player_snake.length > enemy_snake.length - i:
                    enemy_snake.length = i
                    self.score -= 5
                    return False
                else:
                    new_enemy_length = i + player_snake.length
                    enemy_snake.x = enemy_snake.x[:new_enemy_length]
                    enemy_snake.y = enemy_snake.y[:new_enemy_length]
                    enemy_snake.length = new_enemy_length
                    player_snake.length = 0
                    player_snake.x.clear()
                    player_snake.y.clear()
                    player_snake.__init__(self.screen)
                    self.show_game_over()
                    return True

        if self.head_collide(player_snake, enemy_snake):
            if player_snake.length <= enemy_snake.length:
                self.show_game_over()
                return True
            else:
                enemy_snake.length = 0
                enemy_snake.x.clear()
                enemy_snake.y.clear()
                enemy_snake.__init__(self.screen)
                return False

        return False

    def block_collision(self, snake, blocks):
        for block in blocks:
            if snake.x[0] == block.x and snake.y[0] == block.y:
                return True
        return False

    def spawn_new_snake(self):
        enemy_snake = Snake(self.screen, is_enemy=True, foods=self.foods)
        self.enemy_snakes.append(enemy_snake)

    def message(self, msg, color):
        font_size = SCREEN_HEIGHT // 15
        if SCREEN_HEIGHT <= 480:
            font_size = SCREEN_HEIGHT // 20
        elif SCREEN_HEIGHT <= 720:
            font_size = SCREEN_HEIGHT // 15
        else:
            font_size = SCREEN_HEIGHT // 20

        font_style = pygame.font.SysFont(None, font_size)
        message = font_style.render(msg, True, color)
        message_rect = message.get_rect()
        message_rect.centerx = SCREEN_WIDTH // 2
        message_rect.centery = SCREEN_HEIGHT // 2
        self.screen.blit(message, message_rect)

    def show_game_over(self):
        self.message(
            "Game Over. Press ENTER to restart or Q to quit", (255, 255, 255))
        self.timer = pygame.time.get_ticks()
        self.game_over = True
        pygame.display.update()

    def reset_game(self):
        for enemy_snake in self.enemy_snakes:
            del enemy_snake
        self.enemy_snakes = []
        self.setup()
        self.timer = pygame.time.get_ticks()

    def display_time(self):
        elapsed_time_sec = pygame.time.get_ticks()
        font = pygame.font.Font(None, 36)
        time_text = font.render(
            f"Time: {abs(self.timer - elapsed_time_sec) // 1000}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - 140, 10))

    def run(self):
        pygame.time.set_timer(USEREVENT, 1000)

        while self.restart:
            if not self.game_over:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.game_over = True
                        self.restart = False

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.game_pause = True
                            self.message(
                                "Game Paused. Press SPACE BAR to continue", (255, 255, 255))
                            pygame.display.update()

                        if event.key == K_SPACE:
                            self.game_pause = False

                        if event.key == K_RETURN:
                            self.game_pause = False

                        if not self.game_pause:
                            if event.key == K_RETURN:
                                self.reset_game()

                            if event.key == K_UP:
                                self.player_snake.move_up()

                            if event.key == K_DOWN:
                                self.player_snake.move_down()

                            if event.key == K_LEFT:
                                self.player_snake.move_left()

                            if event.key == K_RIGHT:
                                self.player_snake.move_right()

                elapsed_time_ms = pygame.time.get_ticks()

                if self.enemy_snake_spawn_time and abs(self.timer - elapsed_time_ms) >= self.enemy_snake_spawn_time[0]:
                    self.spawn_new_snake()
                    self.enemy_snake_spawn_time.pop(0)

                if self.food_spawn_times and abs(self.timer - elapsed_time_ms) >= self.food_spawn_times[0]:
                    self.foods.append(Food(self.screen))
                    self.food_spawn_times.pop(0)

                try:
                    if not self.game_pause:
                        self.play_game()
                        self.display_time()
                        self.display_score()
                        pygame.display.update()

                except Exception as e:
                    self.show_game_over()
                    self.game_pause = True
                    self.player_snake = Snake(self.screen)

            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.game_over = True
                        self.restart = False

                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.game_pause = True
                            self.message(
                                "Game Paused. Press SPACE BAR to continue", (255, 255, 255))
                            self.timer = pygame.time.get_ticks()
                            pygame.display.update()

                        if event.key == K_q:
                            self.restart = False

                        if event.key == K_RETURN:
                            self.reset_game()
                            self.player_snake.draw(PLAYER_COLOR)
                            for i, snake in enumerate(self.enemy_snakes):
                                color = eval(f'ENEMY_COLOR{i + 1}')
                                snake.draw(color)

                pygame.display.update()

        pygame.quit()


class Snake:
    def __init__(self, surface, is_enemy=False, blocks=None, foods=None):
        self.surface = surface
        self.is_enemy = is_enemy
        directions = ['right', 'left', 'up', 'down']
        self.direction = random.choice(directions)
        self.length = 3
        rand_x = random.randint(
            0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        rand_y = random.randint(
            0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.x = [rand_x, rand_x + BLOCK_SIZE, rand_x + 2 * BLOCK_SIZE]
        self.y = [rand_y, rand_y + BLOCK_SIZE, rand_y + (2 * BLOCK_SIZE)]
        self.target_food = None
        self.blocks = blocks
        self.foods = foods

        if is_enemy and foods:
            self.target_food = random.choice(foods).get_pos()

    def move_up(self):
        if self.direction == 'down':
            return
        self.direction = 'up'

    def move_down(self):
        if self.direction == 'up':
            return
        self.direction = 'down'

    def move_left(self):
        if self.direction == 'right':
            return
        self.direction = 'left'

    def move_right(self):
        if self.direction == 'left':
            return
        self.direction = 'right'

    def draw(self, color):
        head_center_x = self.x[0] + BLOCK_SIZE // 2
        head_center_y = self.y[0] + BLOCK_SIZE // 2
        head_points = []

        if self.direction == "up":
            head_points = [
                (head_center_x, self.y[0]),
                (self.x[0], self.y[0] + BLOCK_SIZE),
                (self.x[0] + BLOCK_SIZE, self.y[0] + BLOCK_SIZE),
            ]
        elif self.direction == "down":
            head_points = [
                (head_center_x, self.y[0] + BLOCK_SIZE),
                (self.x[0], self.y[0]),
                (self.x[0] + BLOCK_SIZE, self.y[0]),
            ]
        elif self.direction == "left":
            head_points = [
                (self.x[0], head_center_y),
                (self.x[0] + BLOCK_SIZE, self.y[0]),
                (self.x[0] + BLOCK_SIZE, self.y[0] + BLOCK_SIZE),
            ]
        elif self.direction == "right":
            head_points = [
                (self.x[0] + BLOCK_SIZE, head_center_y),
                (self.x[0], self.y[0]),
                (self.x[0], self.y[0] + BLOCK_SIZE),
            ]

        pygame.draw.polygon(self.surface, color, head_points)

        for i in range(1, self.length):
            pygame.draw.rect(self.surface, color,
                             (self.x[i], self.y[i], BLOCK_SIZE, BLOCK_SIZE))

    def move(self):
        if self.is_enemy:
            self.move_enemy()
        else:
            self.move_player()

    def move_player(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= BLOCK_SIZE

        if self.direction == 'down':
            self.y[0] += BLOCK_SIZE

        if self.direction == 'left':
            self.x[0] -= BLOCK_SIZE

        if self.direction == 'right':
            self.x[0] += BLOCK_SIZE

        if self.x[0] < 0:
            self.x[0] = self.surface.get_width() - BLOCK_SIZE

        if self.x[0] >= self.surface.get_width():
            self.x[0] = 0

        if self.y[0] < 0:
            self.y[0] = self.surface.get_height() - BLOCK_SIZE

        if self.y[0] >= self.surface.get_height():
            self.y[0] = 0

    def move_enemy(self):
        if not self.target_food and not self.foods:
            return

        if not self.target_food:
            self.target_food = random.choice(self.foods).get_pos()

        if (self.x[0], self.y[0]) == self.target_food:
            self.target_food = None
            return

        dx = self.target_food[0] - self.x[0]
        dy = self.target_food[1] - self.y[0]

        if abs(dx) > abs(dy):
            if dx > 0:
                self.try_change_direction('right')
            else:
                self.try_change_direction('left')
        else:
            if dy > 0:
                self.try_change_direction('down')
            else:
                self.try_change_direction('up')

        self.move_player()

    def try_change_direction(self, new_direction):
        if new_direction in ['up', 'down']:
            if self.direction not in ['up', 'down']:
                self.direction = new_direction
        elif new_direction in ['left', 'right']:
            if self.direction not in ['left', 'right']:
                self.direction = new_direction

    def find_food(self, foods, blocks):
        if self.is_enemy:
            min_distance = float('inf')
            target_food = None

            for food in foods:
                distance = abs(self.x[0] - food.x) + abs(self.y[0] - food.y)
                if distance < min_distance:
                    min_distance = distance
                    target_food = food

            if target_food is not None:
                if target_food.x < self.x[0]:
                    if not self.is_direction_blocked('left', blocks):
                        self.move_left()
                    elif not self.is_direction_blocked('up', blocks):
                        self.move_up()
                    elif not self.is_direction_blocked('down', blocks):
                        self.move_down()
                elif target_food.x > self.x[0]:
                    if not self.is_direction_blocked('right', blocks):
                        self.move_right()
                    elif not self.is_direction_blocked('up', blocks):
                        self.move_up()
                    elif not self.is_direction_blocked('down', blocks):
                        self.move_down()
                elif target_food.y < self.y[0]:
                    if not self.is_direction_blocked('up', blocks):
                        self.move_up()
                    elif not self.is_direction_blocked('left', blocks):
                        self.move_left()
                    elif not self.is_direction_blocked('right', blocks):
                        self.move_right()
                elif target_food.y > self.y[0]:
                    if not self.is_direction_blocked('down', blocks):
                        self.move_down()
                    elif not self.is_direction_blocked('left', blocks):
                        self.move_left()
                    elif not self.is_direction_blocked('right', blocks):
                        self.move_right()

    def is_direction_blocked(self, direction, blocks):
        x, y = self.x[0], self.y[0]

        if direction == 'up':
            y -= BLOCK_SIZE
        elif direction == 'down':
            y += BLOCK_SIZE
        elif direction == 'left':
            x -= BLOCK_SIZE
        elif direction == 'right':
            x += BLOCK_SIZE

        for block in blocks:
            if block.x == x and block.y == y:
                return True

        return False


class Food:
    def __init__(self, surface):
        self.surface = surface
        self.x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(
            0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE

    def get_pos(self):
        return self.x, self.y

    def draw(self, color):
        pygame.draw.rect(self.surface, color,
                         (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


class Block:
    def __init__(self, surface, snakes, foods):
        self.surface = surface
        self.image = pygame.image.load('assets/block.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (BLOCK_SIZE, BLOCK_SIZE))
        possible_positions = [(x, y) for x in range(
            0, SCREEN_WIDTH, BLOCK_SIZE) for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE)]
        random.shuffle(possible_positions)

        for x, y in possible_positions:
            self.x = x
            self.y = y
            if not self.position_conflicts(snakes, foods):
                break

    def position_conflicts(self, snakes, foods):
        for snake in snakes:
            for i in range(snake.length):
                if self.x == snake.x[i] and self.y == snake.y[i]:
                    return True

        for food in foods:
            if self.x == food.x and self.y == food.y:
                return True

        return False

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))


if __name__ == '__main__':
    game = Game()
    game.run()
