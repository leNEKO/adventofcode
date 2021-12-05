from guts.loader import Loader


class Position:
    def __init__(self, number):
        self._number = number
        self._value = False

    def mark(self, number):
        if number == self._number:
            self._value = True

    @property
    def number(self):
        return self._number

    @property
    def value(self):
        return self._value


class Grid:
    def __init__(self):
        self._rows = []

    def add(self, line):
        self._rows.append(
            [
                Position(int(number))
                for number in line.split()
            ]
        )

    def mark(self, number):
        for row in self._rows:
            for position in row:
                position.mark(number)

    def check(self):
        for row in self.rows:
            if all(position.value for position in row):
                yield self, row
        for col in self.cols:
            if all(position.value for position in col):
                yield self, col
        return

    @property
    def remaining_numbers(self):
        return tuple(
            pos.number
            for row in self.rows
            for pos in row
            if pos.value is False
        )


    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return zip(*self._rows)

class Solver:
    def __init__(self, path):
        self._loader = Loader(path).read
        self._grids = []

    @staticmethod
    def head(line):
        return [
            int(number)
            for number in line.split(',')
        ]

    def read(self):
        loader = self._loader()
        self._draw = self.head(
            next(loader)
        )

        for line in loader:
            if line == '':
                grid = Grid()
                self._grids.append(grid)
            else:
                grid.add(line)

    def mark(self, number):
        for grid in self._grids:
            grid.mark(number)
            yield from grid.check()

    @property
    def result(self):
        self.read()

        for number in self._draw:
            for win_grid, win_line in self.mark(number):
                winning_numbers = tuple(
                    position.number
                    for position in win_line
                )

                return (
                    winning_numbers,
                    number,
                    sum(win_grid.remaining_numbers) * number
                )

def test_solve():
    winning_numbers, number, total = Solver('day4_input_test.txt').result

    assert (14, 21, 17, 24, 4) == winning_numbers
    assert 24 == number
    assert 4512 == total

if __name__ == '__main__':
    print(
        Solver('day4_input.txt').result
    )
