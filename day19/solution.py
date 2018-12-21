
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

part2_key = 10551277

with open('./input.txt') as f:
  registers = [0,0,0,0,0,0]
  pointer_register = int(f.readline().split('#ip ')[-1])
  operations = [line.split() for line in f.readlines()]
  while registers[pointer_register] >= 0 and registers[pointer_register] < len(operations):
    op, a, b, c = operations[registers[pointer_register]]
    make_operation(registers, op, int(a), int(b), int(c))
    registers[pointer_register] += 1
print('part1', registers[0])
part_2 = 0
for i in range(1, part2_key + 1):
    if part2_key % i == 0:
        part_2 += i
print('part2', part_2)