offset = 4
iterations = 50000000000
with open('./input.txt') as f:
    init_state = f.readline().split()[-1]
    pots = '....' + init_state + '....'
    combinations = {}
    for line in [x.strip() for x in f.readlines()]:
        combination, output = line.split(' => ')
        combinations[combination] = output

    iteration = 1
    while iteration <= iterations:
        next_generation = list(pots)
        for i in range(len(pots)):
            combination = ''.join(pots[i-2:i+3])
            next_generation[i] = combinations.get(combination, '.')
        next_generation = ''.join(next_generation)
        cut_offset = next_generation.find('#')
        offset -= cut_offset - 4
        next_pots = '....' + \
            ''.join(
                next_generation[cut_offset:next_generation.rfind('#')+1]) + '....'
        if pots == next_pots:
            offset -= (next_generation.find('#') - 4) * iterations - iteration
            break
        pots = next_pots
        iteration += 1

    s = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            s += (i-offset)
    print(s)
