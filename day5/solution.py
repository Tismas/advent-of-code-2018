def reduce_polymer(polymer):
    destroyed_something = False
    for i in range(len(polymer)-1, -1, -1):
        if i+1 >= len(polymer):
            continue
        if polymer[i].lower() == polymer[i+1].lower() and polymer[i].islower() == polymer[i+1].isupper():
            polymer = list(polymer)
            polymer.pop(i+1)
            polymer.pop(i)
            polymer = ''.join(polymer)
            destroyed_something = True
    return polymer, destroyed_something


with open('./input.txt') as f:
    polymer = f.readline()
    destroyed_something = True
    while destroyed_something:
        polymer, destroyed_something = reduce_polymer(polymer)

    print('reduced polymer length', len(polymer))

    unit_types = set()
    shortest = len(polymer)
    for unit in polymer:
        unit_types.add(unit.lower())

    for unit_type in unit_types:
        new_polymer = list(polymer)
        while unit_type in new_polymer:
            new_polymer.remove(unit_type)
        while unit_type.upper() in new_polymer:
            new_polymer.remove(unit_type.upper())

        destroyed_something = True
        while destroyed_something:
            new_polymer, destroyed_something = reduce_polymer(new_polymer)
        if len(new_polymer) < shortest:
          shortest = len(new_polymer)

    print('shortest polymer after removing one unit type', shortest)