from functools import reduce
from guts.loader import Loader

INPUT_PATH='day1.txt'

class Solver:
    def __init__(self, path):
        self._loader = Loader(path)

    @property
    def result(self):
        # don't count first occurence
        count = -1
        previous = 0

        for value in self._loader.read():
            current = int(value)
            count += current > previous
            previous = current

        return count

def test_solver():
    assert Solver(INPUT_PATH).result == 1624

if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)
