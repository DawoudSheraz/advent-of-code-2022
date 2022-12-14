
from collections import OrderedDict

TEST_INPUT = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''


def can_move_down(x, y, grid_map, floor=None):
    y = y + 1
    if floor and y == floor:
        return 0, 0, False
    if (x, y) not in grid_map:
        return 0, 1, True
    elif (x - 1, y) not in grid_map:
        return -1, 1, True
    elif (x + 1, y) not in grid_map:
        return 1, 1, True
    return 0, 0, False


def get_change_factor(val_1, val_2):
    if val_1 > val_2:
        return -1
    if val_1 < val_2:
        return 1
    return 0


def get_coords(data_str):
    data = data_str.split(',')
    return int(data[0]), int(data[1])


def parse_input(data):
    data = data.splitlines()
    output = OrderedDict()

    for row in data:
        coords = row.split(' -> ')
        for count in range(len(coords) - 1):
            x1, y1 = get_coords(coords[count+1])
            x2, y2 = get_coords(coords[count])
            x_factor = get_change_factor(x1, x2)
            y_factor = get_change_factor(y1, y2)
            x = x1
            y = y1
            while x != (x2 + x_factor) or y != (y2 + y_factor):
                output[(x, y)] = '#'
                if x != (x2 + x_factor):
                    x = x + x_factor
                if y != (y2 + y_factor):
                    y = y + y_factor
    return output


def part_1(data):
    coords_map = parse_input(data)
    floor = max([x[1] for x in coords_map])
    sand = 0
    sx, sy = 500, 0
    while True:
        dx, dy, possible = can_move_down(sx, sy, coords_map)
        if possible:
            sy = sy + dy
            sx = sx + dx
        else:
            coords_map[(sx,sy)] = '.'
            sand += 1
            sx, sy = 500, 0
        if sy + 1 > floor:
            break
    return sand


def part_2(data):
    coords_map = parse_input(data)
    sand = 0
    sx, sy = 500, 0
    floor = max([x[1] for x in coords_map]) + 2
    while True:
        dx, dy, possible = can_move_down(sx, sy, coords_map, floor)
        if possible:
            sy = sy + dy
            sx = sx + dx
        else:
            coords_map[(sx, sy)] = '.'
            sand += 1
            sx, sy = 500, 0
        if (500, 0) in coords_map:
            break
    return sand


with open('input.in') as f:
    data = f.read()
    # Part 1: 979
    # Part 2: 29044
    # Note: To do some refactoring to merge 1 & 2
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
