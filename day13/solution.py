class Cart:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.direction = direction
    self.next_turn = -1

  def drive(self, tracks):
    if self.direction == '^':
      self.y -= 1
    elif self.direction == 'v':
      self.y += 1
    elif self.direction == '<':
      self.x -= 1
    elif self.direction == '>':
      self.x += 1

    if tracks[self.y][self.x] == '+':
      directions = '<^>v'
      self.direction = directions[(directions.index(self.direction) + self.next_turn) % len(directions)]
      self.next_turn = (self.next_turn + 2) % 3 - 1
    elif tracks[self.y][self.x] == '/':
      m = {'>': '^', 'v': '<', '<': 'v', '^': '>'}
      self.direction = m[self.direction]
    elif tracks[self.y][self.x] == '\\':
      m = {'>': 'v', 'v': '>', '<': '^', '^': '<'}
      self.direction = m[self.direction]

def colliding(carts):
  positions = [(cart.x,cart.y) for cart in carts]
  return len(set(positions)) != len(positions)

with open('./input.txt') as f:
  tracks = [[x for x in line if x != '\n'] for line in f.readlines()]
  carts = []
  for y in range(len(tracks)):
    for x in range(len(tracks[y])):
      if tracks[y][x] in '^v<>':
        carts.append(Cart(x,y,tracks[y][x]))
        if tracks[y][x-1] in '-\\/+' and tracks[y][x+1] in '-\\/+' and tracks[y-1][x] in '|/\\+' and tracks[y+1][x] in '|/\\+':
          tracks[y][x] = '+'
        if tracks[y][x-1] in '-\\/+' and tracks[y][x+1] in '-\\/+':
          tracks[y][x] = '-'
        elif tracks[y-1][x] in '|\\/+' and tracks[y+1][x] in '|\\/+':
          tracks[y][x] = '|'
        elif tracks[y][x-1] in '-\\/':
          tracks[y][x] = '/'
        elif tracks[y][x+1] in '-/\\':
          tracks[y][x] = '\\'
        elif tracks[y+1][x] in '|\\/':
          tracks[y][x] = '/'
        elif tracks[y-1][x] in '|/\\':
          tracks[y][x] = '\\'

  while not colliding(carts):
    carts.sort(key=lambda cart: cart.y)
    for cart in carts:
      positions = [(c.x,c.y) for c in carts]
      if positions.count((cart.x, cart.y)) == 1:
        cart.drive(tracks)

  positions = [(cart.x,cart.y) for cart in carts]
  carts = [cart for cart in carts if positions.count((cart.x, cart.y)) == 1]
  remaining_positions = [(cart.x,cart.y) for cart in carts]
  print('first part', [position for position in positions if position not in remaining_positions][0])

  while len(carts) > 1:
    while not colliding(carts):
      carts.sort(key=lambda cart: cart.y)
      for cart in carts:
        positions = [(c.x,c.y) for c in carts]
        if positions.count((cart.x, cart.y)) == 1:
          cart.drive(tracks)

    positions = [(cart.x,cart.y) for cart in carts]
    carts = [cart for cart in carts if positions.count((cart.x, cart.y)) == 1]

  print('second part', (carts[0].x, carts[0].y))