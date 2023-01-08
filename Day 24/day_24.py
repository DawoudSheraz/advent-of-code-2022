
TEST_INPUT = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''


GRID_DIRECTIONS = {
    '^': (0, -1),
    'v': (0, 1),
    '>': (1, 0),
    '<': (-1, 0)
}


def update_blizzards(blizzards, max_x, max_y):
    blizzards_with_direction = frozenset()
    blizzard_coords = frozenset()
    for blizzard in blizzards:
        bx, by, bdir = blizzard
        dx, dy = GRID_DIRECTIONS[bdir]
        bnx, bny = bx + dx, by + dy

        if bdir == '^' and bny <= 1:
            bny = max_y - 1
        elif bdir == 'v' and bny >= max_y:
            bny = 2
        elif bdir == '<' and bnx <= 1:
            bnx = max_x - 1
        elif bdir == '>' and bnx >= max_x:
            bnx = 2
        blizzards_with_direction = blizzards_with_direction | {(bnx, bny, bdir)}
        blizzard_coords = blizzard_coords | {(bnx, bny)}
    return blizzards_with_direction, blizzard_coords


def parse(data):
    data = data.splitlines()
    output = frozenset()
    blizz_coords = frozenset()

    for y_idx, row in enumerate(data, 1):
        for x_idx, value in enumerate(row, 1):
            if value in ['v', '^', '<', '>']:
                output = output | {(x_idx, y_idx, value)}
                blizz_coords = blizz_coords | {(x_idx, y_idx)}
    return output, blizz_coords, len(data[0]), len(data)


def print_blizzard(blizzard, max_x, max_y):
    for y in range(2, max_y):
        output = ''
        for x in range(2, max_x):
            dir_found = False
            for dir in ['>', '<', '^', 'v']:
                if (x, y, dir) in blizzard:
                    output += dir
                    dir_found = True
                    break
            if not dir_found:
                output += '.'
        print(output)


def solve(blizzards, blizz_coords, max_x, max_y, start, end):
    state = set()
    queue = [(*start, 0, 0, 0)]
    bliz_time = {}
    p1 = 10000000
    p2 = 1000000

    while len(queue) > 0:
        x, y, minutes, start_visitation, end_visitation = queue.pop(0)

        if (x, y) == end:
            if end_visitation == 0 and start_visitation == 0:
                end_visitation = 1
                p1 = min(p1, minutes)
                print(p1)
            if end_visitation == 1 and start_visitation == 1:
                print("v2", minutes)
                return

        if (x, y) == start and end_visitation == 1 and start_visitation == 0:
            start_visitation = 1

        # this needs fixups to get correct results for p2
        if (x <= 1 or x >= max_x or y <= 1 or y >= max_y) and ((x, y) != start):
            continue

        if (x, y, minutes, start_visitation, end_visitation) in state:
            continue

        state.add((x, y, minutes, start_visitation, end_visitation))

        if minutes + 1 not in bliz_time:
            bliz_time[minutes + 1] = update_blizzards(blizzards, max_x, max_y)

        blizzards, blizz_coords = bliz_time[minutes + 1]

        if (x, y) not in blizz_coords:
            queue.append((x, y, minutes + 1, start_visitation, end_visitation))
        if (x + 1, y) not in blizz_coords:
            queue.append((x + 1, y, minutes + 1, start_visitation, end_visitation))
        if (x - 1, y) not in blizz_coords:
            queue.append((x - 1, y, minutes + 1, start_visitation, end_visitation))
        if (x, y - 1) not in blizz_coords:
            queue.append((x, y - 1, minutes + 1, start_visitation, end_visitation))
        if (x, y + 1) not in blizz_coords:
            queue.append((x, y + 1, minutes + 1, start_visitation, end_visitation))


def part_1(data):
    blizzards, bliz_coords, max_x, max_y = parse(data)
    output = solve(blizzards, bliz_coords, max_x, max_y, (2, 1), (max_x-1, max_y))
    print(output)


part_1(TEST_INPUT)
# Part 1: 271
# with open('input.in') as f:
#     data = f.read()
#     part_1(data)
