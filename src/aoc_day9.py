import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay9(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 9)

    def play_game(self, num_players, last_marble):
        circle = [0, 1] #init value
        current_circle_pos = 1
        
        scores = [0]*num_players
        
        current_player = 2
         # need to use the last mable
        for i in range(2,last_marble+1):
            #print("Move",i,"Player:",current_player)
            if i % 23 != 0:
                # normal play - not divisible by 23
                next_marble_pos = (current_circle_pos + 2)%len(circle)
                circle.insert(next_marble_pos, i)
                current_circle_pos = next_marble_pos
            else:
                # special case - divisible by 23
                scores[current_player] += i
                remove_marble_pos = (current_circle_pos - 7)%len(circle)
                scores[current_player] += circle[remove_marble_pos]
                del circle[remove_marble_pos]
                current_circle_pos = remove_marble_pos
            #print("Circle:",circle)
            #print("Scores:",scores)
            current_player = (current_player + 1) % num_players
        return circle, scores
    
    def part1(self, filename, extra_args):
        input = fileutils.read_as_split_strings_one_line(filename, " ","") # space is delimiter, no comments
        num_players = int(input[0])
        last_marble = int(input[6])
        endgame, scores = self.play_game(num_players, last_marble)
        return max(scores)
    