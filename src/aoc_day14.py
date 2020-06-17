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
