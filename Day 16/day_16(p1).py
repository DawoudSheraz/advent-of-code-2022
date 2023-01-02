import re

TEST_INPUT = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''


def parse(data):
    graph = []
    nodes = []

    for row in data.splitlines():
        row = row.split(' ')
        node = row[1]
        rate = int(re.findall('\\d+', row[4])[0])
        connections = row[(row.index('valves') if 'valves' in row else row.index('valve')) + 1:]
        connections = [x.replace(',', '').strip() for x in connections]
        graph.append({
            'node': node,
            'rate': rate,
            'connections': connections
        })
        nodes.append(node)

    return nodes, graph


def get_node(graph, node):
    return [x for x in graph if x['node'] == node][0]


def get_distances(nodes, graph):
    """
    Create a dictionary containing distance from each node to every other possible node.
    """
    distances = {}
    for main_node in nodes:
        gp_node = get_node(graph, main_node)
        if gp_node['rate'] == 0 and main_node != 'AA':
            continue
        visited = {main_node}
        queue = [(main_node, 0)]
        distances[main_node] = {}
        while len(queue) > 0:
            node, dist = queue.pop(0)
            graph_node = get_node(graph, node)
            for connection in graph_node['connections']:
                connection_node = get_node(graph, connection)
                if connection in visited:
                    continue
                visited.add(node)
                # Keep the distance with the nodes that have non-zero flow rate
                # This reduces the graph size a lot.
                if connection_node['rate'] != 0:
                    distances[main_node][connection] = dist + 1
                queue.append((connection, dist + 1))
    return distances


def dfs(node, graph, distances, visited, time, players, state):
    if time <= 0:
        if players > 1:  # Player 1 has done its part, now let other players do its traversal
            return dfs('AA', graph, distances, visited.copy(), 26, players - 1, state)
        return 0

    if (node, visited, time) in state:
        return state[(node, visited, time)]

    max_pressure = 0
    for neighbor in distances[node]:
        if neighbor in visited:
            continue
        neighbor_node = get_node(graph, neighbor)
        time_remaining = time - distances[node][neighbor] - 1
        visited_added = visited | {node}
        output = dfs(neighbor, graph, distances, visited_added, time_remaining, players, state) + (
                time_remaining * neighbor_node['rate'])
        max_pressure = max(max_pressure, output)
        state[(node, visited, time)] = output

    return max_pressure


def part_1(data, start='AA'):
    nodes, graph = parse(data)
    distances = get_distances(nodes, graph)
    return dfs(start, graph, distances, frozenset(), 30, 1, {})


def part_2(data, start='AA'):
    nodes, graph = parse(data)
    distances = get_distances(nodes, graph)
    state = {}
    output = dfs(start, graph, distances, frozenset(), 26, 2, state)
    return output


# print(f"Part 2: {part_2(TEST_INPUT, 'AA')}")
with open('input.in') as f:
    data = f.read()
    # Part 1: 1754
    print(f"Part 1: {part_1(data)}")
    # print(f"Part 2: {part_2(data, 'AA')}")
