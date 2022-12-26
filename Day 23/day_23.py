
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
    # I need to learn the performance differences of set and list
    # I had this as a list and it was so slower (taking 10+ seconds for part 1 alone). I turned this into set and both
    # parts ran within 5 seconds.
    elves = set()
    for row_idx, row in enumerate(data.splitlines()):
        for col_idx, col in enumerate(row):
            if col == '#':
                elves.add((col_idx + 1, row_idx + 1))
    return elves


def are_neighbors_available(elves, elf):
    for direction in DIRECTION_MAPS.values():
        if (elf[0] + direction[0], elf[1] + direction[1]) in elves:
            return False
    return True


def get_empty_tiles_count(elves):
    count = 0
    min_x, max_x = min(x[0] for x in elves), max(x[0] for x in elves)
    min_y, max_y = min(x[1] for x in elves), max(x[1] for x in elves)

    for r in range(min_y, max_y + 1):
        for c in range(min_x, max_x + 1):
            if (c, r) not in elves:
                count += 1
    return count


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
            elves.add(new_pos)
    return elves, old == elves


def solve(data):
    global DIR_SEQUENCE
    elves = get_elves_coords(data)
    for rd in range(1, 10000):
        elves, same = execute_round(elves)
        DIR_SEQUENCE = [*DIR_SEQUENCE[1:], DIR_SEQUENCE[0]]
        if same:
            yield rd
            break
        if rd == 10:
            yield get_empty_tiles_count(elves)


with open('input.in') as f:
    data = f.read()
    for idx, output in enumerate(solve(data), 1):
        # Part 1: 4138
        # Part 2: 1010
        print(f"Part {idx}: {output}")
