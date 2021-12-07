from enum import Enum, auto
from guts.loader import Loader


INPUT_PATH='day2.txt'


class Action(Enum):
    UP = 'up'
    DOWN = 'down'
    FORWARD = 'forward'

class Dim(Enum):
    HORIZ = auto()
    DEPTH = auto()
    AIM = auto()
class Solver:
    def __init__(self, path):
        self._loader = Loader(path)

    def main(self, method):
        coord = {
            Dim.HORIZ: 0,
            Dim.DEPTH: 0,
            Dim.AIM: 0,
        }

        for line in self._loader.read():
            command, value = line.split(' ')
            action = Action(command)
            value = int(value)
            method(coord, action, int(value))

        return coord[Dim.DEPTH] * coord[Dim.HORIZ]

    def part_one(self):
        def process(coord, action, value):
            def up(coord,value):
                coord[Dim.DEPTH] -= value
            def down(coord, value):
                coord[Dim.DEPTH] += value
            def forward(coord, value):
                coord[Dim.HORIZ] += value

            {
                Action.UP: up,
                Action.DOWN: down,
                Action.FORWARD: forward,
            }[action](coord, value)

        return self.main(process)

    def part_two(self):
        def process(coord, action, value):
            def up(coord,value):
                coord[Dim.AIM] -= value
            def down(coord, value):
                coord[Dim.AIM] += value
            def forward(coord, value):
                coord[Dim.HORIZ] += value
                coord[Dim.DEPTH] += value * coord[Dim.AIM]

            {
                Action.UP: up,
                Action.DOWN: down,
                Action.FORWARD: forward,
            }[action](coord, value)

        return self.main(process)

    @property
    def result(self):
        return (
            self.part_one(),
            self.part_two(),
        )

def test_solver_part_one():
    assert 150 == Solver('day2_test.txt').part_one()

def test_solver_part_two():
    assert 900 == Solver('day2_test.txt').part_two()

if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)