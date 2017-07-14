from __future__ import print_function
from rgbmatrixtetris.lib.board import Board
from rgbmatrixtetris.lib.shape import Shape
import unittest


class BoardTestCase(unittest.TestCase):
    COLUMNS = 2
    ROWS = 2

    board = None

    def setUp(self):
        self.board = Board(self.COLUMNS, self.ROWS)

    def test__init__(self):
        self.assertIsInstance(self.board, Board)

    def test_columns(self):
        self.assertEquals(self.board.columns(), self.COLUMNS)

    def test_rows(self):
        self.assertEquals(self.board.rows(), self.ROWS)

    def test_coordinates(self):
        self.assertEquals(self.board.coordinates(), [[0, 0], [0, 0], [1, 1]])

    def test_join_matrixes(self):
        shape = Shape([[1]])
        self.assertIs(self.board.join_matrixes(shape, (shape.x(), shape.y())), None)
        self.assertEquals(self.board.coordinates(), [[0, 0], [0, 0], [2, 1]])

    def test_check_collision(self):
        shape = Shape([[1]])
        self.assertIs(self.board.check_collision(shape, (shape.x(), shape.y())), False)

    def test_clear_row(self):
        self.assertIs(self.board.clear_row(2), None)
        self.assertEquals(self.board.coordinates(), [[0, 0], [0, 0], [0, 0]])

    def test_clear(self):
        self.assertIs(self.board.clear(), None)

    def test_cleanup(self):
        self.assertIs(self.board.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.board.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
