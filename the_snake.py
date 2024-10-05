from random import randrange, choice
from collections import Counter
# from random import choice, randint, randrange

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# 640x480 => 1~20x20 => 32x24
# Тут опишите все классы игры.


class GameObject:
    """GameObject."""

    # duplicate for passing tests
    position = SCREEN_CENTER

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
        pass

    @staticmethod
    def randomize_position():
        """Picks random (x, y) coordinates on screen"""
        return (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        )


class Apple(GameObject):
    """Apple."""

    _body_color = (255, 0, 0)

    def __init__(self):
        super().__init__(
            body_color=self._body_color,
            position=self.randomize_position()
        )

    # Метод draw класса Apple
    def draw(self):
        """отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Программно змейка — это список координат, каждый элемент списка
    соответствует отдельному сегменту тела змейки.
    Атрибуты и методы класса обеспечивают логику движения,
    отрисовку, обработку событий (нажата клавиша)
    и другие аспекты поведения змейки в игре.
    """

    def __init__(
            self,
            length=1,
            positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
            direction=RIGHT,
            body_color=(0, 255, 0)):
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = direction
        self.body_color = body_color
        self.last = self.positions[-1]
        # super.__init__()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, length=None):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        # @NOTE: Я очень хочу улучшить следующий чекер, но пока нет идей как
        # append new snake head elem
        if self.direction == UP:
            x, y = self.get_head_position
            elem = tuple([
                x,
                (y - GRID_SIZE)
                if (0 <= (y - GRID_SIZE) < SCREEN_HEIGHT)
                else (SCREEN_HEIGHT - GRID_SIZE)
            ])
            self.positions.insert(0, elem)
        elif self.direction == DOWN:
            x, y = self.get_head_position
            elem = tuple([
                x,
                (y + GRID_SIZE)
                if (0 <= (y + GRID_SIZE) < SCREEN_HEIGHT)
                else (0)
            ])
            self.positions.insert(0, elem)
        elif self.direction == LEFT:
            x, y = self.get_head_position
            elem = tuple([
                (x - GRID_SIZE)
                if (0 <= (x - GRID_SIZE) < SCREEN_WIDTH)
                else (SCREEN_WIDTH - GRID_SIZE),
                y
            ])
            self.positions.insert(0, elem)
        elif self.direction == RIGHT:
            val = self.get_head_position
            x, y = val
            elem = tuple([
                (x + GRID_SIZE)
                if (0 <= (x + GRID_SIZE) < SCREEN_WIDTH)
                else (0),
                y
            ])
            self.positions.insert(0, elem)
        else:
            raise ValueError('Unknown direction to move')
        # removes last snake elem when length stays the same
        self.last = self.positions[-1]
        if length is None:
            self.positions.pop()

    def draw(self):
        """Метод draw класса Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self):
        """
        возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def main():
    """Инициализация PyGame:"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        # check snake innards for apple presence
        if apple.position in snake.positions:
            snake.move(snake.length + 1)
            snake.length += 1
            apple.__init__()
        else:
            snake.move()
        # check if snake ate itself
        if Counter(snake.positions)[snake.positions[0]] > 1:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()

    # Тут опишите основную логику игры.
    # ...


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
