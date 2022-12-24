import math

from sympy.solvers import solve as sympy_solve

TEST_INPUT = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''


def parse(data):
    data = data.splitlines()
    out = {}
    for row in data:
        row = row.split(':')
        out[row[0]] = row[1].strip()
    return out


def solve(data_dict, number_dict, monkey):
    monkey_number = data_dict[monkey]
    if monkey_number.isnumeric():
        number_dict[monkey] = int(monkey_number)
    else:
        monkey_number = monkey_number.split(' ')
        val_1 = number_dict.get(monkey_number[0], solve(data_dict, number_dict, monkey_number[0]))
        val_2 = number_dict.get(monkey_number[2], solve(data_dict, number_dict, monkey_number[2]))
        ops = monkey_number[1]
        number_dict[monkey] = int(eval(f"{val_1} {ops} {val_2}"))
    return number_dict[monkey]


def solve_p2(data_dict, number_dict, monkey):
    if monkey == 'humn':
        return 'x'
    monkey_number = data_dict[monkey]
    if monkey_number.isnumeric():
        number_dict[monkey] = int(monkey_number)
    else:
        monkey_number = monkey_number.split(' ')
        val_1 = number_dict.get(monkey_number[0], solve_p2(data_dict, number_dict, monkey_number[0]))
        val_2 = number_dict.get(monkey_number[2], solve_p2(data_dict, number_dict, monkey_number[2]))
        ops = monkey_number[1] if monkey != 'root' else '-'
        op = f"({val_1}) {ops} ({val_2})"
        number_dict[monkey] = eval(op) if 'x' not in op else op
    return number_dict[monkey]


def part_1(data):
    data_dict = parse(data)
    number_dict = {}
    solve(data_dict, number_dict, 'root')
    return number_dict['root']


def part_2(data):
    data_dict = parse(data)
    data_dict['humn'] = 'x'
    number_dict = {}
    # Sympy did the equation solving here. The branch of the tree/monkeys where humn is present
    # is left untouched and accumulated as an algebraic equation.
    # Reddit suggests using Binary search too. The approach is to solve one branch that does not have humn.
    # Take the value as target. Then do a binary search from 0-max value, setting the value to humn to that value.
    # I will try to implement this out, hopefully.
    solve_p2(data_dict, number_dict, 'root')
    out = sympy_solve(number_dict['root'])
    return math.ceil(out[0])


with open('input.in') as f:
    data = f.read()
    # Part 1: 194058098264286
    # Part 2: 3592056845086
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
