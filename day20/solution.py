from copy import copy
import json

directions = {
    'W': (-1, 0),
    'E': (1, 0),
    'S': (0, 1),
    'N': (0, -1),
}

class Room:
    rooms = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connected = []
        self.distance = 0
        Room.rooms.append(self)

    def __str__(self):
        return f'{self.x}, {self.y}, {[(r.x, r.y) for r in self.connected]}'
    
    def connect(self, x, y):
        room = Room(x, y)
        self.connected.append(room)
        return room

    def exists(self, x, y):
        return [room for room in Room.rooms if (room.x, room.y) == (x, y)]

    def find_futhest_room(self):
        distance = 0
        queue = self.connected
        while queue:
            distance += 1
            to_add = []
            for room in queue:
                room.distance = distance
                to_add += room.connected
            queue = to_add
        return distance

def connect_rooms(root, moves):
    if not moves:
        return
    move = moves.pop(0)
    if not move:
        return
    if type(move) == list:
        for branch in move:
            connect_rooms(root, branch + moves)
    else:
        current_room = copy(root)
        for direction in move:
            dx, dy = directions[direction]
            x = current_room.x + dx
            y = current_room.y + dy
            exist = root.exists(x, y)
            current_room = exist[0] if exist else current_room.connect(x, y)
        connect_rooms(current_room, moves)

with open('input.txt') as f:
    regex = f.readline().replace('^', '["').replace('$', '"]').replace('(', '",[["').replace(')', '"]],"').replace('|', '"],["')
    moves = json.loads(regex)
    root = Room(0, 0)
    connect_rooms(root, moves)
    print('part1', root.find_futhest_room())
    print('part2', len([r for r in Room.rooms if r.distance >= 1000]))