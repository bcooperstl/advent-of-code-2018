import sys
import aoc_screen

class AocScreenOverlay(aoc_screen.AocScreen):
    def __init__(self, baseScreen, blankChar=' '):
        aoc_screen.AocScreen.__init__(self, blankChar, baseScreen.minX, baseScreen.maxX, baseScreen.minY, baseScreen.maxY)
        self.baseScreen = baseScreen
        self.blankChar = blankChar
        
    def display_overlay(self):
        combined_lines = []
        for y in range (0,self.height):
            line = []
            for x in range (0,self.width):
                line.append(self.get(x,y))
            combined_lines.append(line)
        
        for line in combined_lines:
            print("".join(line))
    
    def get(self, x, y):
        if self.textmap[y][x]==self.blankChar:
            return self.baseScreen.get(x,y)
        else:
            return self.textmap[y][x]
    
    def clear(self, x, y):
        self.set(x, y, self.blankChar)
    