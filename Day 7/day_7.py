
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
    directory_sizes = defaultdict(int)
    level_stack = []
    for command in data.splitlines():
        if '$ ls' in command:
            continue
        elif '$ cd' in command:
            if '..' in command:
                level_stack.pop()  # move back on level
            else:
                level_stack.append(command.split(' ')[-1])  # new dir at top
        elif 'dir' in command:
            continue
        else:
            size = int(command.split(' ')[0])
            # Add size to active and the parents of the active directory
            for count in range(1, len(level_stack)+1):  # start from 1 because [:0] does nothing
                # unique directory paths
                directory_sizes['/'.join(level_stack[:count])] += size
    return list(directory_sizes.values())


def get_max_size(data_list):
    data_list = list(map(int, data_list))
    data_list = sorted(data_list)
    data_list = [x for x in data_list if x <= 100000]
    sum = 0
    for each in data_list:
        sum += each
    return sum


with open('input.in') as f:
    data = f.read()
    print(get_max_size(create_directory_structure(data)))
