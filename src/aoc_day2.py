import aoc_day
import fileutils
import sys
import collections
import itertools

class AocDay2(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 2)
    
    def part1(self, filename):
        num_twos = 0
        num_threes = 0
        labels = fileutils.read_as_list_of_strings(filename)
        for label in labels:
            frequencies = collections.defaultdict(int)
            for letter in label:
                frequencies[letter] += 1
            if 2 in frequencies.values():
                num_twos += 1
            if 3 in frequencies.values():
                num_threes += 1
        return num_twos * num_threes
    
    def part2(self, filename):
        labels = fileutils.read_as_list_of_strings(filename)
        for left, right in itertools.combinations(labels, 2):
            num_diff=0
            for pos in range(0,len(left)):
                if left[pos] != right[pos]:
                    num_diff += 1
            if num_diff == 1:
                ret = ""
                for pos in range(0,len(left)):
                    if left[pos] == right[pos]:
                        ret = ret+left[pos]
                return ret
        return ""
    