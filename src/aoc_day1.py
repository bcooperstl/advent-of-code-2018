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
    
    def value(self, str):
        if str[0]=='+':
            return int(str[1:])
        elif str[0]=='-':
            return -1*int(str[1:])
        else:
            print("Invalid input",str)
            sys.exit()
    
    def part2(self, filename):
        total = 0
        totals = set()
        totals.add(0)
        str_values = fileutils.read_as_list_of_strings(filename)
        int_values = [self.value(s) for s in str_values]
        while True:
            for i in int_values:
                total+=i
                if total in totals:
                    return total
                else:
                    totals.add(total)
        
            