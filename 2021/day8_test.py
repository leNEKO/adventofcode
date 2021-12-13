import re
from guts.loader import Loader

DIGIT_MAP = {
    k: frozenset(v)
    for k, v in {
        0: 'abcefg',
        1: 'cf',
        2: 'acdef',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg',
    }.items()
}
class Solver:
    PATTERN = re.compile(
        r'\b(\w+)\b'
    )
    def __init__(self, path):
        self._path = path

    def process(self):
        count = 0;
        for line in Loader(self._path).read():
            left, right = self.decode(line)
            mapping = self.mapping([*left, *right])
            for value in right:
                if len(value) in (2,3,4,7):
                    count += 1
        return count

    def decode(self, line):
        decoded = [
            self.normalize(
                self.PATTERN.findall(part)
            )
            for part in line.split('|')
        ]
        return decoded

    @staticmethod
    def normalize(words):
        return [
            frozenset(word)
            for word in words
        ]

    @staticmethod
    def mapping(words):
        word_map = {}
        letter_map = {}
        len_map = {
            2: 1,
            4: 4,
            3: 7,
            7: 8,
        }
        wordset = set(words)
        for word in wordset:
            size = len(word)
            value = len_map.get(size)
            if value is not None:
                word_map[value] = word

        [
            wordset.remove(word)
            for word in word_map.values()
        ]

        letter_map['a'] = ''.join(word_map[7] - word_map[1])

        pass





def test_process():
    solver = Solver('day8_input_test.txt')
    assert 26 == solver.process()


if __name__ == '__main__':
    print(
        Solver('day8_input.txt').process()
    )