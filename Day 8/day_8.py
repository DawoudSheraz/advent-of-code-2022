TEST_INPUT = '''30373
25512
65332
33549
35390'''


def create_data_list(data):
    return [list(map(int, x)) for x in data.splitlines()]


def is_visible(row, column, grid, max_row, max_column):

    data_value = grid[row][column]
    left = grid[row][max(column-1, 0)::-1]
    right = grid[row][min(column+1, max_column):]
    top, bottom = [], []
    counter = 0

    while counter < row:
        top.append(grid[counter][column])
        counter += 1

    counter += 1
    while counter < max_row:
        bottom.append(grid[counter][column])
        counter += 1

    return any(
        (len([x for x in left if x < data_value]) == len(left),
         len([x for x in right if x < data_value]) == len(right),
         len([x for x in top if x < data_value]) == len(top),
         len([x for x in bottom if x < data_value]) == len(bottom)
         )
    )


def get_score(value, data_list):
    for idx, val in enumerate(data_list):
        if val >= value:
            return idx + 1
    return len(data_list)


def get_tectonic_score(row, column, grid, max_row, max_column):
    data_value = grid[row][column]
    left = grid[row][max(column-1, 0)::-1]
    right = grid[row][min(column+1, max_column):]
    top, bottom = [], []
    counter = 0

    while counter < row:
        top.append(grid[counter][column])
        counter += 1
    top = top[::-1]

    counter += 1
    while counter < max_row:
        bottom.append(grid[counter][column])
        counter += 1

    left_score = get_score(data_value, left)
    right_score = get_score(data_value, right)
    top_score = get_score(data_value, top)
    bottom_score = get_score(data_value, bottom)
    return left_score * right_score * bottom_score * top_score


def get_visible_count(grid):
    rows = len(grid)
    columns = len(grid[0])
    visible = 2 * (rows + columns) - 4
    max_score = 0

    for row in range(1, rows - 1):
        for column in range(1, columns - 1):
            if is_visible(row, column, grid, rows, columns):
                visible += 1
            score = get_tectonic_score(row, column, grid, rows, columns)
            if score > max_score:
                max_score = score

    return visible, max_score


with open('input.in') as f:
    # Note: Refactor the above common code
    data = f.read()
    visible, max_score = get_visible_count(create_data_list(data))
    # Part 1: 1794
    # Part 2: 199272
    print(f"Part 1: {visible}")
    print(f"Part 2: {max_score}")
