#!/usr/bin/python3

import aoc_day1
import aoc_day2

class AocDays(object):
    def __init__(self):
        self.programs={
                  1:aoc_day1.AocDay1(),
                  2:aoc_day2.AocDay2(),
                 }

    def get(self, day):
        if day in self.programs:
            return self.programs[day]
        else:
            return None

