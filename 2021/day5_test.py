from functools import reduce
from collections import defaultdict
import re
from guts.loader import Loader

class Solver:
    def __init__(self, path: str):
        self._path: str = path
        self._grid = defaultdict(lambda: 0)

    @staticmethod
    def my_range(b, e):
        return range(min(b,e),max(b,e) +1)

    def draw_line(self, command: str):
        x1, y1, x2, y2 = [
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
        ]

        if x1 == x2:
            for y in self.my_range(y1, y2):
                self._grid[(x1, y)] +=1
        if y1 == y2:
            for x in self.my_range(x1, x2):
                self._grid[(x, y1)] +=1

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

    assert 5 == actual


if __name__ == '__main__':
    print(
        Solver('day5_input.txt').result
    )
