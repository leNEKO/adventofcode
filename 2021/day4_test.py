from typing import Dict, List, Optional, Tuple
from guts.loader import Loader


class Position:
    def __init__(self, number: int):
        self._number: int = number
        self._value: bool = False

    def mark(self):
        self._value = True

        return self

    @property
    def number(self):
        return self._number

    @property
    def value(self):
        return self._value


class Line(list):
    def __init__(self, line: str):
        [
            self.append(
                Position(
                    int(number)
                )
            )
            for number in line.split()
        ]


class Grid:
    def __init__(self):
        self._rows: List[Line] = []
        self._winning_line: Optional[List[Position]] = None
        self._winning_number: Optional[int] = None

    def add(self, row: Line):
        self._rows.append(row)

    def check(self, number: int):
        self._mark(number)

        if self._winning_line is None:
            for line in [*self.rows, *self.cols]:
                if all(position.value for position in line):
                    self._winning_line = line
                    self._winning_number = number

                    yield self

    def _mark(self, number: int):
        for row in self._rows:
            for position in row:
                if position.number == number:
                    return position.mark()

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return zip(*self._rows)

    def _remaining_positions(self):
        return tuple(
            pos
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
            'result': sum(
                map(
                    lambda position: position.number,
                    self._remaining_positions()
                )
            ) * self._winning_number
        }


class Solver:
    def __init__(self, path: str):
        self._path: str = path
        self._grids: List[Grid] = []

    def _load(self):
        def head(line: str) -> List[int]:
            return [
                int(number)
                for number in line.split(',')
            ]

        loader = Loader(self._path).read()

        self.__turns = head(
            next(loader)
        )

        for line in loader:
            if line == '':
                grid = Grid()
                self._grids.append(grid)
            else:
                grid.add(
                    Line(line)
                )

    def _process(self):
        return [
            winner.expose
            for number in self.__turns
            for grid in self._grids
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
