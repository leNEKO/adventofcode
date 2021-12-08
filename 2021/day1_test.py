from collections import deque
from guts.loader import Loader
from pytest import mark

class IntDeque(deque):
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
        q = IntDeque(window)

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

dataprovider = [
    (7,1),
    (5,3),
]
@mark.parametrize('expected, window', dataprovider)
def test_solver(expected, window):
    assert Solver('day1_input_test.txt').process(window) == expected


if __name__ == '__main__':
    result = Solver('day1_input.txt').result
    print(result)
