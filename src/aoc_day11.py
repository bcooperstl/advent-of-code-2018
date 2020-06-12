import aoc_day
import fileutils
from collections import defaultdict

class AocDay11(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 11)

    def power_level(self, x, y, serial):
        rack_id = x + 10
        power = ((rack_id * y) + serial) * rack_id
        power = ((power // 100) % 10) - 5 # the // is for integer division in python3
        return power
    
    def part1(self, filename, extra_args):
        #print("power(3,5,8) should be 4  is",self.power_level(3,5,8))
        #print("power(122,79,57) should be -5  is",self.power_level(122,79,57))
        #print("power(217,196,39) should be 0  is",self.power_level(217,196,39))
        #print("power(101,153,71) should be 4  is",self.power_level(3,5,8))
        rows=300
        cols=300
        serial_number = int(extra_args[0])
        powers = [[self.power_level(x+1, y+1, serial_number) for x in range(0,cols)] for y in range(0,rows)] 
        sums = [[sum(powers[x][y:y+3])+sum(powers[x+1][y:y+3])+sum(powers[x+2][y:y+3]) for x in range (0,cols-2)] for y in range (0,rows-2)]
        max_x=1
        max_y=1
        max_sum = sums[0][0]
        for x in range(0,cols-2):
            for y in range(0,rows -2):
                if sums[x][y] > max_sum:
                    max_x=x+1
                    max_y=y+1
                    max_sum=sums[x][y]
        return str(max_x)+","+str(max_y)
