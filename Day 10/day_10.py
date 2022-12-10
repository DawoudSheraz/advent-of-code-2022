
TEST_INPUT = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''


def part_1(data):
    cycle = 1
    x_register = 1
    stop_point = 20
    score = 0

    for command in data.splitlines():
        counter = 1 if 'noop' in command else 2
        for count in range(counter):
            cycle += 1
            if count == 1:
                x_register += int(command.split(' ')[-1])
            if cycle == stop_point:
                score += (cycle * x_register)
                stop_point += 40

    return score


def part_2(data):
    crt = [['.'] * 40 for _ in range(6)]
    cycle = 0
    x_register = 1
    for command in data.splitlines():
        counter = 1 if 'noop' in command else 2
        for count in range(counter):
            cycle += 1
            if count == 1:
                x_register += int(command.split(' ')[-1])
            if x_register - 1 <= (cycle % 40) <= x_register + 1:
                crt[cycle // 40][cycle % 40] = '#'

    for each in crt:
        print(''.join(each))


with open('input.in') as f:
    data = f.read()
    # Part 1: 14560
    # Part 2: Rendered chars are EKRHEPUZ.
    # I made a fool here, interpreting U as V and wondering why my answer was wrong.
    print(f"Part 1: {part_1(data)}")
    part_2(data)
