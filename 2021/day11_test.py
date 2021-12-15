from collections import defaultdict, namedtuple
from os import system
from time import sleep

from guts.loader import Loader

Position = namedtuple('Position', ('x', 'y'))


class Octopus:
    MAP = '🌕🌖🌗🌘🌑🌑🌑🌑🌑🌓'

    def __init__(self, value):
        self._value = value
        self._has_flashed = False

    def __repr__(self):
        return self.MAP[self._value] + '  '

    def set_neighboor(self, neighboor):
        self._neighboor = neighboor

    def reset(self):
        self._has_flashed = False

    def step(self):
        if self._has_flashed:
            return 0

        self._value += 1

        if self._value > 9:
            self._value = 0
            self._has_flashed = True
            yield 1

            for n in self._neighboor:
                if n is not None:
                    yield from n.step()


class Grid(dict):
    OFFSET_MAP = [
        Position(x, y)
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        if (x, y) != (0, 0)
    ]

    def __init__(self, matrix):
        self.load(matrix)
        self._counter = 0

    def __repr__(self):
        def display():
            y = 0
            for position, octopus in self.items():
                if position.y != y:
                    yield "\n\n"
                yield str(octopus)
                y = position.y
        return ''.join(
            display()
        )

    def load(self, matrix):
        # init grid
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                self.update(
                    {
                        Position(x, y): Octopus(
                            int(value)
                        )
                    }
                )
        # set neighboorhood
        for position, octopus in self.items():
            octopus.set_neighboor(
                [
                    self.get(
                        Position(
                            position.x + offset.x,
                            position.y + offset.y,
                        )
                    )
                    for offset in self.OFFSET_MAP
                ]
            )

    def step(self):
        self._counter += 1

        for octopus in self.values():
            yield from octopus.step()

        for octopus in self.values():
            octopus.reset()


class Solver:
    def step(self, matrix):
        grid = Grid(matrix)
        r = sum(grid.step())

        return str(grid).split()

    def process(self, path, steps):
        grid = Grid(Loader(path).read())

        for _ in range(steps):
            yield from grid.step()

    def simultaneous(self, path):
        grid = Grid(Loader(path).read())
        while True:
            r = sum(grid.step())
            system('clear')
            print(grid)
            sleep(1/12)
            if r >= len(grid):
                return grid._counter


def test_solver():
    solver = Solver()

    step0 = [
        '11111',
        '19991',
        '19191',
        '19991',
        '11111',
    ]

    step1 = solver.step(step0)

    assert step1 == [
        '34543',
        '40004',
        '50005',
        '40004',
        '34543',
    ]

    step2 = solver.step(step1)

    assert step2 == [
        '45654',
        '51115',
        '61116',
        '51115',
        '45654',
    ]


def test_process():
    solver = Solver()

    r = solver.process('day11_input_test.txt', 100)
    assert 1656 == sum(r)


if __name__ == '__main__':
    solver = Solver()
    print(
        sum(
            solver.process('day11_input.txt', 100)
        ),
        solver.simultaneous('day11_input.txt')
    )
