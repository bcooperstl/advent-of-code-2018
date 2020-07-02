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

    def num_in_range(self, target, nanobots):
        return sum(1 for nanobot in nanobots if self.manhattan_distance(target, nanobot) <= nanobot["radius"])
    
    def gen_edge_targets(self, nanobot):
        return [{"x":nanobot["x"], "y":nanobot["y"], "z":nanobot["z"]}, \
                {"x":nanobot["x"]-nanobot["radius"], "y":nanobot["y"], "z":nanobot["z"]}, \
                {"x":nanobot["x"]+nanobot["radius"], "y":nanobot["y"], "z":nanobot["z"]}, \
                {"x":nanobot["x"], "y":nanobot["y"]-nanobot["radius"], "z":nanobot["z"]}, \
                {"x":nanobot["x"], "y":nanobot["y"]+nanobot["radius"], "z":nanobot["z"]}, \
                {"x":nanobot["x"], "y":nanobot["y"], "z":nanobot["z"]-nanobot["radius"]}, \
                {"x":nanobot["x"], "y":nanobot["y"], "z":nanobot["z"]+nanobot["radius"]}]

    def part2(self, filename, extra_args):
        best_target = None
        best_amount = 0
        
        nanobot_data = fileutils.read_as_split_strings(filename, ", ","") # space is delimiter, no comments
        nanobots = self.parse_nanobot_data(nanobot_data)
        origin = {"x":0, "y":0, "z":0}
        all_targets = sorted([targets for nanobot in nanobots for targets in self.gen_edge_targets(nanobot)], key=lambda t:self.manhattan_distance(t, origin))
        
        for target in all_targets:
            if self.num_in_range(target, nanobots) > best_amount:
                best_target = target
                best_amount = self.num_in_range(target, nanobots)
                print("Setting best target to ",target,"with value",best_amount)
        
        return self.manhattan_distance(origin, best_target)
    