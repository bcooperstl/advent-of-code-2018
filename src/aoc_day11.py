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
    
    def get_powers(self, edge_length, serial_number):
        #print("Edgelength:",edge_length,"Serial:",serial_number)
        powers = [[self.power_level(x, y, serial_number) for x in range(1,edge_length+1)] for y in range(1,edge_length+1)] 
        #print("Powers:")
        #for row in powers:
        #    print("  ",row)
        return powers
    
    def find_largest_sum(self, powers, powers_edge_length, square_edge_length):
        num_squares_per_row = powers_edge_length - square_edge_length + 1
        #sums = [ [ 0 for x in range (0, num_squares_per_row)] for y in range(0,num_squares_per_row)]
        
        xMax = 0
        yMax = 0
        sumMax = -999999999
       
        #print("Powers:")
        #for row in powers:
        #    print("  ",row)
        
        print("Calculating ",num_squares_per_row*num_squares_per_row,"sums for edge length",square_edge_length)
        
        row_sums = [[0 for x in range(0, num_squares_per_row)] for y in range(0, powers_edge_length)]
        
        #print("Row Sums:")
        #for row in row_sums:
        #    print("  ",row)
        
        for xTmp in range(0, num_squares_per_row):
            for yTmp in range(0, powers_edge_length):
                for xPos in range(xTmp, xTmp+square_edge_length):
                    row_sums[yTmp][xTmp] += powers[yTmp][xPos]

        #print("Row Sums:")
        #for row in row_sums:
        #    print("  ",row)

        for xSum in range (0, num_squares_per_row):
            for ySum in range(0, num_squares_per_row):
                sum = 0
                for yPos in range(ySum, ySum+square_edge_length):
                    sum += row_sums[yPos][xSum]
                if sum > sumMax:
                    #print("Max sum",sum,"from (",xSum,",",ySum,") larger than prior max",sumMax)
                    xMax=xSum
                    yMax=ySum
                    sumMax=sum
                #if square_edge_length==16 and xSum==89 and ySum==268:
                #    print("90,269,16 has sum",sum)
        print("Max sum for a square with edge",square_edge_length," is from (",xMax+1,",",yMax+1,") with sum",sumMax)
        return xMax+1,yMax+1,sumMax
                
    
    def part1(self, filename, extra_args):
        #print("power(3,5,8) should be 4  is",self.power_level(3,5,8))
        #print("power(122,79,57) should be -5  is",self.power_level(122,79,57))
        #print("power(217,196,39) should be 0  is",self.power_level(217,196,39))
        #print("power(101,153,71) should be 4  is",self.power_level(3,5,8))
        edge_length=300
        #edge_length=300
        serial_number = int(extra_args[0])
        powers = self.get_powers(edge_length, serial_number)
        max_x, max_y, max_sum = self.find_largest_sum(powers, edge_length, 3)
        
        return str(max_x)+","+str(max_y)
    
    # 1 2 3 4 
    # 2 3 4 5 
    # 5 6 7 8 
    # 6 7 8 9
    
    def part2(self, filename, extra_args):
        edge_length=300
        serial_number = int(extra_args[0])
        powers = self.get_powers(edge_length, serial_number)
        
        max_x = 0
        max_y = 0
        max_len = 0
        max_sum = -999999999
        for len in range(1,301):
            print("Checking squares of length",len)
            x,y,sum = self.find_largest_sum(powers, edge_length, len)
            if sum > max_sum:
                print("Max sum",sum,"larger than prior max",max_sum)
                max_x=x
                max_y=y
                max_len=len
                max_sum=sum
        return str(max_x)+","+str(max_y)+","+str(max_len)
    