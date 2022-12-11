
import re
from collections import defaultdict

TEST_INPUT = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''


class Monkey:

    def __init__(self, items, worry_ops, division_check, monkey_index_true, monkey_index_false, worry_check=True):

        self.items = list(map(int, items))
        self.division_check = int(division_check)
        self.monkey_index_true = int(monkey_index_true)
        self.monkey_index_false = int(monkey_index_false)
        self.worry_ops = worry_ops
        self.worry_check = worry_check

    def __str__(self):
        return ','.join(map(str,self.items))

    def add_item(self, item):
        self.items.append(item)

    def get_updated_worry(self, item):
        if self.worry_ops == 'old * old':
            return item * item
        _, ops, value = self.worry_ops.split(' ')
        value = int(value)
        if ops == '+':
            return item + value
        elif ops == '*':
            return item * value

    def determine_monkey_throw_index(self):
        for item in self.items:
            new_worry = self.get_updated_worry(item)
            new_worry = new_worry // 3 if self.worry_check else new_worry
            if new_worry % self.division_check == 0:
                yield new_worry, self.monkey_index_true
            else:
                yield new_worry, self.monkey_index_false
        self.items = []


def create_monkey_list(data, worry_check=True):
    monkey_list = []
    data = data.splitlines()

    for count in range(0, len(data), 7):
        items = re.findall('\\d+', data[count+1])
        ops = data[count+2].split(' = ')[-1]
        division = re.findall('\\d+', data[count+3])[0]
        truth = re.findall('\\d+', data[count + 4])[0]
        false = re.findall('\\d+', data[count + 5])[0]
        monkey = Monkey(items, ops, division, truth, false, worry_check)
        monkey_list.append(monkey)
    return monkey_list


def part_1(data, rounds=20, worry_check=True):
    monkey_inspect_count = defaultdict(int)
    monkey_list = create_monkey_list(data, worry_check)

    for rd in range(rounds):
        for idx, monkey in enumerate(monkey_list):
            for item, new_monkey_index in monkey.determine_monkey_throw_index():
                monkey_list[new_monkey_index].add_item(item)
                monkey_inspect_count[idx] += 1
    out_list = list(sorted((monkey_inspect_count.values()), reverse=True))
    return out_list[0] * out_list[1]


# print(part_1(TEST_INPUT, 10000, False))

with open('input.in') as f:
    data = f.read()
    print(part_1(data))