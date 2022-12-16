
import re

TEST_INPUT = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''


def parse(data):
    sensors, beacons = [], []
    data = data.splitlines()
    for row in data:
        out = list(map(int, (re.findall('-?\\d+', row))))
        dist = abs(out[0] - out[2]) + abs(out[1] - out[3])
        sensors.append((out[0], out[1], dist))
        beacons.append((out[2], out[3]))
    return sensors, beacons


def get_impossible_ranges(sensors, y):
    ranges = []
    for sensor in sensors:
        diff = sensor[2] - abs(sensor[1] - y)
        if diff >= 0:
            ranges.append((sensor[0] - diff, sensor[0] + diff))
    return sorted(ranges, key=lambda x: x[0])


def reduce_by_union(ranges):
    if len(ranges) == 1:
        return ranges
    ranges = sorted(ranges, key=lambda x: x[0])
    output = []
    active = ranges[0]
    for count in range(1, len(ranges)):
        current = ranges[count]
        if current[0] > active[1]:  # If no overlap, add active to list and mark current as active
            output.append(active)
            active = current
        else:
            # I totally got it wrong. It is possible for more than one pair to overlap
            #  That's why update the active until the first non-overlap pair comes.
            # I was adding active to output on first overlap and moving to next pairs which
            # did not give the expected results.
            active = (min(active[0], current[0]), max(current[1], active[1]))
    output.append(active)
    return output


def part_1(data, height=10):
    sensors, beacons = parse(data)
    ranges = get_impossible_ranges(sensors, height)
    ranges = reduce_by_union(ranges)
    return sum([x[1] - x[0] for x in ranges])


def part_2(data, height=20):
    sensors, beacons = parse(data)
    max_y = 4000000
    for y in range(1, height + 1):
        ranges = get_impossible_ranges(sensors, y)
        ranges = reduce_by_union(ranges)
        if len(ranges) == 2:  # Get the first point between 2 ranges
            return ((ranges[0][1] + 1) * max_y) + y


with open('input.in') as f:
    data = f.read()
    #  Part 1: 4793062
    #  Part 2: 10826395253551
    print(f"Part 1: {part_1(data, 2000000)}")
    print(f"Part 2: {part_2(data, 4000000)}")

