
TEST_INPUT = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''


def find_character_priority(char_value):
    if char_value.islower():
        return ord(char_value) - 96
    else:
        return ord(char_value) - 38


def get_priority_number_p1(data_str):
    data_length = len(data_str)
    data_p1 = data_str[:int(data_length/2)]
    data_p2 = data_str[(int(data_length/2)):]
    diff = list(set(data_p1).intersection(set(data_p2)))
    return find_character_priority(diff[0])


def get_priority_number_p2(str1, str2, str3):
    diff = list(set(str1).intersection(set(str2).intersection(set(str3))))
    return find_character_priority(diff[0])


def part_1(data):
    priority = 0
    for data_str in data.splitlines():
        priority += get_priority_number_p1(data_str)
    return priority


def part_2(data):
    priority = 0
    data = data.splitlines()
    for count in range(0, len(data), 3):
        data_set = data[count:count+3]
        priority += get_priority_number_p2(data_set[0], data_set[1], data_set[2])
    return priority


with open('input.in') as f:
    data = f.read()
    # Part 1: 7917
    # Part 2: 2585
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
