import re
from PIL import Image

def draw(m):
    width = len(m[0])
    height = len(m)
    img = Image.new('RGB', (width + 1, height + 1), (0, 0, 0))
    pix = img.load()
    for y in range(height):
        for x in range(width):
            if m[y][x] == '|':
                pix[x,y] = (100, 100, 255)
            elif m[y][x] == '~':
                pix[x,y] = (0, 0, 255)
            elif m[y][x] == '#':
                pix[x,y] = (200, 200, 200)
            else:
                pix[x,y] = (0, 0, 0)
    img.save('result.png')

def map_input_line(line):
    first, second = line.strip().split(', ')
    axis1, value = first.split('=')
    axis2, v1, v2 = re.split(r'=|\.\.', second)
    return {axis1: (int(value), int(value) + 1), axis2: (int(v1), int(v2) + 1)}

def flood(d, to_update):
    dx = d
    should_be_still = True
    while m[y][x+dx] != '#' and m[y+1][x+dx] in '#~':
        if m[y][x+dx] == '.':
            m[y][x+dx] = '|'
            to_update.append((y, x+dx))
        dx += d
    if m[y+1][x+dx] in '|.':
        should_be_still = False
    if m[y+1][x+dx] == '.':
        m[y][x+dx] = '|'
        to_update.append((y, x+dx))
        should_be_still = False
    return should_be_still

with open('./input.txt') as f:
    clays = [map_input_line(line) for line in f.readlines()]
    start_x = min(clays, key=lambda clay: clay['x'][0])['x'][0] - 1
    start_y = min(clays, key=lambda clay: clay['y'][0])['y'][0]
    end_x = max(clays, key=lambda clay: clay['x'][1])['x'][1] - start_x + 1
    end_y = max(clays, key=lambda clay: clay['y'][1])['y'][1] - start_y + 1
    
    m = []
    for y in range(0, end_y):
        m.append([])
        for x in range(0, end_x):
            m[y].append('.')
    
    for clay in clays:
        for y in range(*[clay_y - start_y for clay_y in clay['y']]):
            for x in range(*[clay_x - start_x for clay_x in clay['x']]):
                m[y][x] = '#'

    m[0][500-start_x] = '+'
    m[1][500-start_x] = '|'
    to_update = [(1, 500-start_x)]

    while to_update:
        y, x = to_update.pop(0)
        if m[y][x] != '|' or y + 1 >= len(m):
            continue
        if m[y + 1][x] == '.':
            m[y + 1][x] = '|'
            to_update.append((y+1, x))
        elif m[y + 1][x] in '~#':
            should_be_still = flood(1, to_update)
            if not flood(-1, to_update):
                should_be_still = False
            if should_be_still:
                m[y][x] = '~'
                if m[y][x-1] == '|':
                    to_update.append((y, x-1))
                if m[y][x+1] == '|':
                    to_update.append((y, x+1))
                to_update.append((y-1, x))

    total_part1 = 0
    total_part2 = 0
    for row in m:
        total_part1 += len([x for x in row if x in '~|'])
        total_part2 += len([x for x in row if x == '~'])
    print(total_part1, total_part2)
    draw(m)