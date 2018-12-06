from itertools import accumulate

with open('./input.txt') as f:
    inputs = [*map(int, f.readlines())]
    sums_history = [0] + list(accumulate(inputs))
    final_sum = sums_history[-1]

    groups = {}
    for i, s in enumerate(sums_history):
        mod = s % final_sum
        groups[mod] = groups.get(mod, []) + [(i, s)]

    min_diff, min_index, min_freq = None, None, None
    for mod in groups:
        group = sorted(groups[mod])
        for i in range(len(group)-1):
            ind1, val1 = group[i]
            ind2, val2 = group[i+1]
            diff = abs(val1 - val2)
            index = ind2
            freq = val1
            if min_diff is None or diff < min_diff or (diff == min_diff and index < min_index):
                min_diff = diff
                min_index = index
                min_freq = freq

    print('Sum:', final_sum)
    print('Min freq:', min_freq)
