#!/usr/bin/python3

import aoc_day
import fileutils
import sys

class AocDay1(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 1)
    
    def part1(self, filename):
        total = 0
        values = fileutils.read_as_list_of_strings(filename)
        for value in values:
            if value[0]=='+':
                total+=int(value[1:])
            elif value[0]=='-':
                total-=int(value[1:])
            else:
                print("Invalid input",value)
                sys.exit()
        return total
