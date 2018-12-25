class Point:
    def __init__(self, x, y, z, e):
        self.x = x
        self.y = y
        self.z = z
        self.e = e
        self.connected = set()

    def get_dist(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y) + abs(self.z - point.z) + abs(self.e - point.e)

    def get_all_connected(self, connected):
        connected.add(self)
        for point in self.connected:
            if point not in connected:
                connected.update(point.get_all_connected(connected))
        return connected

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z}, {self.e})'

with open('./input.txt') as f:
    points = [Point(*[int(x.strip()) for x in line.split(',') if x]) for line in f.readlines()]
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if points[i].get_dist(points[j]) <= 3:
                points[i].connected.add(points[j])
                points[j].connected.add(points[i])
    
    to_assign = points[:]
    constellations = []
    while to_assign:
        point = to_assign[0]
        constellation = point.get_all_connected(set())
        constellations.append(constellation)
        for point in constellation:
            to_assign.remove(point)

    print(len(constellations))