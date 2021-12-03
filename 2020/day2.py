import os
import time


def intcode(code):
    data = [int(i) for i in code.split(',')]
    k = 0

    # init
    data[1] = 12
    data[2] = 2

    while k < len(data):
        # print(data)
        # time.sleep(0.1)
        # os.system('clear')

        if data[k] == 99:  # stop opcode
            return data[0]  # finish

        # opcodes
        data[data[k+3]] = {
            1: lambda k: data[data[k+1]] + data[data[k+2]],
            2: lambda k: data[data[k+1]] * data[data[k+2]],
        }[data[k]](k)

        # next block
        k += 4


if __name__ == "__main__":
    with open('day2.input') as file:
        code = file.read()
    print(intcode(code))
