
from collections import deque

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


def bfs(blizzards, blizz_coords, max_x, max_y, start, end, mins):
    state = set()
    queue = deque([(*start, mins)])
    bliz_time = {}

    while len(queue) > 0:
        x, y, minutes = queue.popleft()

        if (x, y) == end:
            return minutes, blizzards, blizz_coords

        if (x <= 1 or x >= max_x or y <= 1 or y >= max_y) and ((x, y) != start):
            continue

        if (x, y, minutes, blizz_coords) in state:
            continue

        state.add((x, y, minutes, blizz_coords))

        if minutes + 1 not in bliz_time:
            bliz_time[minutes + 1] = update_blizzards(blizzards, max_x, max_y)
        blizzards, blizz_coords = bliz_time[minutes + 1]

        if (x, y) not in blizz_coords:
            queue.append((x, y, minutes + 1))
        if (x + 1, y) not in blizz_coords:
            queue.append((x + 1, y, minutes + 1))
        if (x - 1, y) not in blizz_coords:
            queue.append((x - 1, y, minutes + 1))
        if (x, y - 1) not in blizz_coords:
            queue.append((x, y - 1, minutes + 1))
        if (x, y + 1) not in blizz_coords:
            queue.append((x, y + 1, minutes + 1))


def solve(data):
    blizzards, blizz_coords, max_x, max_y = parse(data)
    p1, blizzards, blizz_coords = bfs(blizzards, blizz_coords, max_x, max_y, (2, 1), (max_x - 1, max_y), 0)
    # mins start from 1 to compensate 1-off error
    p2, blizzards, blizz_coords = bfs(blizzards, blizz_coords, max_x, max_y, (max_x - 1, max_y), (2, 1), 1)
    p3, blizzards, blizz_coords = bfs(blizzards, blizz_coords, max_x, max_y, (2, 1), (max_x - 1, max_y), 1)
    return p1, p1 + p2 + p3


with open('input.in') as f:
    data = f.read()
    part1, part2 = solve(data)
    # Part 1: 271
    # Part 2: 813
    # Still a bit slow, despite using state. takes around 2 mins.
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
