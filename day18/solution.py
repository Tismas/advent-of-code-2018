from copy import deepcopy

def getAdjacent(m, x, y):
  res = []
  for dy in [-1, 0, 1]:
    for dx in [-1, 0, 1]:
      if dy != 0 or dx != 0:
        if y+dy >=0 and x+dx>=0 and y+dy<len(m) and x+dx<len(m[0]):
          res.append(m[y + dy][x + dx])
  return res

with open('./input.txt') as f:
  m = [list(x.strip()) for x in f.readlines()]

  for minute in range(1, 11):
    modified_m = deepcopy(m)
    for y in range(len(m)):
      for x in range(len(m[y])):
        adjacent = getAdjacent(m, x, y)
        if m[y][x] == '.' and adjacent.count('|') >= 3:
          modified_m[y][x] = '|'
        elif m[y][x] == '|' and adjacent.count('#') >= 3:
          modified_m[y][x] = '#'
        elif m[y][x] == '#' and (adjacent.count('#') == 0 or adjacent.count('|') == 0):
          modified_m[y][x] = '.'
    m = modified_m

  wood = 0
  lamberyards = 0
  for row in m:
    wood += row.count('|')
    lamberyards += row.count('#')
  print wood * lamberyards