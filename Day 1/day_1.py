
TEST_INPUT = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def solve(input_data):
    """
    simple create a summation list and store each sum there.
    Note to self: there will be Pythonic way to do this in 1-2 lines. Find that.
    """
    reduced_sums = []
    active_sum = 0
    for value in input_data.splitlines():
        if value == '':
            reduced_sums.append(active_sum)
            active_sum = 0
            continue
        active_sum += int(value)
    return sorted(reduced_sums, reverse=True)


with open('input.in') as f:
    data = f.read()
    summation_list = solve(data)
    # Part 1: 69177
    # Part 2: 207456
    print(f"Part 1: {summation_list[0]}")
    print(f"Part 2: {summation_list[0] + summation_list[1] + summation_list[2]}")
