import aoc_day, aoc_day9_node
import fileutils
import sys
from collections import defaultdict

class AocDay9(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 9)

    def play_game_array(self, num_players, last_marble):
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
        return scores
    
    def play_game_linked_list(self, num_players, last_marble):
        #init to list of one item with value 0
        current = aoc_day9_node.AocDay9Node(0)
        
        scores = [0]*num_players
        
        current_player = 1
         # need to use the last mable
        for i in range(1,last_marble+1):
            if i % (last_marble / 100) == 0:
                print("Move",i)
            if i % 23 != 0:
                # normal play - not divisible by 23
                new_node = aoc_day9_node.AocDay9Node(i)
                current.cw.insert_cw(new_node)
                current = new_node
            else:
                # special case - divisible by 23
                scores[current_player] += i
                to_remove = current.ccw.ccw.ccw.ccw.ccw.ccw.ccw
                scores[current_player] += to_remove.value
                current = to_remove.cw
                to_remove.remove()
            #print("Scores:",scores)
            current_player = (current_player + 1) % num_players
        return scores

    def part1(self, filename, extra_args):
        input = fileutils.read_as_split_strings_one_line(filename, " ","") # space is delimiter, no comments
        num_players = int(input[0])
        last_marble = int(input[6])
        scores1 = self.play_game_array(num_players, last_marble)
        scores2 = self.play_game_linked_list(num_players, last_marble)
        return max(scores2)

    def part2(self, filename, extra_args):
        input = fileutils.read_as_split_strings_one_line(filename, " ","") # space is delimiter, no comments
        num_players = int(input[0])
        last_marble = int(input[6])*100
        scores = self.play_game_linked_list(num_players, last_marble)
        return max(scores)
    