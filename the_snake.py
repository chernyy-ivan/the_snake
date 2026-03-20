from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
SNAKE_COLOR = (255, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех объектов,
    который описывает общие свойства и методы.
    """

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс для яблока, который описывает его поведение"""

    def __init__(self):
        positions = self.randomize_position()
        super().__init__(positions, APPLE_COLOR)

    def randomize_position(self):
        """Метод для рандомного расположения яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.x = x
        self.y = y
        self.position = (x, y)
        return (x, y)

    def draw(self):
        """Метод для отрисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """класс для змейки, который описывает ее поведение
    и взаимодействие с другими объектами игры.
    """

    def __init__(self):
        start_position = (((GRID_WIDTH // 2) * GRID_SIZE),
                          ((GRID_HEIGHT // 2) * GRID_SIZE))
        self.positions = [start_position]
        super().__init__(start_position, SNAKE_COLOR)
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Метод для получения позиции головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод для обновления и направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow):
        """Метод для перемещения змейки по игровому полю и
        обработки роста змейки при поедании яблока.
        """

        head_position = self.get_head_position()

        dx, dy = self.direction

        new_x = head_position[0] + (dx * GRID_SIZE)

        new_y = head_position[1] + (dy * GRID_SIZE)

        if new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        elif new_x > SCREEN_WIDTH - GRID_SIZE:
            new_x = 0

        if new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE
        elif new_y > SCREEN_HEIGHT - GRID_SIZE:
            new_y = 0

        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if not grow:
            self.last = self.positions[-1]
            self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод для отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод для сброса игры при столкновении змейки с самой собой."""
        start_position = (((GRID_WIDTH // 2) * GRID_SIZE),
                          ((GRID_HEIGHT // 2) * GRID_SIZE))
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None


def handle_keys(game_object):
    """Функция для обработки нажатий клавиш
    и изменения направления движения змейки.
    """
    
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


def main():
    """Главная функция, которая запускает игру и содержит все основные циклы"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    grow = False

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(grow)
        grow = False
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            grow = False
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            grow = True
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
