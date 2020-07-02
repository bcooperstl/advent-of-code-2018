import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay23(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 23)

    def parse_nanobot_data(self, nanobot_data):
        nanobots = []
        for nanobot in nanobot_data:
            positions = nanobot[0][5:-1].split(",")
            nanobots.append({"x":int(positions[0]), "y":int(positions[1]), "z":int(positions[2]), "radius":int(nanobot[1][2:])})
        return nanobots
    
    def manhattan_distance(self, bot1, bot2):
        return abs(bot1["x"]-bot2["x"]) \
             + abs(bot1["y"]-bot2["y"]) \
             + abs(bot1["z"]-bot2["z"])
             
    def part1(self, filename, extra_args):
        nanobot_data = fileutils.read_as_split_strings(filename, ", ","") # space is delimiter, no comments
        nanobots = self.parse_nanobot_data(nanobot_data)
        strongest = max(nanobots, key=lambda n:n["radius"])
        print("Strongest is:",strongest,"with radius")
        count = sum(1 for nanobot in nanobots if self.manhattan_distance(strongest, nanobot) <= strongest["radius"])
        return count
