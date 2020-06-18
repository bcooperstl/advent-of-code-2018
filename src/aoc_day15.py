import aoc_day
import fileutils
import sys
import aoc_screen, aoc_screen_overlay

class AocDay15(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 15)

    GOBLIN = "G"
    ELF = "E"
    WALL = "#"
    OPEN = "."
    IN_RANGE = "?"
    REACHABLE = "@"
    NEAREST = "!"
    CHOSEN = "+"
    STEP = "*"
    ATTACK_POWER = 3
    START_HITPOINTS = 200
    
    opposite_unit_type = {GOBLIN:ELF, ELF:GOBLIN}
    
    #side effect of this is to change the elves and goblins to open space in the base map. will display them in other places with overlays
    def get_initial_units(self, map):
        units = []
        for y in range(0,map.height):
            for x in range(0,map.width):
                if map.get(x,y) in [self.GOBLIN, self.ELF]:
                    units.append({"id":len(units)+1, "x":x, "y":y, "type":map.get(x,y), "hitpoints":self.START_HITPOINTS})
                    map.set(x,y,self.OPEN)
        return units
    
    def is_next_to(self, one, two):
        if ((one["x"] == two["x"]) and ((one["y"] == (two["y"] - 1)) or (one["y"] == (two["y"] + 1)))):
            return True
        if ((one["y"] == two["y"]) and ((one["x"] == (two["x"] - 1)) or (one["x"] == (two["x"] + 1)))):
            return True
        return False
    
    # if already next to a foe then 
    def should_move(self, unit, foes):
        for foe in foes:
            if self.is_next_to(unit, foe):
                return False
        return True
    
    # return in reading order - up, left, right, down
    def get_neighbor_points(self, point):
        return [(point[0], point[1]-1), (point[0]-1, point[1]), (point[0]+1, point[1]), (point[0], point[1]+1)]
    
    def get_distances_to_open_points(self, point, units_map):
        current_distance = 0
        distances = {point:current_distance}
        last_round = [ point ]
        while last_round:
            current_round = []
            current_distance += 1
            for point in last_round:
                for neighbor in self.get_neighbor_points(point):
                    if neighbor not in distances and units_map.get(neighbor[0], neighbor[1]) == self.OPEN:
                        distances[neighbor]=current_distance
                        current_round.append(neighbor)
            last_round = current_round            
        return distances
            
    def find_move_target_point(self, unit, foes, units_map):
        print("Units:")
        units_map.display_overlay()
        
        # short circuit to return None if there is a foe next to the unit
        unit_neighbor_points = self.get_neighbor_points((unit["x"],unit["y"]))
        for foe in foes:
            if (foe["x"],foe["y"]) in unit_neighbor_points:
                print("Unit at (",unit["x"],",",unit["y"],") is already next to foe at (",foe["x"],",",foe["y"],"). Not moving")
                return None
        
        # find in range
        in_range_targets = []
        for foe in foes:
            for point in self.get_neighbor_points((foe["x"],foe["y"])):
                if units_map.get(point[0], point[1]) == self.OPEN and point not in in_range_targets:
                    in_range_targets.append(point)
        #print("In Range:")
        #in_range_map = aoc_screen_overlay.AocScreenOverlay(units_map)
        #in_range_map.set_multi(in_range_targets, self.IN_RANGE)
        #in_range_map.display_overlay()
        if not in_range_targets:
            return None
        
        #find reachable
        distances_from_unit = self.get_distances_to_open_points((unit["x"], unit["y"]), units_map)
        reachable_targets = []
        for target in in_range_targets:
            if target in distances_from_unit:
                reachable_targets.append(target)
        #print("Reachable:")
        #reachable_map = aoc_screen_overlay.AocScreenOverlay(units_map)
        #reachable_map.set_multi(reachable_targets, self.REACHABLE)
        #reachable_map.display_overlay()
        if not reachable_targets:
            return None
        
        #find nearest
        min_distance = distances_from_unit[reachable_targets[0]]
        nearest_targets = []
        for target in reachable_targets:
            if distances_from_unit[target] < min_distance:
                min_distance = distances_from_unit[target]
                nearest_targets.clear()
            if distances_from_unit[target] == min_distance:
                nearest_targets.append(target)
        #print("Nearest:")
        #nearest_map = aoc_screen_overlay.AocScreenOverlay(units_map)
        #nearest_map.set_multi(nearest_targets, self.NEAREST)
        #nearest_map.display_overlay()
        
        #find chosen
        chosen_target = sorted(nearest_targets, key=lambda t:(t[1],t[0]))[0]
        #print("Chosen:")
        #chosen_map = aoc_screen_overlay.AocScreenOverlay(units_map)
        #chosen_map.set(chosen_target[0], chosen_target[1], self.CHOSEN)
        #chosen_map.display_overlay()
        
        return chosen_target
        
    def find_next_step(self, unit, target_point, units_map):
        distances_from_target = self.get_distances_to_open_points(target_point, units_map)
        min_distance = 0
        next_step = None
        # get_neighbor_points returns in reading order. helps to resolve ties
        for point in self.get_neighbor_points((unit["x"],unit["y"])):
            if point in distances_from_target and (next_step is None or distances_from_target[point] < min_distance):
                min_distance = distances_from_target[point]
                next_step = point
        
        #print("Next Step:")
        #step_map = aoc_screen_overlay.AocScreenOverlay(units_map)
        #step_map.set(next_step[0], next_step[1], self.STEP)
        #step_map.display_overlay()

        return next_step
    
    def find_attack_target(self, unit, foes, units_map):
        possible_targets = self.get_neighbor_points((unit["x"],unit["y"]))
        attack_target = None
        for point in possible_targets:
            for foe in foes:
                if (point == (foe["x"],foe["y"]) and (attack_target is None or foe["hitpoints"] < attack_target["hitpoints"] )):
                    attack_target = foe
        return attack_target
    
    #return true for all units completed or false for combat ended
    def run_round(self, map, units, elf_attack_power):
        attack_powers = {self.GOBLIN:self.ATTACK_POWER,self.ELF:elf_attack_power}
        #sort the units in reading order, which is how they will go in this round
        round_units  = sorted(units, key=lambda u:(u["y"],u["x"]))
        for unit in round_units:
            if unit["hitpoints"] <= 0:
                continue
            units_map = aoc_screen_overlay.AocScreenOverlay(map)
            for u in units:
                if u["hitpoints"] > 0:
                    units_map.set(u["x"], u["y"], u["type"])
            print("Working on unit", unit)
            friends = list(filter(lambda u:u["type"]==unit["type"] and u["id"]!=unit["id"] and u["hitpoints"] > 0, units))
            foes = list(filter(lambda u:u["type"]!=unit["type"] and u["hitpoints"] > 0, units))
            print("Friends:", friends)
            print("Foes:", foes)
            if len(foes) == 0:
                print("No foes remaining. Game is over")
                return False
            move_target = self.find_move_target_point(unit, foes, units_map)
            if move_target !=  None:
                next_step = self.find_next_step(unit, move_target, units_map)
                units_map.clear(unit["x"],unit["y"])
                unit["x"]=next_step[0]
                unit["y"]=next_step[1]
                units_map.set(unit["x"],unit["y"],unit["type"])
            #print("Post Move:")
            #units_map.display_overlay()
            attack_target = self.find_attack_target(unit, foes, units_map)
            if attack_target != None:
                attack_target["hitpoints"] -= attack_powers[unit["type"]]
                if attack_target["hitpoints"] <= 0:
                    print("Unit",attack_target["id"],"at (",attack_target["x"],",",attack_target["y"],") killed")
        return True
        
    def sum_alive_hitpoints(self, units):
        sum = 0
        for unit in units:
            if unit["hitpoints"] > 0:
                sum += unit["hitpoints"]
        return sum
    
    def part1(self, filename, extra_args):
        battlefield = fileutils.read_as_list_of_strings(filename)
        map = aoc_screen.AocScreen(' ')
        map.load(battlefield)
        print("Initial map:")
        map.display()
        units = self.get_initial_units(map)
        print("Cleaned map:")
        map.display()
        units_map = aoc_screen_overlay.AocScreenOverlay(map)
        for u in units:
            units_map.set(u["x"], u["y"], u["type"])
        print("Initial Map:")
        units_map.display_overlay()
        full_rounds = 0
        while self.run_round(map, units, self.ATTACK_POWER):
            full_rounds += 1
            print("After round",full_rounds,":")
            units_map = aoc_screen_overlay.AocScreenOverlay(map)
            for u in units:
                if u["hitpoints"] > 0:
                    units_map.set(u["x"], u["y"], u["type"])
            units_map.display_overlay()
            print(units)
            #remove this. just for testing
            #input("> ")
        
        units_map = aoc_screen_overlay.AocScreenOverlay(map)
        for u in units:
            if u["hitpoints"] > 0:
                units_map.set(u["x"], u["y"], u["type"])
        units_map.display_overlay()
        print(units)
        hitpoints = self.sum_alive_hitpoints(units);
        print("Rounds=",full_rounds,"Hitpoints=",hitpoints)
        return full_rounds*hitpoints

    def run_part2(self, battlefield, elf_attack_power):
        map = aoc_screen.AocScreen(' ')
        map.load(battlefield)
        print("Initial map:")
        map.display()
        units = self.get_initial_units(map)
        print("Cleaned map:")
        map.display()
        units_map = aoc_screen_overlay.AocScreenOverlay(map)
        for u in units:
            units_map.set(u["x"], u["y"], u["type"])
        print("Initial Map:")
        units_map.display_overlay()
        full_rounds = 0
        while self.run_round(map, units, elf_attack_power):
            for unit in units:
                if unit["type"]==self.ELF and unit["hitpoints"] <= 0:
                    return [False, 0]
            full_rounds += 1
            print("After round",full_rounds,":")
            units_map = aoc_screen_overlay.AocScreenOverlay(map)
            for u in units:
                if u["hitpoints"] > 0:
                    units_map.set(u["x"], u["y"], u["type"])
            units_map.display_overlay()
            print(units)
            #remove this. just for testing
            #input("> ")
        
        units_map = aoc_screen_overlay.AocScreenOverlay(map)
        for u in units:
            if u["type"]==self.ELF and u["hitpoints"] <= 0:
                return [False, 0]
            if u["hitpoints"] > 0:
                units_map.set(u["x"], u["y"], u["type"])
        units_map.display_overlay()
        print(units)
        hitpoints = self.sum_alive_hitpoints(units);
        print("Rounds=",full_rounds,"Hitpoints=",hitpoints)
        return [True, full_rounds*hitpoints]
    
    def part2(self, filename, extra_args):
        battlefield = fileutils.read_as_list_of_strings(filename)
        elf_attack_power = self.ATTACK_POWER
        result = self.run_part2(battlefield, elf_attack_power)
        while not result[0]:
            elf_attack_power += 1
            result = self.run_part2(battlefield, elf_attack_power)
        print("No elf deaths with elf_attack_power",elf_attack_power)
        return result[1]
        