from functools import reduce
from collections import defaultdict
import re
from guts.loader import Loader

class Solver:
    def __init__(self, path: str):
        self._path: str = path
        self._grid = defaultdict(lambda: 0)

    # Bresenham's algo
    @staticmethod
    def bresenham_line(x0, y0, x1, y1):
        # steep
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # endpoint swap
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # ystep
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        # init
        deltax = x1 - x0
        deltay = abs(y1 - y0)
        error = -deltax / 2
        y = y0

        # main loop
        for x in range(x0, x1 + 1): # We add 1 to x1 so that the range includes x1
            if steep:
                yield (y,x)
            else:
                yield (x,y)
            error = error + deltay
            if error > 0:
                y = y + ystep
                error = error - deltax

    @staticmethod
    def decode_command(command: str):
        return tuple(
            int(value)
            for value in re.match(
                (
                    r'(?P<x1>\d+),'
                    r'(?P<y1>\d+) -> '
                    r'(?P<x2>\d+),'
                    r'(?P<y2>\d+)'
                ),
                command
            ).groups()
        )

    def draw_line(self, command: str):
        for position in self.bresenham_line(
            *self.decode_command(command)
        ):
            self._grid[position] += 1


    def _load(self):
        loader = Loader(self._path).read()
        for command in loader:
            self.draw_line(command)

    def _bound(self):
        keys = self._grid.keys()

        return (
            max(x for x,_ in keys),
            max(y for _,y in keys),
        )

    def _display(self):
        lx, ly = self._bound()

        for y in range(lx + 1):
            for x in range(ly +1):
                pos = (x,y)
                v = self._grid[pos]
                print(v if v else '.', end='')
            print()
        print()

    @property
    def result(self):
        self._load()

        total = 0
        for value in self._grid.values():
            total += (1 if value > 1 else 0)

        return total

def test_solver():
    actual = Solver('day5_input_test.txt').result

    assert 12 == actual


if __name__ == '__main__':
    print(
        Solver('day5_input.txt').result
    )
