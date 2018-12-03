import re
with open('./input.txt') as f:
  fabric = {}
  not_overlaping_ids = []
  overlaping = 0
  for rect in f.readlines():
    id, x, y, w, h = [int(x) for x in re.split(r'[#|\s|@|,|:|x]', rect) if x]
    not_overlaping_ids.append(id)
    for ys in range(y, y+h):
      fabric[ys] = fabric.get(ys, {})
      for xs in range(x, x+w):
        fabric[ys][xs] = fabric[ys].get(xs, []) + [id]

  for y in fabric:
    for x in fabric[y]:
      if len(fabric[y][x]) > 1:
        overlaping += 1
        for id in fabric[y][x]:
          if id in not_overlaping_ids:
            not_overlaping_ids.remove(id)

  print(overlaping)
  print(not_overlaping_ids)
