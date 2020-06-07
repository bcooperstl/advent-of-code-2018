import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay7(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 7)

    def part1(self, filename, extra_args):
        instructions = fileutils.read_as_split_strings(filename, " ","") # space is delimiter, no comments
        steps = []
        all_values = []
        requirements = defaultdict(list)
        # example is "Step C must be finished before step A can begin."
        #  Will store requirements[A].append(C) based on that
        #  That way the keys define the steps and the values define the dependencies
        for instruction in instructions:
            all_values.append(instruction[1])
            all_values.append(instruction[7])
            requirements[instruction[7]].append(instruction[1])
        all_values=list(set(all_values))
        while all_values:
            next = min(list(filter(lambda x: requirements[x] == [], all_values)))
            print("Next value:",next)
            steps.append(next)
            del requirements[next]
            for requirement in requirements.values(): # it's been satisfied. remove it from the dependencies
                if next in requirement:
                    requirement.remove(next)
            all_values.remove(next)
        return ''.join(steps)
