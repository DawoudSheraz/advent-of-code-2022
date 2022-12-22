
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
    return get_top(visited_grid) + 4


def get_top(visited_grid):
    return max([x[1] for x in visited_grid])


def solve(data, rocks=2022):
    visited_grid = set((x, 0) for x in range(7))  # by default, add floor
    rock_count = 0
    action_counter = -1
    sequence_checker = {}

    while rock_count < rocks:
        rock_id = rock_count % 5
        rock = get_rock(rock_id, get_next_y(visited_grid))
        while True:
            action_counter = (action_counter + 1) % len(data)
            action = data[action_counter]
            if rock_count > 2022:  # Using part 1 rock count as threshold/starting point for cycle sequence checks
                # Reddit for help again, Welp I am awful at this.
                # Key of active_rock and jet operation position is used as identifier
                # for cycle, the pair is bound to repeat.
                sequence_key = (rock_id, action_counter)
                if sequence_key in sequence_checker:
                    previous_rock_count, prev_top = sequence_checker[sequence_key]
                    rock_diff = rock_count - previous_rock_count
                    # Cycle does not begin from the start but rather sometime after the start.
                    # Modulus here is the main thing. Linking back to Day 11 Monkey worry problem,
                    # the modulus was used to reduce the worry level to bring it within range of division.
                    # The same applies here. If the modulus of total rocks with the rock diff is same
                    # as modulus of current rock with rock diff, that means the cycle will be repeating
                    # in intervals from current count till the total number of rocks. So there really isnt
                    # a need to simulate the remaining rocks. Just determine the cycle size and the remaining
                    # cycles and add the value to current height
                    # Again, reddit. Man I am bad at figuring out hidden items in AoC.
                    if rocks % rock_diff == rock_count % rock_diff:
                        cycles_left = (rocks - rock_count) // rock_diff
                        cycle_size = get_top(visited_grid) - prev_top
                        return get_top(visited_grid) + (cycles_left * cycle_size)
                else:
                    # Store the current rock count and the max height
                    sequence_checker[sequence_key] = (rock_count, get_top(visited_grid))

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

    return get_top(visited_grid)


with open('input.in') as f:
    data = f.read()
    # Part 1: 3092
    # Part 2: 1528323699442
    print(f"Part 1: {solve(data)}")
    print(f"Part 2: {solve(data, 1000000000000)}")
