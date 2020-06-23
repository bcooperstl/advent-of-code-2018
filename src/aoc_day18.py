import aoc_day
import fileutils
import sys
import aoc_screen
import copy

class AocDay18(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 18)

    OPEN = '.'
    TREE = '|'
    LUMBERYARD = '#'
    
    translation_map = {OPEN:"open", TREE:"tree", LUMBERYARD:"lumberyard", \
                       "open":OPEN, "tree":TREE, "lumberyard":LUMBERYARD}
    
    def count_components(self, map):
        counts = {"open":0, "tree":0, "lumberyard":0}
        for x in range(map.minX, map.maxX+1):
            for y in range(map.minY, map.maxY+1):
                counts[self.translation_map[map.get(x,y)]] += 1
        return counts
    
    def get_neighbor_counts(self, map, x, y):
        counts = {"open":0, "tree":0, "lumberyard":0}
        cells = []
        #top-left
        if x > map.minX and y > map.minY:
            counts[self.translation_map[map.get(x-1,y-1)]] += 1
        #top
        if y > map.minY:
            counts[self.translation_map[map.get(x,y-1)]] += 1
        #top-right
        if x < map.maxX and y > map.minY:
            counts[self.translation_map[map.get(x+1,y-1)]] += 1
        #left
        if x > map.minX:
            counts[self.translation_map[map.get(x-1,y)]] += 1
        #right
        if x < map.maxX:
            counts[self.translation_map[map.get(x+1,y)]] += 1
        #bottom-left
        if x > map.minX and y < map.maxY:
            counts[self.translation_map[map.get(x-1,y+1)]] += 1
        #bottom
        if y < map.maxY:
            counts[self.translation_map[map.get(x,y+1)]] += 1
        #bottom-right
        if x < map.maxX and y < map.maxY:
            counts[self.translation_map[map.get(x+1,y+1)]] += 1
        return counts
    
    def determine_next_value(self, current, neighbor_counts):
        if current == self.OPEN:
            if neighbor_counts["tree"] >= 3:
                return self.TREE
            else:
                return self.OPEN
        elif current == self.TREE:
            if neighbor_counts["lumberyard"] >= 3:
                return self.LUMBERYARD
            else:
                return self.TREE
        else: # current == self.LUMBERYARD
            if neighbor_counts["lumberyard"] >= 1 and neighbor_counts["tree"] >= 1:
                return self.LUMBERYARD
            else:
                return self.OPEN
    
    def compute_new_map(self, current):
        next = copy.deepcopy(current)
        for x in range(current.minX, current.maxX+1):
            for y in range(current.minY, current.maxY+1):
                next.set(x,y,self.determine_next_value(current.get(x,y), self.get_neighbor_counts(current,x,y)))
        return next

    def part1(self, filename, extra_args):
        start_data = fileutils.read_as_list_of_strings(filename)
        map = aoc_screen.AocScreen(' ')
        map.load(start_data)
        print("Initial map:")
        map.display()
        for minute in range(1,11): # 1 to 10
            map = self.compute_new_map(map)
            print("After",minute,"minutes:")
            map.display()
        counts = self.count_components(map)
        return counts["tree"]*counts["lumberyard"]

    def part2(self, filename, extra_args):
        start_data = fileutils.read_as_list_of_strings(filename)
        map = aoc_screen.AocScreen(' ')
        map.load(start_data)
        print("Initial map:")
        maps = [map]
        map.display()
        repeat_begin=0
        repeat_end=0
        for minute in range(1,1000000001): # 1 to 1 billion. won't got that long
            map = self.compute_new_map(map)
            print("After",minute,"minutes:")
            map.display()
            for index, prior in enumerate(maps):
                if map.equals(prior):
                    repeat_begin = index
                    repeat_end = minute
                    break
            maps.append(map)
            if repeat_begin > 0 and repeat_end > 0:
                break
        period = repeat_end - repeat_begin
        print("Repetition occurs from maps",repeat_begin,"and",repeat_end,"which has period length",period)
        full_periods = (1000000000 - repeat_end) // period
        remainder = (1000000000 - repeat_end) % period
        print("To get to a billion, there are ",full_periods,"periods of length",period,"plus a remainder of ",remainder,"left over")
        target_map = maps[repeat_begin+remainder]
        counts = self.count_components(target_map)
        return counts["tree"]*counts["lumberyard"]
    