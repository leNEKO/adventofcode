from guts.loader import Loader

INPUT_PATH='day2.txt'

class Solver:
    def __init__(self, path):
        self._loader = Loader(path)

    @property
    def result(self):
        action = {
            'up': 0,
            'down': 0,
            'forward': 0,
        }

        for line in self._loader.read():
            command, value = line.split(' ')
            action[command] += int(value)

        return (
            (action['down'] - action['up'])
            * action['forward']
        )

if __name__ == '__main__':
    result = Solver(INPUT_PATH).result
    print(result)