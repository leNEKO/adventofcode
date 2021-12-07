from collections import deque
from functools import reduce
from guts.loader import Loader

INPUT_PATH = 'day1.txt'


class IntDeQueue(deque):
    def __init__(self, size: int = 1):
        self._size = size

    def append(self, num: int):
        if len(self) >= self._size:
            self.popleft()
        return super().append(num)

    def sum(self):
        if self.__len__() == self._size:
            return sum(self)


class Solver:
    def __init__(self, path):
        self._loader = Loader(path)

    def read(self):
        for num in self._loader.read():
            yield int(num)

    def process(self, window: int = 1):
        q = IntDeQueue(window)

        # don't count first occurence
        count = 0
        previous = 0

        for value in self.read():
            current = q.sum()
            q.append(value)
            if current is not None:
                count += current > previous
                previous = current

        return count

    @property
    def result(self):
        return (
            self.process(1),
            self.process(3),
        )


def test_solver_simple():
    assert Solver('day1_test.txt').process(1) == 7


def test_solver_window():
    assert Solver('day1_test.txt').process(3) == 5


if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)
