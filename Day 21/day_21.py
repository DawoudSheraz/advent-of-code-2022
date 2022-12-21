

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
    monkey_number = data_dict[monkey]
    if monkey_number.isnumeric():
        number_dict[monkey] = int(monkey_number)
    else:
        monkey_number = monkey_number.split(' ')
        val_1 = number_dict.get(monkey_number[0], solve_p2(data_dict, number_dict, monkey_number[0]))
        val_2 = number_dict.get(monkey_number[2], solve_p2(data_dict, number_dict, monkey_number[2]))
        ops = monkey_number[1] if monkey != 'root' else '-'
        op = f"{val_1} {ops} {val_2}"
        number_dict[monkey] = eval(op)
    return number_dict[monkey]


def part_1(data):
    data_dict = parse(data)
    number_dict = {}
    solve(data_dict, number_dict, 'root')
    return number_dict['root']


def part_2(data):
    data_dict = parse(data)
    data_dict['humn'] = '0'
    number_dict = {}
    solve_p2(data_dict, number_dict, 'root')
    out = number_dict['root']
    return out


with open('input.in') as f:
    data = f.read()
    print(f"Part 1: {part_1(data)}")
