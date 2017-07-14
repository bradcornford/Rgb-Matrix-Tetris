from __future__ import print_function
from board import Board
from mock import MagicMock, patch
from shape import Shape
from random import randrange as rand
from tinydb import TinyDB, Query
import datetime
import pygame
import sys


try:
    from rgbmatrix import RGBMatrix as RgbMatrix
    from rgbmatrix import RGBMatrixOptions as RgbMatrixOptions
    from rgbmatrix import graphics as Graphics
except ImportError:
    print("[Game][error] An error occurred importing 'rgbmatrix'")
    mock = MagicMock()
    mock.setmode.return_value = True
    mock.Font.return_value = True
    mock.RGBMatrix.return_value.options = True
    with patch.dict('sys.modules', {'rgbmatrix': mock, 'rgbmatrix.RGBMatrix': mock.RGBMatrix, 'rgbmatrix.RGBMatrixOptions': mock.RGBMatrixOptions, 'rgbmatrix.graphics': mock.graphics}):
        from rgbmatrix import RGBMatrix as RgbMatrix
        from rgbmatrix import RGBMatrixOptions as RgbMatrixOptions
        from rgbmatrix import graphics as Graphics

try:
    import RPi.GPIO as Gpio
except ImportError:
    print("[Game][error] An error occurred importing 'RPi.GPIO'")
    mock = MagicMock()
    mock.setmode.return_value = True
    mock.setup.return_value = True
    mock.add_event_detect.return_value = True
    mock.add_event_callback.return_value = True
    mock.output.return_value = True
    mock.input.return_value = True
    mock.cleanup.return_value = True
    with patch.dict('sys.modules', {'RPi': mock, 'RPi.GPIO': mock.GPIO}):
        import RPi.GPIO as Gpio


class Game:
    SWITCHES = None

    BLOCK_SIZE = 16

    COLUMNS = None
    ROWS = None

    SHAPES_NEXT_COUNT = None

    FPS = None

    COLORS = [
        # 0 - Black
        (0, 0, 0),
        # 1 - Purple
        (128, 0, 128),
        # 2 - Green
        (0, 255, 0),
        # 3 - Red
        (255, 0, 0),
        # 4 - Blue
        (0, 0, 255),
        # 5 - Orange
        (255, 165, 0),
        # 6 - Cyan
        (0, 255, 255),
        # 7 - Yellow
        (255, 255, 0),
        # 8 - Dark Grey
        (35, 35, 35),
        # 9 - White
        (255, 255, 255)
    ]

    SHAPES = [
        # T
        [
            [1, 1, 1],
            [0, 1, 0],
        ],

        # S
        [
            [0, 2, 2],
            [2, 2, 0]
        ],

        # Z
        [
            [3, 3, 0],
            [0, 3, 3]
        ],

        # J
        [
            [4, 0, 0],
            [4, 4, 4]
        ],

        # L
        [
            [0, 0, 5],
            [5, 5, 5],
        ],

        # I
        [
            [6, 6, 6, 6],
        ],

        # O
        [
            [7, 7],
            [7, 7],
        ]
    ]

    WIDTH = None
    HEIGHT = None

    COUNTDOWN = None

    SCORE_INCREMENTS = None

    LINES = 0
    SCORE = 0

    LEVEL = 1
    LEVEL_INCREMENT = None

    INTERVAL = None
    INTERVAL_INCREMENT = None

    PAUSED = False

    GAMEOVER = False

    BACKGROUND_GRID = None
    BACKGROUND_BOX = None

    RGB_MATRIX_HARDWARE = None
    RGB_MATRIX_ROWS = None
    RGB_MATRIX_CHAIN_LENGTH = None
    RGB_MATRIX_PARALLEL = None
    RGB_MATRIX_PWM_BITS = None
    RGB_MATRIX_BRIGHTNESS = None
    RGB_MATRIX_LSB_NANOSECONDS = None
    RGB_MATRIX_GPIO_SLOWDOWN = None

    pygame = None
    pygame_font = None
    pygame_screen = None
    pygame_clock = None

    rgbmatrix = None
    rgbmatrix_options = None
    rgbmatrix_font = None

    gpio = None
    db = None

    board = None
    shape = None
    shapes_next = None

    def __init__(self, switches, columns, rows, shapes_next_count, fps, countdown, interval, score_increments, level_increment, interval_increment, rgb_matrix_hardware, rgb_matrix_rows, rgb_matrix_chain_length, rgb_matrix_parallel, rgb_matrix_pwm_bits, rgb_matrix_brightness, rgb_matrix_lsb_nanoseconds, rgb_matrix_gpio_slowdown, rgb_matrix_disable_hardware_pulsing, rgb_matrix_rgb_sequence, pygame_instance=None):
        self.SWITCHES = switches
        self.COLUMNS = columns
        self.ROWS = rows
        self.SHAPES_NEXT_COUNT = shapes_next_count
        self.FPS = fps
        self.COUNTDOWN = countdown
        self.INTERVAL = interval
        self.SCORE_INCREMENTS = score_increments
        self.LEVEL_INCREMENT = level_increment
        self.INTERVAL_INCREMENT = interval_increment
        self.RGB_MATRIX_HARDWARE = rgb_matrix_hardware
        self.RGB_MATRIX_ROWS = rgb_matrix_rows
        self.RGB_MATRIX_CHAIN_LENGTH = rgb_matrix_chain_length
        self.RGB_MATRIX_PARALLEL = rgb_matrix_parallel
        self.RGB_MATRIX_PWM_BITS = rgb_matrix_pwm_bits
        self.RGB_MATRIX_BRIGHTNESS = rgb_matrix_brightness
        self.RGB_MATRIX_LSB_NANOSECONDS = rgb_matrix_lsb_nanoseconds
        self.RGB_MATRIX_GPIO_SLOWDOWN = rgb_matrix_gpio_slowdown
        self.RGB_MATRIX_DISABLE_HARDWARE_PULSING = rgb_matrix_disable_hardware_pulsing
        self.RGB_MATRIX_RGB_SEQUENCE = rgb_matrix_rgb_sequence

        self.gpio = Gpio

        self.rgbmatrix_options = RgbMatrixOptions()
        self.rgbmatrix_options.hardware_mapping = self.RGB_MATRIX_HARDWARE
        self.rgbmatrix_options.rows = self.RGB_MATRIX_ROWS
        self.rgbmatrix_options.chain_length = self.RGB_MATRIX_CHAIN_LENGTH
        self.rgbmatrix_options.parallel = self.RGB_MATRIX_PARALLEL
        self.rgbmatrix_options.pwm_bits = self.RGB_MATRIX_PWM_BITS
        self.rgbmatrix_options.brightness = self.RGB_MATRIX_BRIGHTNESS
        self.rgbmatrix_options.pwm_lsb_nanoseconds = self.RGB_MATRIX_LSB_NANOSECONDS
        self.rgbmatrix_options.gpio_slowdown = self.RGB_MATRIX_GPIO_SLOWDOWN
        self.rgbmatrix_options.disable_hardware_pulsing = self.RGB_MATRIX_DISABLE_HARDWARE_PULSING
        self.rgbmatrix_options.led_rgb_sequence = self.RGB_MATRIX_RGB_SEQUENCE

        if pygame_instance is None:
            self.pygame = pygame
        else:
            self.pygame = pygame_instance

        self.db = TinyDB('data/database.json')

        try:
            self.gpio.setmode(self.gpio.BCM)

            for switch in self.SWITCHES.keys():
                self.gpio.setup(switch, self.gpio.IN)

            self.WIDTH = self.BLOCK_SIZE * (self.COLUMNS + 12)
            self.HEIGHT = self.BLOCK_SIZE * (self.ROWS + 24)

            self.BACKGROUND_GRID = [
                [8 if x % 2 == y % 2 else 0 for x in xrange(self.COLUMNS)]
                for y in xrange(self.ROWS)
            ]
            self.BACKGROUND_BOX = [
                [9 if (x == 0 or x == self.COLUMNS + 1 or y == 0 or y == self.ROWS + 1) else 0 for x in xrange(self.COLUMNS + 2)]
                for y in xrange(self.ROWS + 2)
            ]

            self.pygame.init()
            self.pygame.key.set_repeat(150, 50)
            self.pygame_font = self.pygame.font.Font(self.pygame.font.get_default_font(), 12)
            self.pygame_screen = self.pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 24)
            self.pygame.display.set_caption('RGB Matrix Tetris')
            self.pygame.event.set_blocked(self.pygame.MOUSEMOTION)
            self.pygame.mouse.set_visible(0)
            self.pygame_clock = self.pygame.time.Clock()

            self.rgbmatrix = RgbMatrix(options=self.rgbmatrix_options)
            self.rgbmatrix_graphics = Graphics
            self.rgbmatrix_font = self.rgbmatrix_graphics.Font()
            self.rgbmatrix_font.LoadFont('./rgbmatrixtetris/fonts/4x6.bdf')

            self.board = Board(self.COLUMNS, self.ROWS)
            self.__generate_shapes()
        except AttributeError:
            print("[Game][error] An error occurred initialising game")

    def start(self, run_once=False):
        print("[Game][info] Starting game")

        try:
            self.rgbmatrix.Clear()
            self.pygame_screen.fill((0, 0, 0))
            self.__display_message("Press\n\nenter\n\nto\n\nstart")
            self.pygame.display.update()
            pygame_wait = True

            while pygame_wait:
                try:
                    for event in self.pygame.event.get():
                        if event.type == self.pygame.KEYDOWN:
                            if event.key == self.pygame.K_RETURN:
                                pygame_wait = False
                            elif event.key == self.pygame.K_ESCAPE:
                                self.quit()
                        elif event.type == self.pygame.QUIT:
                            self.quit()
                except KeyboardInterrupt:
                    self.quit()
        except AttributeError:
            print("[Game][error] An error occurred starting game")

        self.__countdown()
        self.__loop()
        self.finish()

        if run_once is not True:
            self.start()

    def __countdown(self):
        print("[Game][info] Starting game countdown")
        try:
            start_ticks = self.pygame.time.get_ticks()

            while True:
                seconds = (self.pygame.time.get_ticks() - start_ticks) / 1000
                self.rgbmatrix.Clear()
                self.pygame_screen.fill((0, 0, 0))
                remaining = (self.COUNTDOWN - seconds)

                if seconds > self.COUNTDOWN:
                    break

                if seconds == self.COUNTDOWN:
                    self.__display_message("Go!")
                elif seconds == 0:
                    self.__display_message("Starting\n\nin %d!" % remaining)
                else:
                    self.__display_message("%d!" % remaining)

                self.pygame.display.update()
                self.pygame.time.wait(1000)
        except AttributeError:
            print("[Game][error] An error occurred starting game countdown")

    def __loop(self):
        print("[Game][info] Starting game loop")

        try:
            self.pygame.time.set_timer(pygame.USEREVENT + 1, self.INTERVAL)

            key_actions = {
                'ESCAPE': lambda: self.quit(),
                'LEFT': lambda: self.__move(-1),
                'RIGHT': lambda: self.__move(+1),
                'DOWN': lambda: self.__drop(True),
                'UP': lambda: self.__rotate_shape(),
                'p': lambda: self.toggle_pause(),
                'RETURN': lambda: self.__instant_drop()
            }

            start_ticks = self.pygame.time.get_ticks()

            while not self.GAMEOVER:
                self.pygame_clock.tick(self.FPS)
                rgbmatrix_canvas = self.rgbmatrix.CreateFrameCanvas()
                self.pygame_screen.fill((0, 0, 0))

                if self.PAUSED:
                    self.__display_message("Paused", None, self.COLORS[9], self.COLORS[0], None)
                else:
                    self.__display_message("Next:", ((self.COLUMNS + 3), 1), self.COLORS[9], self.COLORS[0], None, False)
                    self.__display_message("Time: \n\n\n\n\nScore: \n\n\n\n\nLines: \n\n\n\n\nLevel:", (1, (self.ROWS + 3)), self.COLORS[9], self.COLORS[0], None, False)

                    self.__display_message("%s" % (str(datetime.timedelta(seconds=((self.pygame.time.get_ticks() - start_ticks) / 1000)))), (1, (self.ROWS + 8)), self.COLORS[3], self.COLORS[0], (60, './rgbmatrixtetris/fonts/4x6.bdf'), rgbmatrix_canvas)
                    self.__display_message("%d" % (self.SCORE), (1, (self.ROWS + 14)), self.COLORS[2], self.COLORS[0], (60, './rgbmatrixtetris/fonts/4x6.bdf'), rgbmatrix_canvas)
                    self.__display_message("%d" % (self.LINES), (1, (self.ROWS + 20)), self.COLORS[5], self.COLORS[0], (60, './rgbmatrixtetris/fonts/4x6.bdf'), rgbmatrix_canvas)
                    self.__display_message("%d" % (self.LEVEL), (1, (self.ROWS + 26)), self.COLORS[6], self.COLORS[0], (60, './rgbmatrixtetris/fonts/4x6.bdf'), rgbmatrix_canvas)

                    self.__draw_matrix(self.BACKGROUND_GRID, (1, 1), None, False)
                    self.__draw_matrix(self.board.coordinates(), (1, 1), None, rgbmatrix_canvas)
                    self.__draw_matrix(self.shape.coordinates(), self.shape.position((1, 1)), None, rgbmatrix_canvas)
                    self.__draw_matrix(self.BACKGROUND_BOX, (0, 0), None, rgbmatrix_canvas)

                    for i in range(0, (self.SHAPES_NEXT_COUNT - 1)):
                        self.__draw_matrix(self.shapes_next[i].coordinates(), ((self.COLUMNS + 3), (((i + 1) * 5) - 2)), None, rgbmatrix_canvas)

                rgbmatrix_canvas = self.rgbmatrix.SwapOnVSync(rgbmatrix_canvas)
                self.pygame.display.update()

                try:
                    for event in self.pygame.event.get():
                        if event.type == self.pygame.USEREVENT + 1 and not self.PAUSED:
                            self.__drop(False)
                        elif event.type == self.pygame.QUIT:
                            self.quit()
                        elif event.type == self.pygame.KEYDOWN:
                            for key in key_actions:
                                if event.key == eval("self.pygame.K_" + key):
                                    key_actions[key]()
                except KeyboardInterrupt:
                    self.quit()
        except AttributeError:
            print("[Game][error] An error occurred during game loop")

    def __button_press(self, channel):
        print("[Game][info] Button pressed: %d" % channel)

        event = self.pygame.event.Event(self.pygame.KEYDOWN, key=eval("self.pygame.K_" + self.SWITCHES[channel]), trigger='gpio')
        self.pygame.event.post(event)

    def __generate_shapes(self):
        print("[Game][info] Generating next shapes")

        self.shapes_next = [Shape(self.SHAPES[rand(len(self.SHAPES))]) for x in xrange(self.SHAPES_NEXT_COUNT)]
        self.__next_shape()

    def __next_shape(self):
        print("[Game][info] Getting next shape")

        self.shape = self.shapes_next.pop(0)
        self.shapes_next.append(Shape(self.SHAPES[rand(len(self.SHAPES))]))

        self.shape.set_x(int(self.COLUMNS / 2 - len(self.shape.coordinates()[0]) / 2))
        self.shape.set_y(0)

        if self.board.check_collision(self.shape, self.shape.position()):
            self.GAMEOVER = True

    def __display_message(self, message, coordinates=None, color=COLORS[9], background_color=COLORS[0], message_size=None, rgbmatrix=None):
        print("[Game][info] Displaying message")

        for i, line in enumerate(message.splitlines()):
            pygame_message_font = self.pygame_font
            rgbmatrix_message_font = self.rgbmatrix_font

            if message_size is not None:
                pygame_message_size, rgbmatrix_message_size = message_size
                pygame_message_font = self.pygame.font.Font(self.pygame.font.get_default_font(), pygame_message_size)
                rgbmatrix_message_font = self.rgbmatrix_graphics.Font()
                rgbmatrix_message_font.LoadFont(rgbmatrix_message_size)

            pygame_message_image = pygame_message_font.render(line, False, color, background_color)

            if coordinates is not None:
                pygame_position_x, pygame_position_y = coordinates
                pygame_position_x = (pygame_position_x * self.BLOCK_SIZE)
                pygame_position_y = (pygame_position_y * self.BLOCK_SIZE)
                rgbmatrix_position_x, rgbmatrix_position_y = coordinates
            else:
                pygame_message_image_center_x, pygame_message_image_center_y = pygame_message_image.get_size()
                pygame_message_image_center_x //= 2
                pygame_message_image_center_y //= 2
                pygame_position_x = (self.WIDTH // 2 - pygame_message_image_center_x)
                pygame_position_y = (self.HEIGHT // 2 - pygame_message_image_center_y + i)
                rgbmatrix_position_x = (self.WIDTH / self.BLOCK_SIZE - (4 * len(line))) // 2
                rgbmatrix_position_y = (((self.HEIGHT / self.BLOCK_SIZE - rgbmatrix_message_font.height) // 2) + (i * 3))

            if rgbmatrix is not False:
                if rgbmatrix is None:
                    rgbmatrix = self.rgbmatrix

                r, g, b = color
                self.rgbmatrix_graphics.DrawText(rgbmatrix, rgbmatrix_message_font, rgbmatrix_position_x, rgbmatrix_position_y, self.rgbmatrix_graphics.Color(r, g, b), line)

            self.pygame_screen.blit(
                pygame_message_image,
                (pygame_position_x, pygame_position_y)
            )

    def __draw_line(self, start_position, end_position, color=COLORS[9], rgbmatrix=True):
        print("[Game][info] Drawing line")

        if rgbmatrix:
            r, g, b = color
            start_x, start_y = start_position
            end_x, end_y = end_position
            self.rgbmatrix_graphics.DrawLine(self.rgbmatrix, start_x, start_y, end_x, end_y, self.rgbmatrix_graphics.Color(r, g, b))

        self.pygame.draw.line(self.pygame_screen, color, start_position, end_position)

    def __draw_matrix(self, matrix, offset, color=None, rgbmatrix=None):
        print("[Game][info] Drawing matrix")

        off_x, off_y = offset

        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    if color is None:
                        shape_color = self.COLORS[val]
                    else:
                        shape_color = color

                    if rgbmatrix is not False:
                        if rgbmatrix is None:
                            rgbmatrix = self.rgbmatrix

                        r, g, b = shape_color
                        rgbmatrix.SetPixel((off_x + x), (off_y + y), r, g, b)

                    self.pygame.draw.rect(
                        self.pygame_screen,
                        shape_color,
                        self.pygame.Rect((off_x + x) * self.BLOCK_SIZE, (off_y + y) * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE),
                        0
                    )

    def __count_clear_rows(self, rows):
        print("[Game][info] Counting cleared rows")

        self.LINES += rows
        self.SCORE += self.SCORE_INCREMENTS[rows] * self.LEVEL

        if self.LINES >= self.LEVEL * self.LEVEL_INCREMENT:
            self.LEVEL += 1
            delay = self.INTERVAL - self.INTERVAL_INCREMENT * (self.LEVEL - 1)
            delay = 100 if delay < 100 else delay
            self.pygame.time.set_timer(self.pygame.USEREVENT + 1, delay)

    def __move(self, delta_x):
        print("[Game][info] Moving shape")

        if not self.GAMEOVER and not self.PAUSED:
            new_x = self.shape.x() + delta_x

            if new_x < 0:
                new_x = 0

            if new_x > self.COLUMNS - len(self.shape.coordinates()[0]):
                new_x = self.COLUMNS - len(self.shape.coordinates()[0])

            if not self.board.check_collision(self.shape, (new_x, self.shape.y())):
                self.shape.set_x(new_x)

    def __drop(self, manual):
        print("[Game][info] Drop shape")

        if not self.GAMEOVER and not self.PAUSED:
            self.SCORE += 1 if manual else 0
            self.shape.set_y(self.shape.y() + 1)

            if self.board.check_collision(self.shape, self.shape.position()):
                self.board.join_matrixes(self.shape, self.shape.position())
                self.__next_shape()
                cleared_rows = 0

                while True:
                    for i, row in enumerate(self.board.coordinates()[:-1]):
                        if 0 not in row:
                            self.board.clear_row(i)
                            cleared_rows += 1
                            break
                    else:
                        break

                self.__count_clear_rows(cleared_rows)

                return True

        return False

    def __instant_drop(self):
        print("[Game][info] Instant drop shape")

        if not self.GAMEOVER and not self.PAUSED:
            while not self.__drop(True):
                pass

    def __rotate_shape(self, direction='clockwise'):
        print("[Game][info] Rotating shape %s" % (direction))

        if not self.GAMEOVER and not self.PAUSED:
            new_coordinates = (0, 0)

            if direction == 'clockwise':
                new_coordinates = self.shape.rotate_clockwise()
            elif direction == 'anti-clockwise':
                new_coordinates = self.shape.rotate_anti_clockwise()

            if not self.board.check_collision(Shape(new_coordinates), self.shape.position()):
                self.shape.set_coordinates(new_coordinates)

    def toggle_pause(self):
        print("[Game][info] Toggling paused state")

        self.PAUSED = not self.PAUSED

    def get_score(self):
        print("[Game][info] Calculating score")

        return self.SCORE

    def print_score(self):
        print("[Game][info] Printing score")

        score = self.get_score()

        try:
            self.__display_message("Game\n\nOver!\n\nYour\n\nscore:\n\n%d" % score)
            self.pygame.display.update()
            self.pygame.time.wait(3000)
        except AttributeError:
            print("[Game][error] An error occurred printing score")

    def print_high_score(self):
        print("[Game][info] Printing high score: %d" % self.get_score())

        try:
            self.__display_message("Game\n\nOver!\n\nHigh\n\nscore:\n\n%d!" % self.get_score())
            self.pygame.display.update()
            self.pygame.time.wait(3000)
        except AttributeError:
            print("[Game][error] An error occurred printing high score")

    def finish(self):
        print("[Game][info] Finishing game")

        score = self.get_score()

        self.rgbmatrix.Clear()
        self.pygame_screen.fill((0, 0, 0))

        if self.db.contains(Query().score >= score):
            self.print_score()
        else:
            self.print_high_score()

        self.db.insert({'score': score})
        self.reset()

    def quit(self):
        print("[Game][info] Quitting game")

        self.rgbmatrix.Clear()
        self.pygame_screen.fill((0, 0, 0))
        self.__display_message("Quit...")
        self.pygame.display.update()
        self.pygame.quit()
        sys.exit()

    def reset(self):
        print("[Game][info] Resetting game")

        self.PAUSED = False
        self.GAMEOVER = False
        self.SCORE = 0
        self.LINES = 0
        self.LEVEL = 1

        self.board = Board(self.COLUMNS, self.ROWS)
        self.shape = None
        self.shapes_next = None
        self.__generate_shapes()

        self.pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        self.pygame.display.update()

    def cleanup(self):
        print("[Game][info] Game clean up")

        try:
            self.rgbmatrix.Clear()
        except AttributeError:
            print("[Game][error] An error occurred cleaning up")

    def __exit__(self):
        print("[Game][info] Game exit")

        self.cleanup()
