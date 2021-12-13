from functools import reduce
from guts.loader import Loader


class Solver:
    def __init__(self, path):
        self._path = path

    def read(self):
        return [
            [
                int(point)
                for point in row
            ]
            for row in Loader(self._path).read()
        ]

    def process(self, matrix):
        def is_valid(x, y):
            x_valid = 0 <= x < len(matrix[0])
            y_valid = 0 <= y < len(matrix)

            return x_valid and y_valid

        def get_value(x, y):
            if is_valid(x, y):
                return int(matrix[y][x])
            return 9

        def is_lowest(x, y):
            neighboor_coord = (
                (x, y-1),
                (x, y+1),
                (x-1, y),
                (x+1, y),
            )

            neighboor_values = [
                get_value(x, y)
                for x, y in neighboor_coord
            ]

            return False == any(
                value <= get_value(x, y)
                for value in neighboor_values
            )

        return (
            int(value)
            for y, row in enumerate(matrix)
            for x, value in enumerate(row)
            if is_lowest(x, y)
        )

    @property
    def risk_level(self):
        return reduce(
            lambda total, value: total + value + 1,
            self.process(self.read()),
            0
        )


def test_solver():
    solver = Solver('day9_input_test.txt')
    assert [0,2,3,1,0] == list(
        solver.process(
            [
                '042',
                '436',
                '150',
            ]
        )
    )

    assert 15 == solver.risk_level
    assert [8, 7] == list(
        solver.process(
            [
                '899',
                '999',
                '789',
            ]
        )
    )

    assert [] == list(
        solver.process(
            [
                '99999',
                '90009',
                '90009',
                '99999',
            ]
        )
    )


if __name__ == '__main__':
    solver = Solver('day9_input.txt')

    print(
        solver.risk_level
    )
