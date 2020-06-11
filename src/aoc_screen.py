import sys

class AocScreen(object):
    def __init__(self, startChar=' ', minX=-10, maxX=10, minY=-10, maxY=10):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.width = maxX - minX + 1
        self.height = maxY - minY + 1
        self.startChar = startChar
        self.textmap = [[startChar] * self.width for i in range(self.height)]
        
    def display(self):
        for line in self.textmap:
            print("".join(line))
    
    def set(self, x, y, value):
        if not self.minX <= x <= self.maxX:
            print("x value ",x,"is out of range(",self.minX,",",self.maxX,")")
            sys.exit()
        if not self.minY <= y <= self.maxY:
            print("y value ",y,"is out of range(",self.minY,",",self.maxY,")")
            sys.exit()
        self.textmap[y-self.minY][x-self.minX]=value
    