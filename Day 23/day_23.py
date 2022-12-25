
from collections import defaultdict


TEST_INPUT = '''.....
..##.
..#..
.....
..##.
.....'''


TEST_2 = '''..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............'''

DIRECTION_MAPS = {
    'N': (0, -1),
    'S': (0, 1),
    'W': (-1, 0),
    'E': (1, 0),

    'NE': (1, -1),
    'NW': (-1, -1),
    'SE': (1, 1),
    'SW': (-1, 1),
}

DIR_SEQUENCE = [
    ('N', 'NE', 'NW'),
    ('S', 'SE', 'SW'),
    ('W', 'NW', 'SW'),
    ('E', 'NE', 'SE')
]


def get_elves_coords(data):
    elves = []
    for row_idx, row in enumerate(data.splitlines()):
        for col_idx, col in enumerate(row):
            if col == '#':
                elves.append((col_idx + 1, row_idx + 1))
    return elves


def are_neighbors_available(elves, elf):
    for direction in DIRECTION_MAPS.values():
        if (elf[0] + direction[0], elf[1] + direction[1]) in elves:
            return False
    return True


def next_move_coords(elves):
    next_elves = []
    for elf in elves:
        if are_neighbors_available(elves, elf):
            next_elves.append(elf)
            continue
        any_move = False
        for direction in DIR_SEQUENCE:
            possible = True
            for pos in direction:
                dx, dy = DIRECTION_MAPS[pos]
                if (elf[0] + dx, elf[1] + dy) in elves:
                    possible = False
                    break
            if possible:
                any_move = True
                dx, dy = DIRECTION_MAPS[direction[0]]
                next_elves.append((elf[0] + dx, elf[1] + dy))
                break
        if not any_move:
            next_elves.append(elf)
    return next_elves


def update_positions(current_elves, updated_elves):
    new_elves = [0] * len(current_elves)
    for idx, elf in enumerate(updated_elves):
        if elf in updated_elves[0: idx] + updated_elves[idx + 1:]:
            new_elves[idx] = current_elves[idx]
        else:
            new_elves[idx] = elf
    return new_elves


def execute_round(elves):
    old = elves.copy()
    updated_positions = defaultdict(list)

    for elf in elves:
        if are_neighbors_available(elves, elf):
            continue
        for direction in DIR_SEQUENCE:
            outcome = []
            for pos in direction:
                dx, dy = DIRECTION_MAPS[pos]
                outcome.append((elf[0] + dx, elf[1] + dy) not in elves)
            if all(outcome):
                dx, dy = DIRECTION_MAPS[direction[0]]
                updated_positions[(elf[0] + dx, elf[1] + dy)].append(elf)
                break
    for new_pos, elf in updated_positions.items():
        if len(elf) == 1:
            elves.remove(elf[0])
            elves.append(new_pos)
    return elves, old == elves


def solve(data):
    global DIR_SEQUENCE
    count = 0
    elves = get_elves_coords(data)
    for rd in range(1, 10):
        next_mv = next_move_coords(elves)
        if next_mv == elves:
            print(rd)
            break

        elves = update_positions(elves, next_mv)
        DIR_SEQUENCE = [*DIR_SEQUENCE[1:], DIR_SEQUENCE[0]]

        if rd == 10:
            min_x, max_x = min(x[0] for x in elves), max(x[0] for x in elves)
            min_y, max_y = min(x[1] for x in elves), max(x[1] for x in elves)

            for r in range(min_y, max_y + 1):
                for c in range(min_x, max_x + 1):
                    if (c, r) not in elves:
                        count += 1
            print(count)


def solve_v2(data):
    global DIR_SEQUENCE
    elves = get_elves_coords(data)
    for rd in range(1, 10000):
        print(rd)
        elves, same = execute_round(elves)
        DIR_SEQUENCE = [*DIR_SEQUENCE[1:], DIR_SEQUENCE[0]]
        if same:
            print(rd)
            break


with open('input.in') as f:
    data = f.read()
    # Part 1: 4138
    print(solve_v2(data))
