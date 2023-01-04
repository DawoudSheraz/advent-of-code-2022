
import re


TEST_INPUT = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''


class Blueprint:

    def __init__(
            self, id, ore_robot_cost, clay_robot_cost, obsidian_ore_cost, obsidian_clay_cost,
            geode_ore_cost, geode_obsidian_cost
    ):

        self.id = id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_ore_cost = obsidian_ore_cost
        self.obsidian_clay_cost = obsidian_clay_cost
        self.geode_ore_cost = geode_ore_cost
        self.geode_obsidian_cost = geode_obsidian_cost
        self.resource_counts = [0, 0, 0, 0]  # clay, ore, obsidian, geode

        self.robots = [0, 1, 0, 0]  # clay, ore, obsidian, geode

    def solve(self, ticks, reduction_factor):
        queue = [(*self.resource_counts, *self.robots, ticks)]
        visited = set()
        best = 0

        ore_max_spend = max(self.ore_robot_cost, self.clay_robot_cost, self.obsidian_ore_cost, self.geode_ore_cost)

        while len(queue) > 0:
            clay, ore, obsidian, geode, c_robots, o_robots, ob_robots, g_robots, tick = queue.pop(0)
            best = max(best, geode)
            # No need to build more robot of any kind (except geode) if the current
            # count of the robot is greater than its max spend amount. Only one robot
            # can be built per one min and having resources than max spend dont actually do anything,
            # other than increasing the branches to check.
            if o_robots >= ore_max_spend:
                o_robots = ore_max_spend
            if c_robots >= self.obsidian_clay_cost:
                c_robots = self.obsidian_clay_cost
            if ob_robots >= self.geode_obsidian_cost:
                ob_robots = self.geode_obsidian_cost

            # This is just to reduce the resource count because
            # additional resources won't have much impact on the robot counts unless geode.
            # This avoids creating unnecessary states whose result would be same as an existing
            # state. Reddit had some better pruning mechanism. I tried this and it worked.
            # Not very fast, as expected.
            if ore >= reduction_factor * ore_max_spend:
                ore = ore_max_spend
            if clay >= reduction_factor * self.obsidian_clay_cost:
                clay = self.obsidian_clay_cost
            if obsidian >= reduction_factor * self.geode_obsidian_cost:
                obsidian = self.geode_obsidian_cost

            state = clay, ore, obsidian, geode, c_robots, o_robots, ob_robots, g_robots, tick
            if state in visited or tick == 0 or (best > ((tick * g_robots) + geode)):
                continue
            visited.add(state)

            queue.append(
                (clay + c_robots, ore + o_robots, obsidian + ob_robots, geode + g_robots,
                 c_robots, o_robots, ob_robots, g_robots, tick - 1)
            )

            if obsidian >= self.geode_obsidian_cost and ore >= self.geode_ore_cost:
                queue.append(
                    (clay + c_robots, ore - self.geode_ore_cost + o_robots,
                     obsidian - self.geode_obsidian_cost + ob_robots, geode + g_robots,
                     c_robots, o_robots, ob_robots, g_robots + 1, tick - 1)
                )
                continue

            if ore >= self.ore_robot_cost:
                queue.append(
                    (clay + c_robots, ore - self.ore_robot_cost + o_robots, obsidian + ob_robots, geode + g_robots,
                     c_robots, o_robots + 1, ob_robots, g_robots, tick - 1)
                )
            if ore >= self.clay_robot_cost:
                queue.append(
                    (clay + c_robots, ore - self.clay_robot_cost + o_robots, obsidian + ob_robots, geode + g_robots,
                     c_robots + 1, o_robots, ob_robots, g_robots, tick - 1)
                )
            if clay >= self.obsidian_clay_cost and ore >= self.obsidian_ore_cost:
                queue.append(
                    (clay - self.obsidian_clay_cost + c_robots, ore - self.obsidian_ore_cost + o_robots,
                     obsidian + ob_robots, geode + g_robots,
                     c_robots, o_robots, ob_robots + 1, g_robots, tick - 1)
                )
        return best

    def get_quality(self, ticks, reduction_factor):
        best = self.solve(ticks, reduction_factor)
        return best * self.id


def create_blueprints(data):
    data = data.splitlines()
    output = []
    for line in data:
        values = list(map(int, re.findall('\\d+', line)))
        bp = Blueprint(
            values[0],
            values[1],
            values[2],
            values[3], values[4],
            values[5], values[6]
        )
        output.append(bp)
    return output


def part_1(data):
    bp_list = create_blueprints(data)
    count = 0
    for bp in bp_list:
        output = bp.get_quality(24, 1.75)
        count += output
    return count


def part_2(data):
    bp_list = create_blueprints(data)
    prod = 1
    for bp in bp_list:
        if bp.id < 4:
            output = bp.get_quality(32, 2)
            prod *= (output / bp.id)
        else:
            break
    return int(prod)


with open('input.in') as f:
    data = f.read()
    # Part 1: 1264
    # Part 2: 13475
    # Note: This is very slow with both parts. Runtime is 2+ minutes (sadly).
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
