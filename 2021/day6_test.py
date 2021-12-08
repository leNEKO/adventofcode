from collections import deque
from guts.loader import Loader

class Population():
    def __init__(self, data: list):
        self._counter = deque(
            0
            for _ in range(9)
        )
        for fish in data:
            self._counter[fish] += 1

    def iterate(self):
        generation = self._counter.popleft()
        self._counter[6] += generation
        self._counter.append(generation)

    @property
    def total(self):
        return sum(self._counter)

def process(days, init):
    population = Population(init)
    for _ in range(days):
        population.iterate()

    return population.total

def test_part_one():
    init = [3,4,3,1,2]
    assert 26 == process(18, init)

def test_part_two():
    init = [3,4,3,1,2]
    assert 26984457539 == process(256, init)

if __name__ == '__main__':
    init = [
        int(value)
        for value in Loader('day6_input.txt').data[0].split(',')
    ]

    print(
        process(80, init),
        process(256, init),
    )