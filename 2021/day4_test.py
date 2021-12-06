from typing import Dict, Iterator, List, Optional, Tuple
from guts.loader import Loader


class Position:
    def __init__(self, number):
        self._number = number
        self._value = False

    def mark(self):
        self._value = True

    @property
    def number(self):
        return self._number

    @property
    def value(self):
        return self._value


class Grid:
    def __init__(self):
        self._rows: List[List[Position]] = []
        self._winning_line: Optional[List[Position]] = None
        self._winning_number: Optional[int] = None

    def add_row(self, line: str):
        self._rows.append(
            [
                Position(int(number))
                for number in line.split()
            ]
        )

    def mark(self, number):
        for row in self._rows:
            for position in row:
                if position.number == number:
                    position.mark()

                    return position

    def check(self, number: int) -> Iterator['Grid']:
        self.mark(number)

        if self._winning_line is None:
            for line in [*self.rows, *self.cols]:
                if all(position.value for position in line):
                    self._winning_line = line
                    self._winning_number = number

                    yield self

    @property
    def rows(self) -> List[Position]:
        return self._rows

    @property
    def cols(self) -> List[Position]:
        return zip(*self._rows)

    def _remaining_numbers(self) -> Tuple[int]:
        return tuple(
            pos.number
            for row in self.rows
            for pos in row
            if pos.value is False
        )

    @property
    def expose(self):
        return {
            'winning_number': self._winning_number,
            'winning_line': tuple(
                position.number
                for position in self._winning_line
            ),
            'result': sum(self._remaining_numbers()) * self._winning_number
        }


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
                grid.add_row(line)

    def _process(self):
        return [
            winner.expose
            for number in self.__draw
            for grid in self.__grids
            for winner in grid.check(number)
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
