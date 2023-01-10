
TEST_INPUT = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''


GRID_DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0)
}

NEW_DIRECTION = {
    'U': {'L': 'L', 'R': 'R'},
    'D': {'L': 'R', 'R': 'L'},
    'L': {'L': 'D', 'R': 'U'},
    'R': {'L': 'U', 'R': 'D'},
}

DIR_VALUES = {
    'R': 0,
    'D': 1,
    'L': 2,
    'U': 3
}


def parse_grid(input_map):
    input_map = input_map.splitlines()
    walls = set()
    open_spaces = set()
    complete_map = set()
    for y_idx, row in enumerate(input_map, 1):
        for x_idx, value in enumerate(row, 1):
            if value == '.':
                open_spaces.add((x_idx, y_idx))
                complete_map.add((x_idx, y_idx))
            if value == '#':
                walls.add((x_idx, y_idx))
                complete_map.add((x_idx, y_idx))
    return open_spaces, walls, complete_map


def get_start(complete_map):
    return min([value[0] for value in complete_map if value[1] == 1]), 1


def get_wrap_coordinates(x, y, direction, complete_map):
    new_x, new_y = x, y
    if direction == 'L':
        new_x = max([value[0] for value in complete_map if value[1] == new_y])
    elif direction == 'R':
        new_x = min([value[0] for value in complete_map if value[1] == new_y])
    elif direction == 'U':
        new_y = max([value[1] for value in complete_map if value[0] == new_x])
    elif direction == 'D':
        new_y = min([value[1] for value in complete_map if value[0] == new_x])
    return new_x, new_y


def make_move(x, y, direction, walls, spaces, total_map):
    dx, dy = GRID_DIRECTIONS[direction]
    nx, ny = x + dx, y + dy

    if (nx, ny) in spaces:  # No need to move further
        return nx, ny, True
    elif (nx, ny) in walls:
        return x, y, False
    else:
        nx, ny = get_wrap_coordinates(x, y, direction, total_map)
        if (nx, ny) in spaces:
            return nx, ny, True
        elif (nx, ny) in walls:
            return x, y, False


def part_1(data):
    data = data.split('\n\n')
    open_spaces, walls, complete_map = parse_grid(data[0])
    x, y = get_start(complete_map)
    direction = 'R'
    numb = ''
    for character in data[1]:
        if character.isdigit():
            numb += character
        elif character.isalpha():
            value = int(numb)
            numb = ''
            for _ in range(value):
                x, y, moved = make_move(x, y, direction, walls, open_spaces, complete_map)
                if not moved:
                    break
            direction = NEW_DIRECTION[direction][character]

    if numb != '':
        value = int(numb)
        for _ in range(value):
            x, y, moved = make_move(x, y, direction, walls, open_spaces, complete_map)
            if not moved:
                break

    return (x * 4) + (1000 * y) + (DIR_VALUES[direction])


with open('input.in') as f:
    data = f.read()
    # Part 1: 75388
    print(part_1(data))
