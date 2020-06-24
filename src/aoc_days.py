#!/usr/bin/python3

import aoc_day1, aoc_day2, aoc_day3, aoc_day4, aoc_day5
import aoc_day6, aoc_day7, aoc_day8, aoc_day9, aoc_day10
import aoc_day11, aoc_day12, aoc_day13, aoc_day14, aoc_day15
import aoc_day16, aoc_day17, aoc_day18, aoc_day19

class AocDays(object):
    def __init__(self):
        self.programs={
                  1:aoc_day1.AocDay1(), 2:aoc_day2.AocDay2(), 3:aoc_day3.AocDay3(), 4:aoc_day4.AocDay4(), 5:aoc_day5.AocDay5(),
                  6:aoc_day6.AocDay6(), 7:aoc_day7.AocDay7(), 8:aoc_day8.AocDay8(), 9:aoc_day9.AocDay9(), 10:aoc_day10.AocDay10(),
                  11:aoc_day11.AocDay11(), 12:aoc_day12.AocDay12(), 13:aoc_day13.AocDay13(), 14:aoc_day14.AocDay14(), 15:aoc_day15.AocDay15(), 
                  16:aoc_day16.AocDay16(), 17:aoc_day17.AocDay17(), 18:aoc_day18.AocDay18(), 19:aoc_day19.AocDay19(), 
                 }

    def get(self, day):
        if day in self.programs:
            return self.programs[day]
        else:
            return None

