from collections import defaultdict

# = water - no torch
# . rocks - no neither
# | narrow - no climbing

def estimate(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def get_time(path):
    time = 0
    for i in range(len(path) - 1):
        if path[i][2] == path[i+1][2]:
            time += 1
        else:
            time += 7
    return time

def get_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path

def get_dist_and_tool(region, current, neighbour):
    tool = current[2]
    dest_reg = region[(neighbour[0], neighbour[1])]
    if tool == 'torch':
        if dest_reg == 0 or dest_reg == 2:
            return 1
    elif tool == 'neither':
        if dest_reg == 1 or dest_reg == 2:
            return 1
    elif tool == 'climbing':
        if dest_reg == 0 or dest_reg == 1:
            return 1

    return float('inf')

def a_star(region, goal):
    start = (0,0,'torch')
    closed_set = []
    open_set = [start]
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    f_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    f_score[start] = estimate(start, goal)
    min_f_score = float('inf')

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])
        if current == goal:
            return get_path(came_from, current)
        
        open_set.remove(current)
        closed_set.append(current)

        for change in [(-1,0),(1,0),(0,-1),(0,1),'climbing','torch','neither']:
            neighbour = None
            dist = None
            if type(change) == tuple:
                neighbour = (current[0] + change[0], current[1] + change[1], current[2])
                if neighbour[0] < 0 or neighbour[1] < 0:
                    continue
                dist = get_dist_and_tool(region, current, neighbour)
            else:
                reg = region[(current[0], current[1])]
                if (reg == 0 and change == 'neither') or (reg == 1 and change == 'torch') or (reg == 2 and change == 'climbing'):
                    continue
                neighbour = (current[0], current[1], change)
                dist = 7
            if neighbour in closed_set:
                continue
            tentative_g_score = g_score[current] + dist
            if neighbour not in open_set:
                open_set.append(neighbour)
            elif tentative_g_score >= g_score[neighbour]:
                continue
            
            came_from[neighbour] = current
            g_score[neighbour] = tentative_g_score
            heuristic_distance = estimate(neighbour, goal)
            f_score[neighbour] = g_score[neighbour] + heuristic_distance
            if heuristic_distance < min_f_score:
                min_f_score = heuristic_distance
                print(min_f_score)
            

with open('./input.txt') as f:
    extra_space = 200
    depth = int(f.readline().split('depth: ')[1])
    target_x, target_y = [int(x) for x in f.readline().split('target: ')[1].split(',')]
    index = {}
    level = {}
    region = {}
    for y in range(target_y + 1 + extra_space):
        for x in range(target_x + 1 + extra_space):
            if (x == 0 and y == 0) or (x == target_x and y == target_y):
                index[(x, y)] = 0
            elif y == 0:
                index[(x, y)] = x * 16807
            elif x == 0:
                index[(x, y)] = y * 48271
            else:
                index[(x, y)] = level[(x-1, y)] * level[(x,y-1)]
            level[(x, y)] = (index[(x, y)] + depth) % 20183
            region[(x, y)] = level[(x, y)] % 3
    
    s = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            s += region[(x, y)]
    print('part1', s)

    path = a_star(region, (target_x, target_y, 'torch'))
    print('part2', path)
    print('time', get_time(path))