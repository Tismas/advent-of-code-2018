r = [0]*6
v = []
while True:
  r[3] = r[4] | 65536
  r[4] = 6152285
  while True:
    r[4] = r[4] + r[3] % 256
    r[4] = ((r[4] % 16777216) * 65899) % 16777216
    if r[3] < 256:
      break
    r[3] = int(r[3] / 256)
  if r[4] in v:
    print("Part 2: {} (after {} iterations)".format(v[-1], len(v)))
    r[0] = r[4]
  else:
    v.append(r[4])
    if len(v) == 1:
      print("Part 1: {}".format(v[-1]))
  if r[4] == r[0]:
    break