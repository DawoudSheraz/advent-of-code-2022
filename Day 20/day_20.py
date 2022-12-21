
TEST_INPUT = '''1
2
-3
3
-2
0
4'''


def solve(data, part=1, repeat=1):
    data = data.splitlines()
    data = list(enumerate(map(int, data)))  # Enumerate to create idx, value unique tuple because values repeat
    if part == 2:
        data = [(x[0], x[1] * 811589153) for x in data]
    data_length = len(data)
    movement_list = data.copy()
    for _ in range(repeat):
        for item in data:
            idx = movement_list.index(item)
            # -1 is needed here because we need to pop from list first and then add the value to new position
            # The addition to new position is being done on total-1 list.
            # I first did if-else to cater for edge cases and negative indices but
            # I didn't know what modulus already took care of negative indices
            # -2 % 8 = 6 and not -2 (sweating intensifies)
            next_idx = (idx + item[1]) % (data_length - 1)
            movement_list.insert(next_idx, movement_list.pop(idx))
    zero_index = [idx for idx, value in enumerate(movement_list) if value[1] == 0][0]

    return sum([movement_list[(zero_index + s) % data_length][1] for s in [1000, 2000, 3000]])


with open('input.in') as f:
    data = f.read()
    # Part 1:4914
    # Part 2:7973051839072
    print(f"Part 1:{solve(data)}")
    print(f"Part 2:{solve(data, 2, 10)}")
