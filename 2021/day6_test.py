from collections import deque
from guts.loader import Loader
from pytest import mark

class Population(deque):
    def __init__(self, data: list):
        super().__init__(
            0 for _ in range(9)
        )
        for value in data:
            self[value] += 1

    def iterate(self):
        generation = self.popleft()
        self[6] += generation
        self.append(generation)

    @property
    def total(self):
        return sum(self)

def process(days, init):
    population = Population(init)
    for _ in range(days):
        population.iterate()

    return population.total

init = [3,4,3,1,2]
dataprovider = [
    (init, 18, 26),
    (init, 256, 26_984_457_539),
]

@mark.parametrize('init, days, fishes', dataprovider)
def test_process(init, days, fishes):
    assert fishes == process(days, init)

if __name__ == '__main__':
    init = [
        int(value)
        for value in Loader('day6_input.txt').data[0].split(',')
    ]

    print(
        process(80, init),
        process(256, init),
    )