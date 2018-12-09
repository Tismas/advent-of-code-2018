from collections import deque

with open('./input.txt') as f:
    players_count, last_marble_points = [*map(int, f.readline().split())]
    marbles = deque([0])
    players = [0] * players_count
    
    for points in range(1, last_marble_points * 100 + 1):
        if points % 23 == 0:
            marbles.rotate(7)
            players[points % players_count] += points + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(points)
    
    print(max(players))
    