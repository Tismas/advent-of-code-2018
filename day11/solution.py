serial_number = 7400
size = 300

grid = []
for y in range(1, size + 1):
  grid.append([])
  for x in range(1, size + 1):
    rack_id = x + 10
    grid[y-1].append(((rack_id * y + serial_number) * rack_id) % 1000 // 100 - 5)

m = 0
mx = 0
my = 0
msize = 0
for sq_size in range(1, 301):
  for y in range(size-sq_size):
    for x in range(size-sq_size):
      s = 0
      for sy in range(sq_size):
        for sx in range(sq_size):
          s += grid[y + sy][x + sx]
      if s > m:
        m = s
        msize = sq_size
        mx = x
        my = y
print(m, mx + 1, my + 1, msize)