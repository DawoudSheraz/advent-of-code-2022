
TEST_INPUT = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''


def get_rock(rock_type, y):
    """
    Get the position of a new rock against a given y. x is hardcoded starting from 2
    because each rock is two units away from the left wall. Position is taken from bottom left.
    """
    if rock_type == 0:
        return [(2, y), (3, y), (4, y), (5, y)]
    elif rock_type == 1:
        return [(3, y), (2, y + 1), (3, y + 1), (4, y + 1), (3, y + 2)]
    elif rock_type == 2:
        return [(2, y), (3, y), (4, y), (4, y + 1), (4, y + 2)]
    elif rock_type == 3:
        return [(2, y), (2, y + 1), (2, y + 2), (2, y + 3)]
    elif rock_type == 4:
        return [(2, y), (3, y), (2, y + 1), (3, y + 1)]


def print_grid(visited_grid):
    """
    Helper function to print the current state of grid
    """
    output = []
    max_y = max([x[1] for x in visited_grid])
    for y in range(max_y + 1, -1, -1):
        out = ''
        for x in range(-1, 8):
            if x in [-1, 7]:
                out += '|'
                continue
            out += '#' if (x, y) in visited_grid else '.'
        output.append(out)
    print('\n'.join(output))


def can_move(dx, dy, rock, visited_grid):
    for pos in rock:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if (new_x, new_y) in visited_grid:
            return False
    return True


def move_rock(dx, dy, rock, visited_grid, register_visit):
    updated_rock = []
    for pos in rock:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if (new_x < 0) or (new_x >= 7):  # if out of bounds, keep the position as it is
            updated_rock = rock
            break
        updated_rock.append((new_x, new_y))

    if register_visit:
        for each in updated_rock:
            visited_grid.add(each)
    return updated_rock


def get_next_y(visited_grid):
    max_y = max([x[1] for x in visited_grid])
    return max_y + 4


def solve(data, height=2022):
    visited_grid = set((x, 0) for x in range(7))  # by default, add floor
    rock_count = 0
    action_counter = -1

    while rock_count < height:
        rock_id = rock_count % 5
        rock = get_rock(rock_id, get_next_y(visited_grid))
        while True:
            action_counter = (action_counter + 1) % len(data)
            action = data[action_counter]
            if action == '<':
                if can_move(-1, 0, rock, visited_grid):
                    rock = move_rock(-1, 0, rock, visited_grid, False)
            elif action == '>':
                if can_move(1, 0, rock, visited_grid):
                    rock = move_rock(1, 0, rock, visited_grid, False)
            if can_move(0, -1, rock, visited_grid):
                rock = move_rock(0, -1, rock, visited_grid, False)
            else:
                move_rock(0, 0, rock, visited_grid, True)
                break
        rock_count += 1

    return max([x[1] for x in visited_grid])


with open('input.in') as f:
    data = f.read()
    # solve(TEST_INPUT, 1000000000000)
    print(f"Part 1: {solve(data)}")