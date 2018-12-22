with open('./input.txt') as f:
    depth = int(f.readline().split('depth: ')[1])
    target_x, target_y = [int(x) for x in f.readline().split('target: ')[1].split(',')]
    index = {}
    level = {}
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            if (x == 0 and y == 0) or (x == target_x and y == target_y):
                index[(x, y)] = 0
            elif y == 0:
                index[(x, y)] = x * 16807
            elif x == 0:
                index[(x, y)] = y * 48271
            else:
                index[(x, y)] = level[(x-1, y)] * level[(x,y-1)]
            level[(x, y)] = (index[(x, y)] + depth) % 20183
    
    s = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            s += level[(x, y)] % 3
    print(s)