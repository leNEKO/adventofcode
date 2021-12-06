from typing import Dict, Iterator, List, Optional, Tuple
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
        self.__rows: List[List[Position]] = []
        self.__winning_line: Optional[List[Position]] = None
        self.__winning_number: Optional[int] = None

    def add(self, line: str):
        self.__rows.append(
            [
                Position(int(number))
                for number in line.split()
            ]
        )

    def check(self, number: int) -> Iterator['Grid']:
        for row in self.__rows:
            for position in row:
                position.mark(number)

        if self.__winning_line is None:
            for line in [*self.rows, *self.cols]:
                if all(position.value for position in line):
                    self.__winning_line = line
                    self.__winning_number = number

                    yield self

    @property
    def rows(self) -> List[Position]:
        return self.__rows

    @property
    def cols(self) -> List[Position]:
        return zip(*self.__rows)

    @property
    def report(self):
        return {
            'winning_number' : self.__winning_number,
            'winning_line': tuple(
                position.number
                for position in self.__winning_line
            ),
            'result': sum(self.remaining_numbers) * self.__winning_number
        }

    @property
    def remaining_numbers(self) -> Tuple[int]:
        return tuple(
            pos.number
            for row in self.rows
            for pos in row
            if pos.value is False
        )


class Solver:
    def __init__(self, path: str):
        self.__path: str = path
        self.__grids: List[Grid] = []

    def _load(self):
        def head(line: str) -> List[int]:
            return [
                int(number)
                for number in line.split(',')
            ]

        loader = Loader(self.__path).read()

        self.__draw = head(
            next(loader)
        )

        for line in loader:
            if line == '':
                grid = Grid()
                self.__grids.append(grid)
            else:
                grid.add(line)

    def _mark_position_in_grids(self, number):
        for grid in self.__grids:
            yield from grid.check(number)

    def _process(self):
        return [
            winner.report
            for number in self.__draw
            for winner in self._mark_position_in_grids(number)
        ]

    @property
    def result(self) -> Dict:
        self._load()
        winners = self._process()

        return {
            'first': winners[0],
            'last': winners[-1],
        }


def test_solver():
    report = Solver('day4_input_test.txt').result['first']

    assert (14, 21, 17, 24, 4) == report['winning_line']
    assert 24 == report['winning_number']
    assert 4512 == report['result']


if __name__ == '__main__':
    print(
        Solver('day4_input.txt').result
    )
