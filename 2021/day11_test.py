from collections import namedtuple
from os import system
from time import sleep
from guts.loader import Loader

Position = namedtuple('Position', ('x', 'y'))


class Octopus:
    def __init__(self, value):
        self._value = value
        self._has_flashed = False

    def set_neighborhood(self, neighborhood):
        self._neighborhood = neighborhood

    def reset(self):
        self._has_flashed = False

    def flash(self):
        self._value = 0
        self._has_flashed = True # only once per step
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
    DISPLAY_MAP = '█▓▒░  ░▒▓█'
    OFFSET_MAP = [
        Position(x, y)
        for x in (-1, 0, 1)
        for y in (-1, 0, 1)
        if (x, y) != (0, 0)
    ]

    def __init__(self, matrix):
        self.load(matrix)
        self.setup_neighborhood()

        self._step = 0

    def __repr__(self):
        def display():
            y = 0
            for position, octopus in self.items():
                if position.y != y:
                    yield "\n"
                y = position.y

                # less flash
                diff = (self._step) % 10
                yield self.DISPLAY_MAP[octopus._value - diff] * 2

        return ''.join(
            display()
        )

    def __hash__(self):
        return hash(
            ''.join(
                str(octo._value)
                for octo in self.values()
            )
        )

    def load(self, matrix):
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

    def setup_neighborhood(self):
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
        self._step += 1

        for octopus in self.values():
            yield from octopus.step()

        for octopus in self.values():
            octopus.reset()


class Solver:
    def part_a(self, path, steps):
        grid = Grid(Loader(path).read())

        for _ in range(steps):
            yield from grid.step()

    def part_b(self, path, visual=True):
        lines = Loader(path).read()
        grid = Grid(lines)

        hashes = set()
        loop = 0

        def loop_detect():
            key = hash(grid)
            if key in hashes:
                return 1
            hashes.add(key)

            return 0

        def display(fps=60):
            system('clear')
            print(grid)
            sleep(1/fps)

        while True:

            r = sum(grid.step())

            if visual:
                display()

            if r >= len(grid):
                pass
                return grid._step

            loop += loop_detect()

            if loop > 9:
                pass
                return 'infinite loop'


def test_process():
    solver = Solver()

    r = solver.part_a('day11_input_test.txt', 100)
    assert 1656 == sum(r)


if __name__ == '__main__':
    solver = Solver()
    path = 'day11_input.txt'

    print(
        sum(solver.part_a(path, 100)),
        solver.part_b(path)
    )
