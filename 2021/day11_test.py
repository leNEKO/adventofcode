from collections import namedtuple
from os import system
from time import sleep
from guts.loader import Loader

Position = namedtuple('Position', ('x', 'y'))


class Octopus:
    DISPLAY_MAP = '🌕🌖🌗🌘🌑🌑🌑🌑🌑🌓'

    def __init__(self, value):
        self._value = value
        self._has_flashed = False

    def __repr__(self):
        return self.DISPLAY_MAP[self._value]

    def set_neighborhood(self, neighborhood):
        self._neighborhood = neighborhood

    def reset(self):
        self._has_flashed = False

    def flash(self):
        self._value = 0
        self._has_flashed = True
        yield 1

        for n in self._neighborhood:
            yield from n.step()

    def step(self):
        if self._has_flashed:
            return

        self._value += 1

        if self._value > 9:
            yield from self.flash()


class Grid(dict):
    OFFSET_MAP = [
        Position(x, y)
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        if (x, y) != (0, 0)
    ]

    def __init__(self, matrix):
        self.load(matrix)
        self.setup()
        self._counter = 0

    def __repr__(self):
        def display():
            y = 0
            for position, octopus in self.items():
                if position.y != y:
                    yield "\n"
                yield str(octopus)
                y = position.y

        return ''.join(
            display()
        )

    def __hash__(self):
        return hash(str(self))

    def load(self, matrix):
        # init grid
        [
            self.update(
                {
                    Position(x, y): Octopus(
                        int(value)
                    )
                }
            )
            for y, row in enumerate(matrix)
            for x, value in enumerate(row)
        ]

    def setup(self):
        for position, octopus in self.items():
            positions = [
                Position(
                    position.x + offset.x,
                    position.y + offset.y,
                )
                for offset in self.OFFSET_MAP
            ]

            neighborhood = [
                neighbor
                for neighbor in (
                    self.get(position)
                    for position in positions
                )
                if neighbor is not None
            ]

            octopus.set_neighborhood(neighborhood)

    def step(self):
        self._counter += 1

        for octopus in self.values():
            yield from octopus.step()

        for octopus in self.values():
            octopus.reset()


class Solver:
    def step(self, matrix):
        grid = Grid(matrix)
        grid.step()

        return str(grid).split()

    def part_a(self, path, steps):
        grid = Grid(Loader(path).read())

        for _ in range(steps):
            yield from grid.step()

    def part_b(self, path):
        lines = Loader(path).read()
        return self.simultaneous(lines)

    def simultaneous(self, lines):
        grid = Grid(lines)

        hashes = set()
        loop = 0

        def loop_detect():
            key = hash(grid)
            if key in hashes:
                return 1
            hashes.add(key)
            return 0

        while True:
            system('clear')

            r = sum(grid.step())
            print(grid)

            if r >= len(grid):
                return grid._counter

            loop += loop_detect()

            print(loop)
            if loop > 9:
                return 'infinite loop'

            sleep(1/60)


def test_process():
    solver = Solver()

    r = solver.part_a('day11_input_test.txt', 100)
    assert 1656 == sum(r)


if __name__ == '__main__':
    solver = Solver()

    def random_lines(w, h):
        from random import choice
        values = '0123456789'
        for _ in range(h):
            yield ''.join(
                [
                    choice(values)
                    for _ in range(w)
                ]
            )

    print(
        solver.simultaneous(random_lines(11, 11))
    )
