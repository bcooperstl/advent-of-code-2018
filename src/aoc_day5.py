import aoc_day
import fileutils
import sys

class AocDay5(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 5)

    def part1(self, filename):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        input = fileutils.read_as_string(filename)
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
        return current_length

