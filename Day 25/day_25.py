
TEST_INPUT = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''

CHAR_MAP = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}


def snafu_to_int(snafu_str):
    output = 0
    snafu_str = snafu_str[::-1]
    for counter in range(len(snafu_str)):
        output += (CHAR_MAP[snafu_str[counter]] * (5 ** counter))
    return output


def int_to_snafu(number):
    """
    That was actually the main part here. This is complicated because 3 and 4 are represented as
    1= and 1- respectively. This means despite being base5, they are represented by 2 characters.
    The 1st character in both is 1 which is equivalent to 5. Therefore, when reducing an int to snifu,
    if remainder is 3 or 4, 5 needs to be added in the main number to cater for digit size difference. The
    first character -/= is appended to output.

    * Example
        * Convert 14 to Snafu
            * Iteration 1
                * 14 % 5 == 4 -- output => '-'
                    * Now, if we do 14 // 5, the quotient is 2. 2 % 5 = 2 and output becomes 2- (after reverse)
                        2- is not the correct Snafu representation here.
                    * Add 5 in main number i.e. 14 and divide the result by 5 to avoid 1-off error
                    * (14 + 5) // 5 ==> 3, output => '-'
            * Iteration 2
                * 3 % 5 == 3, output = '-='
                    * (3 + 5) // 5 => 1
            * Iteration 3
                * 1 % 5 == 1 (since 1 is represented as 1, no need to add 5 here), output = '-=1'
        * Final Result: 1=- (25 - 10 - 1)
    """
    number_increment_count = {
        0: 0,
        1: 0,
        2: 0,
        3: 5,
        4: 5
    }
    number_replacement_map = {
        0: '0',
        1: '1',
        2: '2',
        3: '=',
        4: '-'
    }
    output = ''
    while number > 0:
        remainder = number % 5
        number = (number + number_increment_count[remainder]) // 5
        output += number_replacement_map[remainder]
    return output[::-1]


def part_1(data):
    value = 0
    for snafu_number in data.splitlines():
        value += snafu_to_int(snafu_number)
    return int_to_snafu(value)


with open('input.in') as f:
    data = f.read()
    # Part 1: 2=20---01==222=0=0-2
    print(f"Part 1: {part_1(data)}")
