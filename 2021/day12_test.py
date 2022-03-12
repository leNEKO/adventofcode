class Node:
    def __init__(self, name):
        self.name = name
        self.links = []

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other._name

    def link(self, node):
        self.links.append(node)

    def is_big(self):
        return self.name.isupper()


class Register(dict):
    def update(self, name) -> Node:
        current = self.get(name)
        if current is None:
            super().update({name: Node(name)})

        return self.get(name)


class Solver:
    def __init__(self, lines):
        self._register = Register()
        for line in lines:
            names = line.split('-')

            nodes = [
                self._register.update(name)
                for name in names
            ]

            a, b = nodes
            a.link(b)

            if a.is_big():
                b.link(a)

    def process(self):
        def traverse(current_node: Node, end_node: Node, visited=None):
            if visited is None:
                visited = []
            visited.append(current_node.name)
            for next_node in current_node.links:
                if next_node.name in visited and next_node.is_big() is False:
                    continue
                if next_node is end_node:
                    visited = []
                    print(', '.join(visited))
                    yield 1
                yield from traverse(next_node, end_node, visited)

        r = sum(
            traverse(
                self._register.get('start'),
                self._register.get('end')
            )
        )

        return r


def test_process():
    data = (
        'start-A',
        'start-b',
        'A-c',
        'A-b',
        'b-d',
        'A-end',
        'b-end',
    )

    solver = Solver(data)
    assert 3 == solver.process()


if __name__ == '__main__':
    r = test_process()
