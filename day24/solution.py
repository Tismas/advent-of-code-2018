from copy import deepcopy 
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
        return f'Group {self.id}: {self.units} units with {self.hp} hp and {self.damage} damage'

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

def is_draw(forces1, forces2):
    for group1 in forces1:
        for group2 in forces2:
            if group1.damage_type not in group2.immunities:
                return False
    return True

with open('./input.txt') as f:
    immune_system_boost = 0
    min_immune_system_found = False
    min_immune_system_boost = 0
    max_immune_system_boost = 100000000
    original_immune_system, original_infection = load_input(f)
    while not min_immune_system_found:
        immune_system = deepcopy(original_immune_system)
        infection = deepcopy(original_infection)
        for group in immune_system:
            group.damage += immune_system_boost
            group.effective_power = group.damage * group.units
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
            if is_draw(immune_system, infection):
                break

        immune_system_units = sum([group.units for group in immune_system])
        infection_units = sum([group.units for group in infection])
        if immune_system_boost == 0:
            print('part 1', immune_system if immune_system else infection_units )
        
        if immune_system_units and not infection_units:
            max_immune_system_boost = immune_system_boost - 1
            immune_system_boost = (max_immune_system_boost + min_immune_system_boost) // 2
        else:
            min_immune_system_boost = immune_system_boost + 1
            immune_system_boost = (max_immune_system_boost + min_immune_system_boost) // 2

        if max_immune_system_boost <= min_immune_system_boost:
            min_immune_system_found = True

    print(immune_system_units)