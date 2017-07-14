from __future__ import print_function
from rgbmatrixtetris.lib.game import Game
from mock import MagicMock
import unittest


class GameTestCase(unittest.TestCase):
    SWITCHES = {17: ''}
    COLUMNS = 1
    ROWS = 1
    SHAPES_NEXT_COUNT = 1
    FPS = 0
    COUNTDOWN = 0
    INTERVAL = 1000
    SCORE_INCREMENTS = [
        0,
        1
    ]
    LEVEL_INCREMENT = 10
    INTERVAL_INCREMENT = 50
    RGB_MATRIX_HARDWARE = 'regular'
    RGB_MATRIX_ROWS = 1
    RGB_MATRIX_CHAIN_LENGTH = 1
    RGB_MATRIX_PARALLEL = 1
    RGB_MATRIX_PWM_BITS = 1
    RGB_MATRIX_BRIGHTNESS = 1
    RGB_MATRIX_LSB_NANOSECONDS = 1
    RGB_MATRIX_LED_SLOWDOWN_GPIO = 1
    RGB_MATRIX_DISABLE_HARDWARE_PULSING = 1
    RGB_MATRIX_RGB_SEQUENCE = 1

    game = None

    def setUp(self):
        mock = MagicMock()

        keypress_event_mock = MagicMock()
        keypress_event_mock.type = 1
        keypress_event_mock.key = 1

        userevent_event_mock = MagicMock()
        userevent_event_mock.type = 3

        mock.get_size.return_value = (0, 0)
        mock.get.return_value = [keypress_event_mock, userevent_event_mock]
        mock.get_ticks.side_effect = [0, 6000, 0, 5000]

        mock.Font.return_value = mock
        mock.render.return_value = mock

        mock.KEYDOWN = 1
        mock.K_RETURN = 1
        mock.USEREVENT = 2

        mock.font = mock
        mock.display = mock
        mock.event = mock
        mock.time = mock

        self.game = Game(
            self.SWITCHES,
            self.COLUMNS,
            self.ROWS,
            self.SHAPES_NEXT_COUNT,
            self.FPS,
            self.COUNTDOWN,
            self.INTERVAL,
            self.SCORE_INCREMENTS,
            self.LEVEL_INCREMENT,
            self.INTERVAL_INCREMENT,
            self.RGB_MATRIX_HARDWARE,
            self.RGB_MATRIX_ROWS,
            self.RGB_MATRIX_CHAIN_LENGTH,
            self.RGB_MATRIX_PARALLEL,
            self.RGB_MATRIX_PWM_BITS,
            self.RGB_MATRIX_BRIGHTNESS,
            self.RGB_MATRIX_LSB_NANOSECONDS,
            self.RGB_MATRIX_LED_SLOWDOWN_GPIO,
            self.RGB_MATRIX_DISABLE_HARDWARE_PULSING,
            self.RGB_MATRIX_RGB_SEQUENCE,
            mock
        )

    def test__init__(self):
        self.assertIsInstance(self.game, Game)

    def test_start(self):
        self.assertIs(self.game.start(True), None)

    def test_toggle_pause(self):
        self.assertIs(self.game.toggle_pause(), None)
        self.assertEqual(self.game.PAUSED, True)
        self.assertIs(self.game.toggle_pause(), None)
        self.assertEqual(self.game.PAUSED, False)

    def test_get_score(self):
        self.assertIs(self.game.get_score(), 0)

    def test_print_score(self):
        self.assertIs(self.game.print_score(), None)

    def test_print_high_score(self):
        self.assertIs(self.game.print_high_score(), None)

    def test_finish(self):
        self.assertIs(self.game.finish(), None)

    def test_quit(self):
        with self.assertRaises(SystemExit):
            self.assertIs(self.game.quit(), None)

    def test_reset(self):
        self.assertIs(self.game.reset(), None)

    def test_cleanup(self):
        self.assertIs(self.game.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.game.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
