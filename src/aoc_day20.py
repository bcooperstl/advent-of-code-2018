import aoc_day
import fileutils
import sys
import aoc_screen, aoc_screen_overlay

class Day20Room(object):
    def __init__(self, location):
        self.location = location
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.distance = None
    
    def setNorth(self, other):
        self.north = other
        other.south = self
    
    def setSouth(self, other):
        self.south = other
        other.north = self
    
    def setEast(self, other):
        self.east = other
        other.west = self
    
    def setWest(self, other):
        self.west = other
        other.east = self
    
    def setDirection(self, other, direction):
        if direction == 'N':
            self.setNorth(other)
        elif direction == 'S':
            self.setSouth(other)
        elif direction == 'E':
            self.setEast(other)
        elif direction == 'W':
            self.setWest(other)
        
    
        

class AocDay20(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 20)
    
    grid_changes = {'N':(0,-1), 'S':(0,1), 'E':(1,0), 'W':(-1,0)}
    
    def work_sequence(self, route, start, rooms):
        current = start
        for step in route:
            location = tuple(map(sum, zip(current.location, self.grid_changes[step])))
            if not location in rooms:
                rooms[location] = Day20Room(location)
            next = rooms[location]
            current.setDirection(next, step)
            current = next
        
    def set_distances_from_start(self, start):
        currentRooms = [start]
        distance = 0
        while currentRooms:
            nextRooms = []
            for room in currentRooms:
                print("Setting",room.location,"to distance",distance)
                room.distance = distance
                for neighbor in [room.north, room.south, room.east, room.west]:
                    if (neighbor != None) and neighbor.distance == None:
                        nextRooms.append(neighbor)
            currentRooms = nextRooms
            distance += 1
        
    def part1(self, filename, extra_args):
        start_data = fileutils.read_as_string(filename)
        start_room = Day20Room((0, 0))
        start_room.distance = 0
        rooms = {(0,0):start_room}
        self.work_sequence(start_data[1:-1], start_room, rooms)
        self.set_distances_from_start(start_room)
        maxDistance = max([room.distance for room in rooms.values()])
        return maxDistance
    
    