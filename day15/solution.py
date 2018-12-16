from copy import deepcopy


def debug(m, entities):
    m = deepcopy(m)
    for entity in entities:
        y = entity['y']
        x = entity['x']
        t = entity['type']
        m[y][x] = t
    for y in range(len(m)):
        row = m[y]
        healths = '  '
        for entity in sorted(entities, key=lambda e: e['x']):
            if entity['y'] == y:
                t = entity['type']
                h = entity['health']
                healths += f'{t}({h})  '
        print(''.join(row) + healths)
    print()


def sign(x):
    return 1 if x >= 0 else -1


def bfs(m, entity, entities):
    entities = [e for e in entities if e['health'] > 0]
    y = entity['y']
    x = entity['x']
    queue = [(y, x, [])]
    checked = set()
    checked.add((y, x))
    found = False
    solutions = []
    while queue:
        my, mx, steps = queue.pop(0)
        overlaping_entities = [e for e in entities if e['y'] == my and e['x'] == mx and (my != y or mx != x)]
        if overlaping_entities:
            overlaping_entity = overlaping_entities[0]
            if overlaping_entity['type'] == entity['target']:
                found = True
                solutions.append(steps)
            else:
                continue

        if not found:
            for change in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                dy, dx = change
                # move outside of the map
                if my + dy < 0 or my + dy >= len(m) or mx + dx < 0 or mx + dx >= len(m[0]):
                    continue
                # wall
                if m[my + dy][mx + dx] != '.':
                    continue
                if (my + dy, mx + dx) not in checked:
                    queue.append((my + dy, mx + dx, steps + [(my+dy, mx+dx)]))
                    checked.add((my + dy, mx + dx))
    if solutions:
        return min(solutions, key=lambda solution: len(solution))[0]
    return (0, 0)


def get_attack_target(entity, entities):
    enemies = [e for e in entities if e['type'] == entity['target'] and e['health'] > 0]
    if not enemies:
        return 'No enemies'
    y = entity['y']
    x = entity['x']
    possible_targets = [e for e in enemies if abs(e['y'] - y) + abs(e['x'] - x) == 1]
    if possible_targets:
        return min(possible_targets, key=lambda e: (e['health'], e['y'], e['x']))
    return None


with open('./input.txt') as f:
    original_map = [list(x.strip()) for x in f.readlines()]
    for dmg in range(3, 100):
        rounds = 0
        entities = []
        elf_count = 0
        m = deepcopy(original_map)
        for y in range(len(m)):
            for x in range(len(m[y])):
                if m[y][x] in 'GE':
                    t = m[y][x]
                    target = [e for e in 'GE' if e != t][0]
                    if t == 'E':
                        elf_count += 1
                    entities.append(
                        {'y': y, 'x': x, 'type': t, 'target': target, 'health': 200, 'dmg': dmg if t == 'E' else 3 })
                    m[y][x] = '.'

        while len(set([e['type'] for e in entities])) > 1:
            to_remove = []
            is_full_round = True
            entities.sort(key=lambda e: (e['y'], e['x']))
            for entity in entities:
                if entity['health'] <= 0:
                    continue
                target = get_attack_target(entity, entities)
                if target == 'No enemies':
                    is_full_round = False
                    break
                elif target:
                    target['health'] -= entity['dmg']
                else:
                    dy, dx = bfs(m, entity, entities)
                    if dy != 0 and dx != 0:
                        entity['x'] = dx
                        entity['y'] = dy
                    target = get_attack_target(entity, entities)
                    if target and entity['health'] > 0:
                        target['health'] -= entity['dmg']
                if target and target['health'] <= 0:
                    to_remove.append(target)
            for e in to_remove:
                entities.remove(e)
            rounds += is_full_round
        if dmg == 3:
            print('PART 1')
            print('rounds', rounds)
            print('outcome', rounds * sum([e['health'] for e in entities]))
        if elf_count == len([e for e in entities if e['type'] == 'E']):
            print('PART 2')
            print('attack power needed', dmg)
            print('rounds', rounds)
            print('outcome', rounds * sum([e['health'] for e in entities]))
            break