#!/usr/bin/python3

import aoc_day1, aoc_day2, aoc_day3, aoc_day4, aoc_day5
import aoc_day6, aoc_day7, aoc_day8, aoc_day9

class AocDays(object):
    def __init__(self):
        self.programs={
                  1:aoc_day1.AocDay1(), 2:aoc_day2.AocDay2(), 3:aoc_day3.AocDay3(), 4:aoc_day4.AocDay4(), 5:aoc_day5.AocDay5(),
                  6:aoc_day6.AocDay6(), 7:aoc_day7.AocDay7(), 8:aoc_day8.AocDay8(), 9:aoc_day9.AocDay9(), 
                 }

    def get(self, day):
        if day in self.programs:
            return self.programs[day]
        else:
            return None

