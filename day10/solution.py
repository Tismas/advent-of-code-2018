from PIL import Image
import re

def draw(points):
    min_x = min(points, key=lambda point: point.x).x
    min_y = min(points, key=lambda point: point.y).y
    for point in points:
      point.x -= min_x
      point.y -= min_y

    width = max(points, key=lambda point: point.x).x
    height = max(points, key=lambda point: point.y).y
    img = Image.new('RGB', (width + 1, height + 1), (0, 0, 0))
    pix = img.load()
    for point in points:
      pix[point.x,point.y] = (255, 255, 255)
    img.save('result.png')


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)


with open('./input.txt') as f:
    points = [Point(x, y, vx, vy) for x, y, vx, vy in (re.search(
        r'position=<([\s|-]?\d+), ([\s|-]?\d+)> velocity=<([\s|-]?\d+), ([\s|-]?\d+)>', line).groups() for line in f.readlines())]

    width = abs(max(points, key=lambda point: point.x).x) - min(points, key=lambda point: point.x).x
    last_width = width
    time = 0
    while width <= last_width:
      for point in points:
        point.x += point.vx
        point.y += point.vy
      last_width = width
      width = abs(max(points, key=lambda point: point.x).x) - min(points, key=lambda point: point.x).x
      time += 1
    time -= 1
    for point in points:
      point.x -= point.vx
      point.y -= point.vy

    draw(points)
    print(time)