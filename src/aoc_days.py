#!/usr/bin/python3

import aoc_day1
import aoc_day2
import aoc_day3
import aoc_day4

class AocDays(object):
    def __init__(self):
        self.programs={
                  1:aoc_day1.AocDay1(),
                  2:aoc_day2.AocDay2(),
                  3:aoc_day3.AocDay3(),
                  4:aoc_day4.AocDay4(),
                 }

    def get(self, day):
        if day in self.programs:
            return self.programs[day]
        else:
            return None

