from __future__ import print_function


class Board:
    COLUMNS = None

    ROWS = None

    COORDINATES = None

    def __init__(self, columns, rows):
        print("[Board][info] Initialising Board")

        self.COLUMNS = columns
        self.ROWS = rows
        self.__generate()

    def __generate(self):
        self.COORDINATES = [
            [0 for x in xrange(self.COLUMNS)]
            for y in xrange(self.ROWS)
        ]
        self.COORDINATES += [
            [1 for x in xrange(self.COLUMNS)]
        ]

    def columns(self):
        print("[Board][info] Getting Board columns")

        return self.COLUMNS

    def rows(self):
        print("[Board][info] Getting Board rows")

        return self.ROWS

    def coordinates(self):
        print("[Board][info] Getting Board coordinates")

        return self.COORDINATES

    def join_matrixes(self, shape, shape_offset):
        print("[Board][info] Joining Board and Shape matrixes")

        offset_x, offset_y = shape_offset

        for current_y, row in enumerate(shape.coordinates()):
            for current_x, val in enumerate(row):
                self.COORDINATES[current_y + offset_y - 1][current_x + offset_x] += val

    def check_collision(self, shape, coordinates):
        print("[Board][info] Checking for Shape collision")

        coordinates_x, coordinates_y = coordinates

        for current_y, row in enumerate(shape.coordinates()):
            for current_x, cell in enumerate(row):
                try:
                    if cell and self.COORDINATES[current_y + coordinates_y][current_x + coordinates_x]:
                        return True
                except IndexError:
                    return True

        return False

    def clear_row(self, row):
        print("[Board][info] Clearing row from coordinates")

        del self.COORDINATES[row]

        self.COORDINATES = [[0 for i in xrange(self.COLUMNS)]] + self.COORDINATES

    def clear(self):
        print("[Board][info] Clearing board")

        self.COORDINATES = None
        self.COLUMNS = None
        self.ROWS = None

    def cleanup(self):
        print("[Board][info] Board clean up")

        self.clear()

    def __exit__(self):
        print("[Board][info] Board exit")

        self.cleanup()
