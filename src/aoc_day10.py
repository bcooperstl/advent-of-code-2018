import aoc_day, aoc_screen
import fileutils
import sys
from collections import defaultdict

class AocDay10(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 10)

    def displayIt(self, minX, maxX, minY, maxY, points):
        screen = aoc_screen.AocScreen('.', minX, maxX, minY, maxY)
        for point in points:
            screen.set(point["posX"], point["posY"], '#')
        screen.display()

    def part1(self, filename, extra_args):
        lines = fileutils.read_as_list_of_strings(filename)
        points = []
        for line in lines:
            line = line.replace("position=<","").replace("> velocity=<",",").replace(">","").replace(" ","")
            values = [int(val) for val in line.split(",")]
            point = {"posX":values[0], "posY":values[1], "velX":values[2], "velY":values[3]}
            points.append(point)
        shouldRun = True
        time = 0
        while shouldRun:
            minX = points[0]["posX"] + points[0]["velX"]
            maxX = points[0]["posX"] + points[0]["velX"]
            minY = points[0]["posY"] + points[0]["velY"]
            maxY = points[0]["posY"] + points[0]["velY"]
            for point in points:
                point["posX"] = point["posX"] + point["velX"]
                point["posY"] = point["posY"] + point["velY"]
                if point["posX"] < minX:
                    minX = point["posX"]
                if point["posX"] > maxX:
                    maxX = point["posX"]
                if point["posY"] < minY:
                    minY = point["posY"]
                if point["posY"] > maxY:
                    maxY = point["posY"]
            if (maxX - minX <= 100) or (maxY - minY <= 100):
                print("X range is ",maxX-minX+1," Y range is ",maxY-minY+1,"  Action?")
                print("  d) display")
                print("  q) quit")
                print("  s) skip")
                action = input("> ")
                if action == "q":
                    shouldRun = False
                    print("Elapsed time is",time,"seconds")
                elif action == "d":
                    self.displayIt(minX, maxX, minY, maxY, points)
            time +=1

    def part2(self, filename, extra_args):
        self.part1(filename, extra_args)