import threading

import atexit
import pygame
import os


start_event = threading.Event()

pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600

# Цвета
BLACK = (0, 0, 0)
RED = (200, 50, 70)

class Style:
    walls = (10, 10, 10)
    cells = (230, 230, 230)
    coins = (240, 200, 10)
    flag = (10, 230, 10)

# Размеры клетки
CELL_SIZE = 50

# Количество клеток по ширине и высоте
cells_width = screen_width // CELL_SIZE
cells_height = screen_height // CELL_SIZE

field = [[False for _x in range(cells_width)] for _y in range(cells_height)]
coins = [[False for _x in range(cells_width)] for _y in range(cells_height)]
flags = [[False for _x in range(cells_width)] for _y in range(cells_height)]

for x in range(cells_width):
    field[0][x] = field[cells_height - 1][x] = True

for y in range(cells_height):
    field[y][0] = field[y][cells_width - 1] = True


def draw_field(screen):
    for y in range(cells_height):
        for x in range(cells_width):
            if not field[y][x]:
                pygame.draw.rect(
                    screen,
                    Style.cells,
                    (
                        x * CELL_SIZE + 1,
                        y * CELL_SIZE + 1,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2,
                    ),
                )
            if coins[y][x]:
                pygame.draw.circle(
                    screen,
                    Style.coins,
                    (
                        x * CELL_SIZE + 7,
                        y * CELL_SIZE + 7,
                    ),
                    5
                )
            if flags[y][x]:
                pygame.draw.circle(
                    screen,
                    Style.flag,
                    (
                        x * CELL_SIZE + 7,
                        y * CELL_SIZE + 17,
                    ),
                    5
                )


class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 3
        self.y = 4
        self.dir_x = 0
        self.dir_y = -1
        self.color = BLACK
        self.finished = False
        self.lock = threading.Lock()
        self.ms = 700

    def draw(self, screen):
        with self.lock:
            pygame.draw.rect(
                screen,
                self.color,
                (
                    self.x * CELL_SIZE + 10,
                    self.y * CELL_SIZE + 10,
                    CELL_SIZE - 20,
                    CELL_SIZE - 20,
                ),
            )
            x = (self.x + 0.5 + 0.3 * self.dir_x) * CELL_SIZE - 5
            y = (self.y + 0.5 + 0.3 * self.dir_y) * CELL_SIZE - 5
            pygame.draw.rect(
                screen,
                RED,
                (
                    x,
                    y,
                    10,
                    10,
                ),
            )

    def pause(self, ms=None):
        pygame.time.wait(ms or self.ms)

    def go(self):
        do_exit = False
        with self.lock:
            self.x += self.dir_x
            self.y += self.dir_y

            if field[self.y][self.x]:
                self.color = RED
                do_exit = True

        if do_exit:
            self.pause(2000)
            os._exit(2)

        self.pause()

    def right(self):
        with self.lock:
            self.dir_x, self.dir_y = -self.dir_y, self.dir_x

        self.pause()

    def left(self):
        with self.lock:
            self.dir_x, self.dir_y = self.dir_y, -self.dir_x

        self.pause()

    def wall(self):
        with self.lock:
            return field[self.y + self.dir_y][self.x + self.dir_x]

    def wall_right(self):
        with self.lock:
            dir_x, dir_y = -self.dir_y, self.dir_x
            return field[self.y + dir_y][self.x + dir_x]

    def move(self, x, y):
        with self.lock:
            self.x = x
            self.y = y

    def coin(self):
        with self.lock:
            return coins[self.y][self.x]

    def flag(self):
        with self.lock:
            return flags[self.y][self.x]

    def set_flag(self):
        with self.lock:
            flags[self.y][self.x] = True


robot = Robot()

def go():
    robot.go()

def right():
    robot.right()

def left():
    robot.left()

def wall():
    return robot.wall()

def wall_right():
    return robot.wall_right()

def coin():
    return robot.coin()

def flag():
    return robot.flag()

def set_flag():
    return robot.set_flag()


def main_loop():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Клетчатое поле")
    clock = pygame.time.Clock()

    # Основной игровой цикл
    cur_type = "w"
    started = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os._exit(1)
                elif event.key == pygame.K_w:
                    cur_type = "w"
                elif event.key == pygame.K_c:
                    cur_type = "c"
            elif event.type == pygame.MOUSEWHEEL:
                robot.ms = int(max(10, min(1000, robot.ms + event.y * 0.1 * robot.ms)))
            elif event.type == pygame.MOUSEBUTTONDOWN and not started:
                # Получение позиции клика мыши
                mouse_pos = pygame.mouse.get_pos()
                # Преобразование позиции в координаты клетки
                cell_x = mouse_pos[0] // CELL_SIZE
                cell_y = mouse_pos[1] // CELL_SIZE

                if cell_x < cells_width and cell_y < cells_height:
                    if event.button == 1:
                        if cur_type == "w":
                            field[cell_y][cell_x] = not field[cell_y][cell_x]
                        elif cur_type == "c":
                            coins[cell_y][cell_x] = not coins[cell_y][cell_x]
                    elif event.button == 3:
                        robot.move(cell_x, cell_y)
                        started = True
                        start_event.set()

        clock.tick(50)

        screen.fill(Style.walls)

        draw_field(screen)

        if started:
            robot.draw(screen)

        # Обновление экрана
        pygame.display.flip()

        # Обработка событий
        pygame.display.update()

    pygame.quit()


thread = threading.Thread(target=main_loop)
thread.start()
start_event.wait()
robot.pause()

def finalize():
    print("stop")
    thread.join()
    pygame.quit()

atexit.register(finalize)
