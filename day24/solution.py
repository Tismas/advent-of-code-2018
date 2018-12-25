import re

class Group:
    def __init__(self, text, i):
        data = re.search(r'(\d+) units each with (\d+) hit points (\(.+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)', line).groups()
        self.id = i
        self.units = int(data[0])
        self.hp = int(data[1])
        if data[2]:
            features = re.search(r'\((weak to ((\w|\s|,)+)|immune to ((\w|\s|,)+)|; )+\)', data[2]).groups()
            self.weaknesses = (features[1] or '').split(', ')
            self.immunities = (features[-2] or '').split(', ')
        else:
            self.immunities = []
            self.weaknesses = []
        self.damage = int(data[3])
        self.damage_type = data[4]
        self.initiative = int(data[5])
        self.target = None
        self.targetted_by = None
        self.effective_power = self.damage * self.units

    def calculate_dmg(self, target):
        if self.damage_type in target.immunities:
            return 0
        elif self.damage_type in target.weaknesses:
            return self.effective_power * 2
        return self.effective_power

    def attack(self):
        target = self.target
        killed_units = self.calculate_dmg(target) // target.hp
        target.units -= killed_units
        self.target = None
        target.targetted_by = None
        target.effective_power -= killed_units * target.damage

    def __repr__(self):
        return f'Group {self.id}: {self.units} units with {self.hp} hp and {self.damage} damage\n'

def load_input(f):
    global line
    immune_system = []
    infection = []

    f.readline()
    line = f.readline()
    i = 1
    while line.strip():
        immune_system.append(Group(line, 'immune '+str(i)))
        line = f.readline()
        i += 1

    line = f.readline()
    line = f.readline()
    i = 1
    while line.strip():
        infection.append(Group(line, 'infection '+str(i)))
        line = f.readline()
        i += 1
    
    return immune_system, infection

def select_targets(forces1, forces2):
    potential_targets = forces2[:]
    for group in forces1:
        best_target = None
        best_dmg = 0
        for potential_target in potential_targets: 
            dmg = group.calculate_dmg(potential_target)
            if dmg == 0:
                continue
            if dmg > best_dmg:
                best_target = potential_target
                best_dmg = dmg
            elif dmg == best_dmg:
                if best_target.effective_power == potential_target.effective_power:
                    best_target = best_target if best_target.initiative > potential_target.initiative else potential_target
                else:
                    best_target = best_target if best_target.effective_power > potential_target.effective_power else potential_target 
        if best_dmg > 0:
            group.target = best_target
            best_target.targetted_by = group
            potential_targets.remove(best_target)

with open('./input.txt') as f:
    immune_system, infection = load_input(f)
    while immune_system and infection:
        immune_system.sort(key=lambda group: group.effective_power, reverse=True)
        infection.sort(key=lambda group: group.effective_power, reverse=True)

        select_targets(immune_system, infection)
        select_targets(infection, immune_system)

        all_groups = immune_system + infection
        all_groups.sort(key=lambda group: group.initiative, reverse=True)
        for group in all_groups:
            if group.units > 0 and group.target:
                group.attack()
        
        immune_system = [group for group in immune_system if group.units > 0]
        infection = [group for group in infection if group.units > 0]
        print(immune_system, infection)

    print(sum([group.units for group in immune_system]), sum([group.units for group in infection]))

#  [Group infection 3: 1298 units with 41570 hp and 63 damage - 1298
# , Group infection 7: 309 units with 44733 hp and 258 damage - 273
# , Group infection 1: 1203 units with 57281 hp and 58 damage - 1215
# , Group infection 4: 2106 units with 40187 hp and 33 damage - 2134
# , Group infection 10: 1955 units with 36170 hp and 24 damage - 1950
# , Group infection 6: 3412 units with 24220 hp and 11 damage - 3408
# , Group infection 5: 22 units with 55432 hp and 1687 damage - 22
# , Group infection 2: 238 units with 13627 hp and 108 damage - 238
# ]