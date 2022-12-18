
from functools import lru_cache

TEST_INPUT = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''


global p2_data


def get_pair_neighbors(x, y, z):
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def parse(input_data):
    return [tuple(map(int, x.split(','))) for x in input_data.splitlines()]


def in_bounds(pt, min_x, max_x, min_y, max_y, min_z, max_z):
    if (
        min_x <= pt[0] <= max_x and
        min_y <= pt[1] <= max_y and
        min_z <= pt[2] <= max_z
    ):
        return True
    return False


@lru_cache()
def exterior_reachable(pt, min_x, max_x, min_y, max_y, min_z, max_z):
    global p2_data
    queue = [pt]
    visited = set()

    while len(queue) > 0:
        point = queue.pop(0)
        if point in visited:
            continue
        if point in p2_data:
            continue
        visited.add(point)
        if not in_bounds(point, min_x, max_x, min_y, max_y, min_z, max_z):
            return True
        for neighbor in get_pair_neighbors(*point):
            if neighbor not in p2_data and neighbor not in visited:
                queue.append(neighbor)
    return False


def part_2(data):
    global p2_data
    p2_data = parse(data)
    x_list = [x[0] for x in p2_data]
    y_list = [x[1] for x in p2_data]
    z_list = [x[2] for x in p2_data]

    exterior = 0
    min_x, max_x = min(x_list), max(x_list)
    min_y, max_y = min(y_list), max(y_list)
    min_z, max_z = min(z_list), max(z_list)

    for cube in p2_data:
        for neighbor in get_pair_neighbors(*cube):
            if exterior_reachable(
                    neighbor, min_x, max_x, min_y, max_y, min_z, max_z
            ):
                exterior += 1

    return exterior


def part_1(data):
    overlap = 0
    data = parse(data)
    for pair in data:
        for neighbor in get_pair_neighbors(pair[0], pair[1], pair[2]):
            if neighbor in data:
                overlap += 1
    return (len(data) * 6) - overlap


with open('input.in') as f:
    data = f.read()
    # Part 1: 4244
    # Part 2: 2460
    # Part 2 took really really long time to run, even lru cache did not help much.
    # I will dig into refactoring this in a better, fast way.
    # Some options, iterate from min -> max and mark the points
    # Keep track of air and outside points and do not run loop if the current point is in either
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")

