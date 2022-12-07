
from collections import defaultdict

TEST_INPUT = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''


def create_directory_structure(data):
    """
    note to self: This was fun parsing
    """
    directory_sizes = defaultdict(int)
    level_stack = []
    for command in data.splitlines():
        if '$ ls' in command or 'dir' in command:
            continue
        elif '$ cd' in command:
            if '..' in command:
                level_stack.pop()  # move back one level
            else:
                level_stack.append(command.split(' ')[-1])  # new dir at top
        else:
            size = int(command.split(' ')[0])

            # Add size to active and the parents of the active directory
            # start from 1 because [:0] does nothing, +1 is needed to include path
            # for very last element as [:count] does not include complete list if count = length-1.
            # This +1 took a lot of my time.
            for count in range(1, len(level_stack)+1):
                # unique directory paths, assuming nested dirs can have same names
                directory_sizes['//'.join(level_stack[:count])] += size
    return list(directory_sizes.values())


def solve(data_list):
    data_list = sorted(list(map(int, data_list)))

    # total size (/) - # the max size a directory can use and still allow updates
    size_to_free = data_list[-1] - 40000000
    deleted_dir_size = 7000000
    total_size = 0
    for size in data_list:
        if size <= 100000:
            total_size += size
        if size_to_free <= size <= deleted_dir_size:
            deleted_dir_size = size
    return total_size, deleted_dir_size


with open('input.in') as f:
    data = f.read()
    output = solve(create_directory_structure(data))
    # Part 1: 1989474
    # Part 2: 1111607
    print(f"Part 1: {output[0]}")
    print(f"Part 2: {output[1]}")
