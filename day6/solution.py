from PIL import Image
from random import randint

def visualize(grid, width, height):
    colors = [(randint(0, 255),randint(0, 255),randint(0, 255)) for i in range(60)]
    img = Image.new('RGB', (width, height), (0, 0, 0))
    pix = img.load()
    for y in range(height):
        for x in range(width):
            if grid[y][x] != '.':
                pix[x,y] = colors[int(grid[y][x])]
    img.save('areas.png')

def get_dist(point, x, y):
    return abs(point['x'] - x) + abs(point['y'] - y)

def get_closest(points, x, y):
    closest = []
    min_dist = None
    for point_id in points:
        point = points[point_id]
        dist = get_dist(point, x, y)
        if min_dist is None or dist <= min_dist:
            if min_dist == dist:
                closest.append(point)
            else:
                closest = [point]
            min_dist = dist
    return '.' if len(closest) > 1 else closest[0]['id']

with open('./input.txt') as f:
    points = {str(i): {'x': int(x), 'y': int(y), 'area': 0, 'id': str(i)} for i, (x, y) in ((i, line.split(', ')) for i, line in enumerate(f.readlines()))}
    grid_width = max([points[point_id]['x'] for point_id in points]) + 1
    grid_height = max([points[point_id]['y'] for point_id in points]) + 1
    grid = [[get_closest(points, x, y) for x in range(grid_width)] for y in range(grid_height)]
    visualize(grid, grid_width, grid_height)

    infinite_ids = set()
    max_safe_region_dist = 10000
    safe_region_area = 0
    for y in range(grid_height):
        for x in range(grid_width):
            point_id = grid[y][x]
            if point_id != '.':
                point = points[point_id]
                point['area'] += 1
                if x == 0 or x == grid_width - 1 or y == 0 or y == grid_height - 1:
                    infinite_ids.add(point_id)
            
            total_dist = 0
            for point_id in points:
                total_dist += get_dist(points[point_id], x, y)
            if total_dist < max_safe_region_dist:
                safe_region_area += 1

    max_area = max([points[point_id]['area'] for point_id in points if point_id not in infinite_ids])

    print('Max area:', max_area)
    print('Safe area:', safe_region_area)