
TEST_INPUT = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''


def get_list(pair):
    pair = list(map(int, pair.split('-')))
    return [i for i in range(pair[0], pair[1]+1)]


def is_overlapping(pair1, pair2):
    pair1 = get_list(pair1)
    pair2 = get_list(pair2)
    return list(set(pair1).intersection(pair2)), pair1, pair2


def part_1(data):
    overlap_count = 0
    for row in data.splitlines():
        pair1, pair2 = row.split(',')
        overlapping, pair1, pair2 = is_overlapping(pair1, pair2)
        # length check of data list is needed to check fully-contained condition
        if overlapping and ((len(overlapping) == len(pair1)) or (len(overlapping) == len(pair2))):
            overlap_count += 1
    return overlap_count


def part_2(data):
    overlap_count = 0
    for row in data.splitlines():
        pair1, pair2 = row.split(',')
        overlapping, pair1, pair2 = is_overlapping(pair1, pair2)
        if overlapping:
            overlap_count += 1
    return overlap_count


with open('input.in') as f:
    data = f.read()
    # Part 1: 651
    # Part 2: 956
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
