import aoc_day
import fileutils
import sys

class AocDay5(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 5)

    def remove_pairs(self, input):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        prior_length = 0
        current_length = len(input)
        while prior_length != current_length:
            prior_length = current_length
            for i in range(0,26):
                ul = upper[i]+lower[i]
                lu = lower[i]+upper[i]
                input = input.replace(ul,"")
                input = input.replace(lu,"")
            current_length = len(input)
        return input
    
    def part1(self, filename, extra_args):
        input = fileutils.read_as_string(filename)
        res = self.remove_pairs(input)
        return len(res)
    
    def part2(self, filename, extra_args):
        input = fileutils.read_as_string(filename)
        min_length = len(input)
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0,26):
            length = len(self.remove_pairs(input.replace(upper[i],"").replace(lower[i],"")))
            if length < min_length:
                min_length = length
        return min_length
