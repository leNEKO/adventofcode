from guts.loader import Loader


class Position:
    def __init__(self, number):
        self.__number = number
        self.__value = False

    def mark(self, number):
        if number == self.__number:
            self.__value = True

    @property
    def number(self):
        return self.__number

    @property
    def value(self):
        return self.__value


class Grid:
    def __init__(self):
        self.__rows = []
        self.__completed = False

    def add(self, line):
        self.__rows.append(
            [
                Position(int(number))
                for number in line.split()
            ]
        )

    def mark(self, number):
        for row in self.__rows:
            for position in row:
                position.mark(number)

    def check(self):
        if self.__completed == False:
            for row in self.rows:
                if all(position.value for position in row):
                    self.__completed = True

                    yield self, row
            for col in self.cols:
                if all(position.value for position in col):
                    self.__completed = True

                    yield self, col

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
        return self.__rows

    @property
    def cols(self):
        return zip(*self.__rows)


class Solver:
    def __init__(self, path):
        self.__loader = Loader(path).read()
        self.__grids = []
        self.__winners = []

    def read(self):
        def head(line):
            return [
                int(number)
                for number in line.split(',')
            ]

        self._draw = head(
            next(self.__loader)
        )

        for line in self.__loader:
            if line == '':
                grid = Grid()
                self.__grids.append(grid)
            else:
                grid.add(line)

    def process(self):
        def mark_position_in_grids(self, number):
            for grid in self._grids:
                grid.mark(number)

                yield from grid.check()

        for number in self._draw:
            for win_grid, win_line in mark_position_in_grids(self, number):
                winning_numbers = tuple(
                    position.number
                    for position in win_line
                )

                self.__winners.append(
                    (
                        winning_numbers,
                        number,
                        sum(win_grid.remaining_numbers) * number
                    )
                )

    @property
    def result(self):
        self.read()
        self.process()

        return {
            'first': self.__winners[0],
            'last': self.__winners[-1],
        }


def test_solver():
    winning_numbers, number, total = Solver(
        'day4_input_test.txt').result['first']

    assert (14, 21, 17, 24, 4) == winning_numbers
    assert 24 == number
    assert 4512 == total


if __name__ == '__main__':
    print(
        Solver('day4_input.txt').result
    )
