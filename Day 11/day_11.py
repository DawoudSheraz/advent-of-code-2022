
import re

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

    def __init__(self, items, worry_ops, division_check, monkey_index_true, monkey_index_false):

        self.items = list(map(int, items))
        self.division_check = int(division_check)
        self.monkey_index_true = int(monkey_index_true)
        self.monkey_index_false = int(monkey_index_false)
        self.worry_ops = worry_ops

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

    def determine_monkey_throw_index(self, worry_modulus=None):
        for item in self.items:
            new_worry = self.get_updated_worry(item)
            new_worry = new_worry // 3 if not worry_modulus else new_worry % worry_modulus
            if new_worry % self.division_check == 0:
                yield new_worry, self.monkey_index_true
            else:
                yield new_worry, self.monkey_index_false
        self.items = []


def create_monkey_list(data):
    monkey_list = []
    data = data.splitlines()

    for count in range(0, len(data), 7):
        items = re.findall('\\d+', data[count+1])
        ops = data[count+2].split(' = ')[-1]
        division = re.findall('\\d+', data[count+3])[0]
        truth = re.findall('\\d+', data[count + 4])[0]
        false = re.findall('\\d+', data[count + 5])[0]
        monkey = Monkey(items, ops, division, truth, false)
        monkey_list.append(monkey)
    return monkey_list


def solve(data, rounds=20, calculate_modulus_worry=False):
    monkey_list = create_monkey_list(data)
    monkey_inspect_count = [0] * len(monkey_list)

    mod = None
    if calculate_modulus_worry:
        # Part 2: I have to thank reddit convos for that. The divisors are all prime, so their
        # product is LCM. LCM reduces the worry level and avoids the long division.
        # part of comment from reddit
        # "It stems from the fact that if you have x % p = y, then x % (p*q) = y as well, if q > 1."
        # Well, this seems like one of things that a lot of speed programmers with sharp maths got very quickly. I
        # didn't and had to check reddit. Learned something new, that's what matters.
        mod = 1
        for monkey in monkey_list:
            mod *= monkey.division_check

    for rd in range(rounds):
        for idx, monkey in enumerate(monkey_list):
            for item, new_monkey_index in monkey.determine_monkey_throw_index(worry_modulus=mod):
                monkey_list[new_monkey_index].add_item(item)
                monkey_inspect_count[idx] += 1

    out_list = sorted(monkey_inspect_count)
    return out_list[-1] * out_list[-2]


with open('input.in') as f:
    data = f.read()
    # Part 1: 120384
    # Part 2: 32059801242
    print(f"Part 1: {solve(data)}")
    print(f"Part 2: {solve(data, 10000, True)}")
