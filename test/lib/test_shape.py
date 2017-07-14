from __future__ import print_function
from rgbmatrixtetris.lib.shape import Shape
import unittest


class ShapeTestCase(unittest.TestCase):
    COORDINATES = [
        [1, 1, 1, 1]
    ]

    shape = None

    def setUp(self):
        self.shape = Shape(self.COORDINATES)

    def test__init__(self):
        self.assertIsInstance(self.shape, Shape)

    def test_set_coordinates(self):
        self.assertIs(self.shape.set_coordinates([[1, 0, 0, 1]]), None)
        self.assertEquals(self.shape.coordinates(), [[1, 0, 0, 1]])

    def test_set_x(self):
        self.assertIs(self.shape.set_x(1), None)
        self.assertEquals(self.shape.x(), 1)

    def test_set_y(self):
        self.assertIs(self.shape.set_y(1), None)
        self.assertEquals(self.shape.y(), 1)

    def test_increment_x(self):
        self.assertIs(self.shape.increment_x(), None)
        self.assertEquals(self.shape.x(), 1)

    def test_increment_y(self):
        self.assertIs(self.shape.increment_y(), None)
        self.assertEquals(self.shape.y(), 1)

    def test_decrement_x(self):
        self.assertIs(self.shape.decrement_x(), None)
        self.assertEquals(self.shape.x(), -1)

    def test_decrement_y(self):
        self.assertIs(self.shape.decrement_y(), None)
        self.assertEquals(self.shape.y(), -1)

    def test_coordinates(self):
        self.assertEquals(self.shape.coordinates(), self.COORDINATES)

    def test_x(self):
        self.assertEquals(self.shape.x(), 0)

    def test_y(self):
        self.assertEquals(self.shape.y(), 0)

    def test_rotate_clockwise(self):
        self.shape.set_coordinates([[0, 0, 1], [1, 1, 1]])
        self.assertEquals(self.shape.rotate_clockwise(), [[1, 0], [1, 0], [1, 1]])

    def test_rotate_anti_clockwise(self):
        self.shape.set_coordinates([[0, 0, 1], [1, 1, 1]])
        self.assertEquals(self.shape.rotate_anti_clockwise(), [[1, 1], [0, 1], [0, 1]])

    def test_cleanup(self):
        self.assertIs(self.shape.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.shape.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
