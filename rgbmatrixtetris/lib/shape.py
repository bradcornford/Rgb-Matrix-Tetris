from __future__ import print_function


class Shape:
    COORDINATES = None

    X = None
    Y = None

    def __init__(self, coordinates, x=0, y=0):
        print("[Shape][info] Initialising Shape")

        self.COORDINATES = coordinates
        self.X = x
        self.Y = y

    def set_coordinates(self, coordinates):
        print("[Shape][info] Setting Shape coordinates")

        self.COORDINATES = coordinates

    def set_x(self, x):
        print("[Shape][info] Setting Shape X position")

        self.X = x

    def set_y(self, y):
        print("[Shape][info] Setting Shape Y position")

        self.Y = y

    def set_position(self, coordinates):
        print("[Shape][info] Setting Apple X, Y position")

        x, y = coordinates

        self.X = x
        self.Y = y

    def increment_x(self, increment=1):
        print("[Shape][info] Increment Shape X position by %d" % (increment))

        self.X += increment

    def increment_y(self, increment=1):
        print("[Shape][info] Increment Shape Y position by %d" % (increment))

        self.Y += increment

    def decrement_x(self, decrement=1):
        print("[Shape][info] Decrement Shape X position by %d" % (decrement))

        self.X -= decrement

    def decrement_y(self, decrement=1):
        print("[Shape][info] Decrement Shape Y position by %d" % (decrement))

        self.Y -= decrement

    def coordinates(self):
        print("[Shape][info] Getting Shape coordinates")

        return self.COORDINATES

    def x(self):
        print("[Shape][info] Getting Shape X position")

        return self.X

    def y(self):
        print("[Shape][info] Getting Shape Y position")

        return self.Y

    def position(self, offset=(0, 0)):
        print("[Shape][info] Getting Shape X,Y position")

        offset_x, offset_y = offset

        return ((self.X + offset_x), (self.Y + offset_y))

    def rotate_clockwise(self):
        print("[Shape][info] Rotating Shape clockwise")

        return [
            [
                self.COORDINATES[y][x]
                for y in xrange(len(self.COORDINATES) - 1, -1, -1)
            ]
            for x in xrange(len(self.COORDINATES[0]))
        ]

    def rotate_anti_clockwise(self):
        print("[Shape][info] Rotating Shape anti-clockwise")

        return [
            [
                self.COORDINATES[y][x]
                for y in xrange(len(self.COORDINATES))
            ]
            for x in xrange(len(self.COORDINATES[0]) - 1, -1, -1)
        ]

    def clear(self):
        print("[Shape][info] Clearing Shape")

        self.COORDINATES = None
        self.X = None
        self.Y = None

    def cleanup(self):
        print("[Shape][info] Shape clean up")

        self.clear()

    def __exit__(self):
        print("[Shape][info] Shape exit")

        self.cleanup()
