import re


class Nanobot:
    def __init__(self, inp):
        # pos=<47080643,44475111,58806598>, r=68351961
        x, y, z, r = [int(x) for x in re.split(r'pos=<|,|>|\s|r=', inp) if x]
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]: {self.r}'


def get_dist(pos1, pos2):
    p1 = pos1
    p2 = pos2
    if type(pos1) == Nanobot:
        p1 = (pos1.x, pos1.y, pos1.z)
    if type(pos2) == Nanobot:
        p2 = (pos2.x, pos2.y, pos2.z)
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


with open('./input.txt') as f:
    nanobots = [Nanobot(line) for line in f.readlines()]
    strongest = max(nanobots, key=lambda nanobot: nanobot.r)
    distances = [get_dist(nanobot, strongest) for nanobot in nanobots]
    print('part1', len(
        [distance for distance in distances if distance <= strongest.r]))

    xs, ys, zs = zip(*[(bot.x, bot.y, bot.z) for bot in nanobots])

    min_x, min_y, min_z, max_x, max_y, max_z = min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)
    total_x_dist = max_x - min_x
    dist = total_x_dist + 100

    while True:
        target_count = 0
        best = None
        best_val = None
        min_x, min_y, min_z, max_x, max_y, max_z = min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)
        for x in range(min_x, max_x + 1, dist):
            for y in range(min_y, max_y + 1, dist):
                for z in range(min_z, max_z + 1, dist):
                    count = len([bot for bot in nanobots if (
                        get_dist(bot, (x, y, z)) - bot.r) / dist <= 0])
                    coord_sum = abs(x) + abs(y) + abs(z)
                    if count > target_count:
                        target_count = count
                        best_val = coord_sum
                        best = (x, y, z)
                    elif count == target_count:
                        if not best_val or coord_sum < best_val:
                            best_val = coord_sum
                            best = (x, y, z)
        if dist == 1:
            break
        else:
            print(dist)
            xs = [best[0] - dist, best[0] + dist]
            ys = [best[1] - dist, best[1] + dist]
            zs = [best[2] - dist, best[2] + dist]
            dist //= 2
    print('part2', best_val)
