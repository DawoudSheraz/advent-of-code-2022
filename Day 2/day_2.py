
P1_MAP = {
    'A': 'Rock',
    'B': 'Paper',
    'C': 'Scissors'
}

P2_MAP = {
    'X': 'Rock',
    'Y': 'Paper',
    'Z': 'Scissors'
}

SCORE_MAP = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3
}

FORWARD_CHECK_MAP = {
    'Rock': 'Scissors',
    'Scissors': 'Paper',
    'Paper': 'Rock'
}

REVERSE_CHECK_MAP = {
    'Scissors': 'Rock',
    'Rock': 'Paper',
    'Paper': 'Scissors'
}


TEST_INPUT = '''A Y
B X
C Z'''


def get_outcome_score(p1_input, p2_input):
    if p1_input == p2_input:
        return 3
    if FORWARD_CHECK_MAP[p2_input] == p1_input:
        return 6
    return 0


def decrypt_command(p1, p2):
    """
    Used in part 2. Determine player 2 action by selecting appropriate response against player 1 to either win,
    lose, or draw.
    """
    p1_input = P1_MAP[p1]
    if p2 == 'X':  # Lose
        return FORWARD_CHECK_MAP[p1_input]
    elif p2 == 'Y':  # Draw
        return p1_input
    else:  # Win
        return REVERSE_CHECK_MAP[p1_input]


def part_1(data):
    score = 0
    for data_str in data.splitlines():
        p1, p2 = data_str.split(' ')
        p1_input = P1_MAP[p1]
        p2_input = P2_MAP[p2]
        score += get_outcome_score(p1_input, p2_input) + SCORE_MAP[p2_input]
    return score


def part_2(data):
    score = 0
    for data_str in data.splitlines():
        p1, p2 = data_str.split(' ')
        p1_input = P1_MAP[p1]
        p2_input = decrypt_command(p1, p2)
        score += get_outcome_score(p1_input, p2_input) + SCORE_MAP[p2_input]
    return score


with open('input.in') as f:
    data = f.read()
    # Part 1: 13009
    # Part 2: 10398
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
