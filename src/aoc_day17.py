import aoc_day
import fileutils
import sys
import aoc_screen, aoc_screen_overlay

class AocDay17(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 17)

    CLAY = "#"
    SAND = "."
    SPRING = "+"
    
    # line is either:
    #  x=495, y=2..7
    #  y=7, x=495..501
    #  will return xLow=495, xHigh=495, yLow=2, yHigh=7
    #              xLow=495, xHigh=501, yLow=7, yHigh=7
    def parse_line(self, line):
        parts = line.split(", ")
        range = parts[1][2:].split("..")
        
        return {parts[0][0]+"Low":int(parts[0][2:]), \
                parts[0][0]+"High":int(parts[0][2:]), \
                parts[1][0]+"Low":int(range[0]), \
                parts[1][0]+"High":int(range[1])} 
    
    def part1(self, filename, extra_args):
        clay_locations = [self.parse_line(loc) for loc in fileutils.read_as_list_of_strings(filename)]
        print(clay_locations)
        return 0
    