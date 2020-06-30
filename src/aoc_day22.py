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
        
        
        