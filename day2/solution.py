from collections import Counter


def lev(s1, s2):
    if len(s1) < len(s2):
        return lev(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


with open('./input.txt') as f:
    twos = 0
    threes = 0
    similar = []
    lines = [x.strip() for x in f.readlines()]
    for line in lines:
        c = Counter(line)
        vals = c.values()
        if 2 in vals:
            twos += 1
        if 3 in vals:
            threes += 1
        for line2 in lines:
            if lev(line, line2) == 1:
                if line not in similar:
                    similar.append(line)
                if line2 not in similar:
                    similar.append(line2)

    print('Checksum:', twos * threes)
    print('Similar:', similar)
