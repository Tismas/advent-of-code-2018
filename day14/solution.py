recipes = '37'
first_elf = 0
second_elf = 1
needed_recipes = 147061
while len(recipes) < needed_recipes + 10:
  recipes += str(int(recipes[first_elf]) + int(recipes[second_elf]))
  first_elf += (1 + int(recipes[first_elf]))
  first_elf %= len(recipes)
  second_elf += (1 + int(recipes[second_elf]))
  second_elf %= len(recipes)

print(recipes[needed_recipes:needed_recipes+10])

while str(needed_recipes) not in recipes[-len(str(needed_recipes)) - 2:]:
  recipes += str(int(recipes[first_elf]) + int(recipes[second_elf]))
  first_elf += (1 + int(recipes[first_elf]))
  first_elf %= len(recipes)
  second_elf += (1 + int(recipes[second_elf]))
  second_elf %= len(recipes)

print(recipes.find(str(needed_recipes)))