import aoc_day
import fileutils
import sys
import aoc_screen
import copy

class AocDay22(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 22)

    ROCKY = '.'
    WET = "="
    NARROW = "|"
    MOUTH = "M"
    TARGET = "T"
    
    other_equip = {ROCKY:{"torch":"climbing","climbing":"torch"}, \
                   WET:{"climbing":"neither","neither":"climbing"}, \
                   NARROW:{"torch":"neither","neither":"torch"}}

    def get_geologic_index(self, region, regions, target):
        if region["x"] == 0 and region["y"] == 0:
            return 0
        elif region["x"] == target["x"] and region["y"] == target["y"]:
            return 0
        elif region["y"] == 0:
            return region["x"] * 16807
        elif region["x"] == 0:
            return region["y"] * 48271
        else:
            return regions[region["y"]][region["x"]-1]["erosion"] * regions[region["y"]-1][region["x"]]["erosion"]
    
    def get_erosion_level(self, region, depth):
        return (region["geologic"]+depth) % 20183
    
    def get_type(self, region):
        if region["erosion"] % 3 == 0:
            return self.ROCKY
        elif region["erosion"] %3 == 1:
            return self.WET
        else:
            return self.NARROW
    
    def get_risk(self, region):
        if region["type"] == self.ROCKY:
            return 0
        elif region["type"] == self.WET:
            return 1
        else:
            return 2
    
    # go from 0 to maxX and 0 from maxY
    def allocate_regions(self, maxX, maxY):
        return [[{"x":x, "y":y} for x in range(0, maxX+1)] for y in range(0, maxY+1)]
        
    def area_total_risk(self, regions, target):
        total = sum(region["risk"] for row in regions[0:target["y"]+1] for region in row[0:target["x"]+1] )
        return total
    
    def work_regions(self, regions, target, depth):
        for row in regions:
            for region in row:
                region["geologic"] = self.get_geologic_index(region, regions, target)
                region["erosion"] = self.get_erosion_level(region, depth)
                region["type"] = self.get_type(region)
                region["risk"] = self.get_risk(region)
    
    def part1(self, filename, extra_args):
        inputs = fileutils.read_as_list_of_strings(filename)
        depth = int(inputs[0].split(" ")[1])
        target = {"x":int(inputs[1].split(" ")[1].split(",")[0]), \
                  "y":int(inputs[1].split(" ")[1].split(",")[1])}
        print("Depth:",depth)
        print("Target:",target)
        regions = self.allocate_regions(target["x"]+5, target["y"]+5)
        self.work_regions(regions, target, depth)
        return self.area_total_risk(regions, target)
        
        
    def add_times(self, regions):
        for row in regions:
            for region in row:
                if region["type"] == self.ROCKY:
                    region["times"]={"torch":None,"climbing":None}
                elif region["type"] == self.WET:
                    region["times"]={"climbing":None,"neither":None}
                else:
                    region["times"]={"torch":None,"neither":None}
        
    def get_neighbors(self, regions, x, y):
        neighbors = []
        #north
        if y > 0:
            neighbors.append(regions[y-1][x])
        #south
        if y < len(regions) - 1:
            neighbors.append(regions[y+1][x])
        #west
        if x > 0:
            neighbors.append(regions[y][x-1])
        #east
        if x < len(regions[0]) - 1:
            neighbors.append(regions[y][x+1])
        return neighbors
    
    def part2(self, filename, extra_args):
        inputs = fileutils.read_as_list_of_strings(filename)
        depth = int(inputs[0].split(" ")[1])
        target = {"x":int(inputs[1].split(" ")[1].split(",")[0]), \
                  "y":int(inputs[1].split(" ")[1].split(",")[1])}
        print("Depth:",depth)
        print("Target:",target)
        maxX = int(target["x"]*5)
        maxY = int(target["y"]*2)
        regions = self.allocate_regions(maxX, maxY)
        self.work_regions(regions, target, depth)
        self.add_times(regions)
        
        regions[0][0]["times"]["torch"] = 0
        regions[0][0]["times"][self.other_equip[regions[0][0]["type"]]["torch"]] = 7
        print(regions[0][0])
        
        regions_hit = [regions[0][0]]
        
        time = 0
        while regions[target["y"]][target["x"]]["times"]["torch"] is None or regions[target["y"]][target["x"]]["times"]["torch"] > (time - 10):
            print("Time is",time)
            for region in regions_hit:
                for equip, visit_time in region["times"].items():
                    if time == visit_time:
                        #print("Analyzing region",region["x"],region["y"],"with",equip,"at time",time)
                        neighbors = self.get_neighbors(regions, region["x"], region["y"])
                        for neighbor in neighbors:
                            #print(neighbor)
                            if equip in neighbor["times"]:
                                #print(" Can enter neighbor",neighbor["x"],neighbor["y"])
                                if neighbor["times"][equip] is None:
                                    #print("  Setting first entry with",equip,"at time",time+1)
                                    neighbor["times"][equip] = time + 1
                                elif neighbor["times"][equip] > (time + 1):
                                    #print("  Updating entry with",equip,"at time",time+1)
                                    neighbor["times"][equip] = time + 1
                                neighbor_other_equip = self.other_equip[neighbor["type"]][equip]
                                if neighbor["times"][neighbor_other_equip] is None:
                                    #print("  Setting first entry with other equip",neighbor_other_equip,"at time",time + 8) # + 1 to get there and + 7 to change
                                    neighbor["times"][neighbor_other_equip] = time + 8
                            if neighbor not in regions_hit:
                                regions_hit.append(neighbor)
            for region in regions_hit:
                times = region["times"].values();
                if None not in times and (min(times) < (time - 30)):
                    regions_hit.remove(region)
            time += 1
        
        return regions[target["y"]][target["x"]]["times"]["torch"]