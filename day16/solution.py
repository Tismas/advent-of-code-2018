from copy import copy

operations = {}

def make_operation(registers, opcode, a, b, c):
    if opcode == 'addr':
        registers[c] = registers[a] + registers[b]
    elif opcode == 'addi':
        registers[c] = registers[a] + b
    elif opcode == 'mulr':
        registers[c] = registers[a] * registers[b]
    elif opcode == 'muli':
        registers[c] = registers[a] * b
    elif opcode == 'banr':
        registers[c] = registers[a] & registers[b]
    elif opcode == 'bani':
        registers[c] = registers[a] & b
    elif opcode == 'borr':
        registers[c] = registers[a] | registers[b]
    elif opcode == 'bori':
        registers[c] = registers[a] | b
    elif opcode == 'setr':
        registers[c] = registers[a]
    elif opcode == 'seti':
        registers[c] = a
    elif opcode == 'gtir':
        registers[c] = 1 if a > registers[b] else 0
    elif opcode == 'gtri':
        registers[c] = 1 if registers[a] > b else 0
    elif opcode == 'gtrr':
        registers[c] = 1 if registers[a] > registers[b] else 0
    elif opcode == 'eqir':
        registers[c] = 1 if a == registers[b] else 0
    elif opcode == 'eqri':
        registers[c] = 1 if registers[a] == b else 0
    elif opcode == 'eqrr':
        registers[c] = 1 if registers[a] == registers[b] else 0


with open('./input.txt') as f:
    line = f.readline()
    like_3_or_more = 0
    while 'Before' in line:
        possible_operations = []
        before = eval(line[8:])
        opcode, a, b, c = [int(x) for x in f.readline().split()]
        after = eval(f.readline()[8:])
        f.readline()
        line = f.readline()

        for operation in ['addr','addi','mulr','muli','banr','bani','borr','bori','setr','seti','gtir','gtri','gtrr','eqir','eqri','eqrr']:
            temp = copy(before)
            make_operation(temp, operation, a, b, c)
            if temp == after:
                possible_operations.append(operation)

        if len(possible_operations) >= 3:
            like_3_or_more += 1
        possible_operations_with_elimination = [x for x in possible_operations if x not in operations.values()]
        if len(possible_operations_with_elimination) == 1:
            operation = possible_operations_with_elimination[0]
            operations[opcode] = operation

    print('Part 1: ', like_3_or_more)

    test_inputs = [x.strip() for x in f.readlines() if x.strip()]
    registers = [0, 0, 0, 0]
    for test in test_inputs:
        opcode, a, b, c = [int(x) for x in test.split()]
        make_operation(registers, operations[opcode], a, b, c)

    print('Part 2: ', registers[0])