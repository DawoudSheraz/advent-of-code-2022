
import re

TEST_INPUT = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''


def generate_stacks(data_values):
    total_stacks = int(re.findall('\\d+', data_values[-1])[-1])
    stacks = [[] for _ in range(total_stacks)]
    for value in range(len(data_values) - 1):
        for col in range(len(data_values[value])):
            # 1, 5, 9 and so on, indices where the values would be
            if (col - 1) % 4 == 0 and data_values[value][col] != ' ':
                stack_idx = int((col - 1) / 4)
                stacks[stack_idx].append(data_values[value][col])
    return stacks


def get_tops(stacks):
    output = ''
    for stack in stacks:
        output += stack[0]
    return output


def perform_move(stacks, move_command):
    command_values = list(map(int, re.findall('\\d+', move_command)))
    items_to_move, from_index, to_index = command_values[0], command_values[1] - 1, command_values[2] - 1
    moved = 0
    while moved < items_to_move:
        popped = stacks[from_index].pop(0)
        stacks[to_index].insert(0, popped)
        moved += 1


def perform_move_p2(stacks, move_command):
    command_values = list(map(int, re.findall('\\d+', move_command)))
    items_to_move, from_index, to_index = command_values[0], command_values[1] - 1, command_values[2] - 1
    moved = 0
    popped = []
    while moved < items_to_move:
        popped.append(stacks[from_index].pop(0))
        moved += 1
    for item in popped[::-1]:
        stacks[to_index].insert(0, item)


def part_1(data):
    stack_data, commands = data.split('\n\n')
    stacks = generate_stacks(stack_data.splitlines())
    for each in commands.splitlines():
        perform_move(stacks, each)
    return get_tops(stacks)


def part_2(data):
    stack_data, commands = data.split('\n\n')
    stacks = generate_stacks(stack_data.splitlines())
    for each in commands.splitlines():
        perform_move_p2(stacks, each)
    return get_tops(stacks)


with open('input.in') as f:
    data = f.read()
    # Part 1: ZRLJGSCTR
    # Part 2: PRTTGRFPB
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
