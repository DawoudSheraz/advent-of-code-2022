
import json
from functools import cmp_to_key
from itertools import zip_longest

TEST_INPUT = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''


def in_correct_order(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return 0 if p1 == p2 else (-1 if p1 > p2 else 1)
    elif isinstance(p1, list) and isinstance(p2, int):
        return in_correct_order(p1, [p2])
    elif isinstance(p1, int) and isinstance(p2, list):
        return in_correct_order([p1], p2)
    elif isinstance(p1, list) and isinstance(p2, list):
        for pp1, pp2 in zip_longest(p1, p2):
            if pp1 is None:
                return 1
            if pp2 is None:
                return -1
            out = in_correct_order(pp1, pp2)
            if out in [-1, 1]:
                return out
    return 0


def get_packets(data):
    data = data.split('\n\n')
    output = []
    for data_row in data:
        data_row = data_row.split('\n')
        p1 = json.loads(data_row[0])
        p2 = json.loads(data_row[1])
        output.append((p1, p2))
    return output


def get_packets_p2(data):
    output = []
    for data_row in data.splitlines():
        if data_row == '':
            continue
        output.append(json.loads(data_row))
    return output


def part_1(data):
    packets = get_packets(data)
    idx_count = 0
    for idx, packet_pair in enumerate(packets):
        output = in_correct_order(packet_pair[0], packet_pair[1])
        if output == 1:
            idx_count += idx + 1
    return idx_count


def part_2(data):
    packets = get_packets_p2(data)
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=cmp_to_key(in_correct_order), reverse=True)

    product = 1
    for idx, packet in enumerate(packets):
        if packet == [[2]] or packet == [[6]]:
            product *= (idx + 1)
    return product


with open('input.in') as f:
    data = f.read()
    # Part 1: 5529
    # Part 2: 27690
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
