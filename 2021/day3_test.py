from typing import Counter
from guts.loader import Loader

INPUT_PATH='day3.txt'

class Solver:
    def __init__(self, path):
        self._matrix = [
            [c for c in line]
            for line in Loader(path).read()
        ]

    def most_commons_in_column(self, matrix):
        return [
            Counter(column).most_common()
            for column in list(zip(*matrix)) # rotated
        ]

    @property
    def power_comsuption(self):
        def get_rate(key):
            return int(
                ''.join(
                    m[key][0]
                    for m in self.most_commons_in_column(self._matrix)
                ),
                2
            )

        return get_rate(0) * get_rate(-1)

    @property
    def life_support_rating(self):
        def get_rate(key, final):
            matrix = self._matrix.copy()
            for k in range(0, len(self._matrix[0])):
                commons = self.most_commons_in_column(matrix)
                matrix = [
                    line
                    for line in matrix
                    if line[k] == commons[k][key][0]
                ]

                if len(matrix) == 2:
                    for m in matrix:
                        if m[-1] == final:
                            return int(''.join(m), 2)

        o2 = get_rate(0, '1')
        co2 = get_rate(-1, '0')
        return {
            'oxygen generator': o2,
            'CO2 scrubber': co2,
            'total': o2 * co2,
        }

    @property
    def result(self):
        return {
            'power comsuption': self.power_comsuption,
            'life support rating': self.life_support_rating,
        }

def test_life_support_rating():
    expected = {
        'power comsuption': 198,
        'life support rating': {
            'oxygen generator': 23,
            'CO2 scrubber': 10,
            'total': 230,
        },
    }
    actual = Solver('day3_test.txt').result;

    assert expected == actual

if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)