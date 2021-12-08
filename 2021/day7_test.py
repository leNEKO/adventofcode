from guts.loader import Loader

class Solver:
    def __init__(self, input):
        self._input = input

    def part_one(self, destination):
        return sum(
            abs(origin - destination)
            for origin in self._input
        )

    def part_two(self, destination):
        return sum(
            value * (value+1) // 2
            for origin in self._input
            for value in [abs(origin - destination)]
        )


    def optimize(self, algo):
        positions = len(self._input)

        result = None
        for pos in range(0,positions):
            total = algo(pos)
            result = (
                total
                if result is None or result > total
                else result
            )

        return result

def test_process():
    solver = Solver([16,1,2,0,4,2,7,1,2,14])
    assert 37 == solver.optimize(solver.part_one)
    assert 41 == solver.part_one(1)
    assert 168 == solver.part_two(5)

if __name__ == '__main__':
    init = [
        int(value)
        for value in
        Loader('day7_input.txt').data[0].split(',')
    ]

    solver = Solver(init)
    print(
        solver.optimize(solver.part_one),
        solver.optimize(solver.part_two),
    )