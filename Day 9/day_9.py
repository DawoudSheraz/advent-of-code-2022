
TEST_INPUT = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

TEST_INPUT_2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''


def diagonal(head_row, head_col, tail_row, tail_col):
    return abs(head_row - tail_row) == 1 and abs(tail_col - head_col) == 1


def determine_tail_coords(head_row, head_col, tail_row, tail_col):

    row_diff = head_row - tail_row
    col_diff = head_col - tail_col
    coords_diff = abs(row_diff) + abs(col_diff)
    if (coords_diff == 2 and diagonal(head_row, head_col, tail_row, tail_col)) or coords_diff <= 1:
        return tail_row, tail_col
    else:
        tx, ty = head_row, head_col  # this line gives me creeps now, I kept tail values here instead of head.
        if coords_diff >= 4:
            tx = head_row + 1 if row_diff < 0 else head_row - 1
            ty = head_col + 1 if col_diff < 0 else head_col - 1
        elif abs(col_diff) >= 2:
            ty = head_col + 1 if col_diff < 0 else head_col - 1
        elif abs(row_diff) >= 2:
            tx = head_row + 1 if row_diff < 0 else head_row - 1
        return tx, ty


def parse_knots(head_row, head_col, knots):

    updated_knots = [(head_row, head_col)]
    for count in range(len(knots) - 1):
        head_row, head_col = updated_knots[count][0], updated_knots[count][1]
        tail_row, tail_col = knots[count+1][0], knots[count+1][1]
        tail_x, tail_y = determine_tail_coords(head_row, head_col, tail_row, tail_col)
        updated_knots.append((tail_x, tail_y))

    return tail_x, tail_y, updated_knots


def traverse_grid(visited_grid, direction, steps, head_x, head_y, knots):
    if direction in ['U', 'D']:
        counter = head_x
        if direction == 'U':
            while counter > head_x - steps:
                counter -= 1
                tail_x, tail_y, knots = parse_knots(counter, head_y, knots)
                visited_grid.add((tail_x, tail_y))
        else:
            while counter < head_x + steps:
                counter += 1
                tail_x, tail_y, knots = parse_knots(counter, head_y, knots)
                visited_grid.add((tail_x, tail_y))
        return counter, head_y, knots
    else:
        counter = head_y
        if direction == 'R':
            while counter < head_y + steps:
                counter += 1
                tail_x, tail_y, knots = parse_knots(head_x, counter, knots)
                visited_grid.add((tail_x, tail_y))
        else:
            while counter > head_y - steps:
                counter -= 1
                tail_x, tail_y, knots = parse_knots(head_x, counter, knots)
                visited_grid.add((tail_x, tail_y))
        return head_x, counter, knots


def solve(data, knots_length=2):
    visited = set()
    head_x, head_y = 0, 0
    knots = [(0, 0) for _ in range(knots_length)]
    for action in data.splitlines():
        command = action.split(' ')
        head_x, head_y, knots = traverse_grid(visited, command[0], int(command[1]), head_x, head_y, knots)
    return len(visited)


with open('input.in') as f:
    data = f.read()
    # Part 1: 6357
    # Part 2: 2627
    print(f"Part 1: {solve(data, 2)}")
    print(f"Part 2: {solve(data, 10)}")
