
TEST_INPUT = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''


GRID_DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1)
}


def get_data_grid(data):
    output = []
    for row in data.splitlines():
        output.append([ord(x) if (x != 'E' and x != 'S') else (ord('a') if x == 'S' else ord('z')) for x in row])
    return output


def bfs(grid, start_row, start_col, rows, cols, end):
    visited = set()
    steps = 0
    queue = [(start_row, start_col, steps)]
    while len(queue) > 0:
        x, y, steps = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        current = grid[x][y]
        if (x, y) == end:
            return steps

        for _, coords in GRID_DIRECTIONS.items():
            dx, dy = coords[0], coords[1]
            rowx = x + dx
            coly = y + dy
            if rowx in [-1, rows] or coly in [cols, -1]:
                continue
            grid_val = grid[rowx][coly]
            if grid_val - current <= 1:
                queue.append((rowx, coly, steps+1))


def solve(data, part=1):
    grid = get_data_grid(data)
    rows, cols = len(grid), len(grid[0])
    endx, endy = 0, 0
    start_pos = []
    distances = []
    pos_checks = ['S'] if part == 1 else ['S', 'a']
    for row in range(rows):
        for col in range(cols):
            if data.splitlines()[row][col] in pos_checks:
                start_pos.append((row, col))
            if data.splitlines()[row][col] == 'E':
                endx, endy = row, col
    for starts in start_pos:
        output = bfs(grid, starts[0], starts[1], rows, cols, (endx, endy))
        distances.append(output if output else None)
    distances = [x for x in distances if x is not None]
    return min(distances)


with open('input.in') as f:
    data = f.read()
    # Part 1: 528
    # Part 2: 522 -- execution is slower as I am just brute forcing all possible paths.
    # Maybe A* or Dijkstra can give better output here.
    print(f"Part 1: {solve(data)}")
    print(f"Part 2: {solve(data, part=2)}")
