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
        
    def load(self, data):
        self.minY=0
        self.maxY=len(data)-1
        self.height=len(data)
        self.minX=0
        self.maxX=len(data[0])-1
        self.width=len(data[0])
        self.textmap = [[self.startChar] * self.width for i in range(self.height)]
        for y in range(0,self.height):
            for x in range(0,self.width):
                self.textmap[y][x]=data[y][x]

    def display(self):
        for line in self.textmap:
            print("".join(line))
    
    def equals(self, other):
        if self.minX != other.minX or \
           self.maxX != other.maxX or \
           self.minY != other.minY or \
           self.maxY != other.maxY:
            return False
        for y in range(self.minY, self.maxY+1):
            for x in range (self.minX, self.maxX+1):
                if self.textmap[y][x] != other.textmap[y][x]:
                    return False
        return True
    
    def get(self, x, y):
        return self.textmap[y-self.minY][x-self.minX]
    
    def set(self, x, y, value):
        if not self.minX <= x <= self.maxX:
            print("x value ",x,"is out of range(",self.minX,",",self.maxX,")")
            sys.exit()
        if not self.minY <= y <= self.maxY:
            print("y value ",y,"is out of range(",self.minY,",",self.maxY,")")
            sys.exit()
        self.textmap[y-self.minY][x-self.minX]=value
    
    def set_multi(self, points, value):
        for point in points:
            self.set(point[0], point[1], value)
