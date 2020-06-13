import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay12(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 12)

    def build_map(self, input):
        map = {}
        for i in range(0,32): # all 5 binary digit numbers 0-31
            # convert the binary 0 to . and 1 to #
            map[format(i,'05b').replace('0','.').replace('1','#')]='.'
        for line in input:
            map[line[0]]=line[2]
        return map
    
    def part1(self, filename, extra_args):
        data = fileutils.read_as_split_strings(filename, " ","") # space is delimiter, no comments
        current="...."+data[0][2]+"...." #prepend and append 4 empty pots. will evaulate from 2 before to 2 after
        start_val=-4
        notes=self.build_map(data[2:])
        
        print("Gen 0: length",len(current),"indexed from", start_val,"to",len(current)+start_val-1,current)
        for i in range(1,21):
            next=list(current)
            for c in range(0,len(current)-4):
                next[c+2]=notes[current[c:c+5]]
            while next[0]!='.' or next[1]!='.' or next[2]!='.' or next[3]!='.':
                next.insert(0,'.')
                start_val -= 1
            while next[-1]!='.' or next[-2]!='.' or next[-3]!='.' or next[-4]!='.':
                next.append('.')
            current="".join(next)
            print("Gen",i,": length",len(current),"indexed from", start_val,"to",len(current)+start_val-1,current)
        sum = 0
        for i in range(0,len(current)):
            if current[i] == '#':
                sum += (i + start_val)
        return sum
        
        