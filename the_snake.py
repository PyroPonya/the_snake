from random import randrange, choice

import pygame as pg

# 640x480 => 1~20x20 => 32x24
# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Centre of the screen
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """GameObject."""

    def __init__(
            self,
            body_color=BOARD_BACKGROUND_COLOR,
            position=SCREEN_CENTER
    ):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        """
        raise NotImplementedError(
            f'method draw() not implemented for class {self}'
        )

    def draw_cell(
        self,
        position,
        color=BOARD_BACKGROUND_COLOR,
        border=BOARD_BACKGROUND_COLOR
    ):
        """Draws singular cell. Color => fill. Border => outline."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border, rect, 1)


class Apple(GameObject):
    """Apple."""

    def __init__(self, restricted_positions):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(restricted_positions)

    def randomize_position(self, restricted_positions):
        """Picks random (x, y) coordinates on screen"""
        self.position = tuple([
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        ])
        while (self.position in restricted_positions):
            self.randomize_position(restricted_positions)

    def draw(self):
        """отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """
    Программно змейка — это список координат, каждый элемент списка
    соответствует отдельному сегменту тела змейки.
    Атрибуты и методы класса обеспечивают логику движения,
    отрисовку, обработку событий (нажата клавиша)
    и другие аспекты поведения змейки в игре.
    """

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        # append new snake head elem
        if self.direction == UP:
            x, y = self.get_head_position()
            self.positions.insert(
                0, tuple([x, (y - GRID_SIZE) % SCREEN_HEIGHT]))
        elif self.direction == DOWN:
            x, y = self.get_head_position()
            self.positions.insert(
                0, tuple([x, (y + GRID_SIZE) % SCREEN_HEIGHT]))
        elif self.direction == LEFT:
            x, y = self.get_head_position()
            self.positions.insert(
                0, tuple([(x - GRID_SIZE) % SCREEN_WIDTH, y]))
        elif self.direction == RIGHT:
            x, y = self.get_head_position()
            self.positions.insert(
                0, tuple([(x + GRID_SIZE) % SCREEN_WIDTH, y]))
        else:
            raise ValueError('Unknown direction to move')
        self.last = self.positions.pop()

    def draw(self):
        """Метод draw класса Snake"""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0], self.body_color, BORDER_COLOR)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def grow(self):
        """Grows the snake."""
        self.positions.append(self.last)
        self.last = None

    def get_head_position(self):
        """
        возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()


def main():
    """Инициализация PyGame:"""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        # check snake innards for apple presence
        snake.move()
        if apple.position in snake.positions:
            snake.grow()
            apple.__init__(snake.positions)
        # check if snake ate itself
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
