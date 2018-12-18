from copy import deepcopy

def get_adjacent(m, x, y):
  res = []
  for dy in [-1, 0, 1]:
    for dx in [-1, 0, 1]:
      if dy != 0 or dx != 0:
        if y+dy >=0 and x+dx>=0 and y+dy<len(m) and x+dx<len(m[0]):
          res.append(m[y + dy][x + dx])
  return res

with open('./input.txt') as f:
  m = [list(x.strip()) for x in f.readlines()]
  seen = [m]
  repeating_index = 0

  for minute in range(1, 1000):
    modified_m = deepcopy(m)
    for y in range(len(m)):
      for x in range(len(m[y])):
        adjacent = get_adjacent(m, x, y)
        if m[y][x] == '.' and adjacent.count('|') >= 3:
          modified_m[y][x] = '|'
        elif m[y][x] == '|' and adjacent.count('#') >= 3:
          modified_m[y][x] = '#'
        elif m[y][x] == '#' and (adjacent.count('#') == 0 or adjacent.count('|') == 0):
          modified_m[y][x] = '.'
    m = modified_m
    if modified_m in seen:
      repeating_index = seen.index(modified_m)
      break
    seen.append(modified_m)

  repeating_range = len(seen) - repeating_index
  final_index = repeating_index + (1000000000 - repeating_index) % repeating_range
  m = seen[final_index]
  wood = 0
  lamberyards = 0
  for row in m:
    wood += row.count('|')
    lamberyards += row.count('#')
  print(wood * lamberyards)