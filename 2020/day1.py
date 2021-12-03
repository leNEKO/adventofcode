from functools import reduce

# Load data
with open('day1.input') as file:
    MASSES = [int(s) for s in file.read().splitlines()]


def fuel(masse):
    return masse // 3 - 2


def recursive_fuel(masse, total=0):
    f = fuel(masse)

    if f > 0:
        total += f

        return recursive_fuel(f, total)

    return total


def needed_fuel(masses):
    return sum(fuel(i) for i in masses)


def really_needed_fuel(masses):
    return sum(recursive_fuel(i) for i in masses)


if __name__ == '__main__':
    # day 2 tests
    assert (966 == recursive_fuel(1969))
    assert (50346 == recursive_fuel(100756))

    responses = {
        'needed fuel': needed_fuel(MASSES),
        'needed fuel, fuel included': really_needed_fuel(MASSES),
    }

    print(responses)
