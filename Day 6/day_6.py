

def get_index_value(data, window_size):
    for count in range(0, len(data) - window_size):
        reduced_value = data[count: count+window_size]
        if len(set(reduced_value)) == len(reduced_value):
            return count + window_size


with open('input.in') as f:
    data = f.read()
    # Part 1: 1757
    # Part 2: 2950
    print(f"Part 1: {get_index_value(data, 4)}")
    print(f"Part 2: {get_index_value(data, 14)}")
