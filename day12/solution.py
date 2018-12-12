padding = 30
with open('./input.txt') as f:
    pots = list('.'*padding + f.readline().split()[-1] + '.'*padding)
    combinations = {}
    for line in [x.strip() for x in f.readlines()]:
        combination, output = line.split(' => ')
        combinations[combination] = output

    for _ in range(20):
      next_generation = pots[:]
      for i in range(0, len(pots)):
          combination = ''.join(pots[i-2:i+3])
          next_generation[i] = combinations.get(combination, '.')
      pots = next_generation

    s = 0
    for i in range(len(pots)):
      if pots[i] == '#':
        s += (i-padding)
    print(s)