import aoc_day
import fileutils
import sys
from collections import defaultdict

class AocDay14(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 14)

    def part1(self, filename, extra_args):
        num_recipes = int(extra_args[0])
        extra_recipes = 10
        recipes = [3, 7]
        elf_positions = [0, 1]
        total_to_create = num_recipes + extra_recipes
        while len(recipes) < total_to_create:
            #print("Positions",elf_positions,"Recipes",recipes)
            sum = recipes[elf_positions[0]] + recipes[elf_positions[1]]
            if sum >= 10:
                recipes.append(1)
                recipes.append(sum%10)
            else:
                recipes.append(sum)
            elf_positions[0]=(elf_positions[0]+1+recipes[elf_positions[0]])%len(recipes)
            elf_positions[1]=(elf_positions[1]+1+recipes[elf_positions[1]])%len(recipes)
        #print("Final recipes",recipes)
        return "".join([str(recipe) for recipe in recipes[num_recipes:num_recipes+extra_recipes]])

    def part2(self, filename, extra_args):
        target = extra_args[0]
        target_length = len(target)
        pos_checked = 0
        recipes = [3, 7]
        elf_positions = [0, 1]
        while True:
            if len(recipes)%100000 == 0:
                print("Recipes",len(recipes))
            #print("Positions",elf_positions,"Recipes",recipes)
            sum = recipes[elf_positions[0]] + recipes[elf_positions[1]]
            if sum >= 10:
                recipes.append(1)
                recipes.append(sum%10)
            else:
                recipes.append(sum)
            elf_positions[0]=(elf_positions[0]+1+recipes[elf_positions[0]])%len(recipes)
            elf_positions[1]=(elf_positions[1]+1+recipes[elf_positions[1]])%len(recipes)
            while len(recipes)-pos_checked >= target_length:
                #print("Checking recipes from",pos_checked,recipes)
                if target == "".join([str(recipe) for recipe in recipes[pos_checked:pos_checked+target_length]]):
                    #print("Match found")
                    return pos_checked
                else:
                    pos_checked = pos_checked+1
        #print("Final recipes",recipes)
        return "".join([str(recipe) for recipe in recipes[num_recipes:num_recipes+extra_recipes]])
