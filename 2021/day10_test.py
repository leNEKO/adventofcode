from enum import Enum
from guts.loader import Loader

class Symbols(Enum):
    PARENS = r'()'
    BRACKETS = r'[]'
    BRACES = r'{}'
    TAGS = r'<>'

ILLEGAL_SCORE = {
    Symbols.PARENS: 3,
    Symbols.BRACKETS: 57,
    Symbols.BRACES: 1197,
    Symbols.TAGS: 25137,
}

INCOMPLETE_SCORE = {
    Symbols.PARENS: 1,
    Symbols.BRACKETS: 2,
    Symbols.BRACES: 3,
    Symbols.TAGS: 4,
}


class Solver:
    @staticmethod
    def check_line(line):
        # init a list for recording open symbols
        stack = []

        def check_illegal(line):
            for char in line:
                for symbol in Symbols:
                    if char == symbol.value[0]:  # if match open symbol
                        stack.append(symbol)  # record the symbol
                    elif char == symbol.value[1]:  # if match close symbol
                        if stack.pop() != symbol:  # if close symbol not match last recorded
                            stack.clear()
                            return ILLEGAL_SCORE.get(symbol)
            return 0

        def check_incomplete():
            total = 0
            for symbol in stack[::-1]:
                total *= 5
                total += INCOMPLETE_SCORE.get(symbol, 0)
            return total

        return (
            check_illegal(line),
            check_incomplete()
        )

    def process(self, path):
        score_illegal = 0
        score_incomplete = []
        for line in Loader(path).read():
            a, b = self.check_line(line);
            score_illegal += a
            if b:
                score_incomplete.append(b)

        s = sorted(score_incomplete)

        return (score_illegal, s[len(s) // 2])


def test_is_paired():
    solver = Solver()
    assert 294 == solver.check_line('<{([{{}}[<[[[<>{}]]]>[]]')[1]
    assert 1480781 == solver.check_line('(((({<>}<{<{<>}{[]{[]{}')[1]
    assert ILLEGAL_SCORE.get(Symbols.BRACES) == solver.check_line('{([(<{}[<>[]}>{[]{[(<()>')[0]
    assert (26397, 288957) == solver.process('day10_input_test.txt')

if __name__ == '__main__':
    solver = Solver()
    print(
        solver.process('day10_input.txt')
    )