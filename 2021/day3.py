from typing import Counter
from guts.loader import Loader

INPUT_PATH='day3.txt'

class Solver:
    def __init__(self, path):
        self._loader = Loader(path)

    @property
    def result(self):
        input_matrix = [
            [c for c in line]
            for line in self._loader.read()
        ]

        most_commons_in_column = [
            Counter(col).most_common()
            for col in list(zip(*input_matrix)) # rotated
        ]

        def get_rate(key):
            return int(
                ''.join(
                    m[key][0]
                    for m in most_commons_in_column
                ),
                2
            )

        return get_rate(0) * get_rate(1)

if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)