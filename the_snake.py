from random import randint

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (255, 255, 0)

# Скорость движения змейки (кадров в секунду)
SPEED = 20


# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов на поле."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        position = self.randomize_position()
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        """Устанавливает яблоку случайную позицию на поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
        return (x, y)

    def draw(self):
        """Отрисовывает яблоко на поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        start_position = (
            (GRID_WIDTH // 2) * GRID_SIZE,
            (GRID_HEIGHT // 2) * GRID_SIZE
        )
        self.positions = [start_position]
        super().__init__(start_position, SNAKE_COLOR)
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет текущее направление, если есть зарезервированное."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow):
        """Перемещает змейку и управляет ростом."""
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_x = head_position[0] + dx * GRID_SIZE
        new_y = head_position[1] + dy * GRID_SIZE

        # Прохождение сквозь стены
        if new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        elif new_x >= SCREEN_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE
        elif new_y >= SCREEN_HEIGHT:
            new_y = 0

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if not grow:
            self.last = self.positions.pop()
        else:
            self.last = None
            self.length += 1

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затираем старый хвост, если змейка не выросла
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        start_position = (
            (GRID_WIDTH // 2) * GRID_SIZE,
            (GRID_HEIGHT // 2) * GRID_SIZE
        )
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и выход из игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    grow = False

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move(grow)
        grow = False

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            grow = True

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
