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
    opposites = {'N':'S', 'S':'N', 'E':'W', 'W':'E'}
    
    def work_sequence(self, route, start, rooms):
        current = start
        for step in route:
            location = tuple(map(sum, zip(current.location, self.grid_changes[step])))
            if not location in rooms:
                rooms[location] = Day20Room(location)
            next = rooms[location]
            current.setDirection(next, step)
            current = next
        return current
        
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
    
    #def make_options(self, path):
    #    results = [[]]
    #    for char in path:
    #        for result in results:
    #            print(result)
    #            if len(result) > 0 and result[-1][0] == self.opposites[char]:
    #                # have an opposite (NS). drop the last one
    #                del result[-1]
    #            else:
    #                result.append([char])
    #    return results
    
    def is_net_no_movement(self, route):
        for i in range(0,len(route)):
            if route[i] not in self.opposites:
                return False
            if route[0-i-1] != self.opposites[route[i]]:
                return False
        return True
    
    def optimize_options(self, options):
        hasEmpty = False
        hasNetNoMovement = False
        
        for option in options:
            if self.is_net_no_movement(option):
                hasNetNoMovement = True
            if option == "":
                hasEmpty = True
        
        if hasEmpty and hasNetNoMovement:
            options.remove("")
        return options
        
    def process_sequences_recursively(self, route, start, rooms, depth):
        head_sequence_start = 0
        head_sequence_end = -1
        options_start = []
        options_end = []
        tail = ""
        inHead = True
        inOptions = False
        numOptions = 0
        numParens = 0
        for i in range(0,len(route)):
            # found the first ( now into the options
            if inHead and route[i] == '(':
                head_sequence_end = i-1
                numOptions += 1
                options_start.append(i+1)
                options_end.append(-1)
                inOptions = True
                inHead = False
            elif inOptions:
                if route[i] == '(':
                    numParens += 1
                elif route[i] == ')':
                    if numParens == 0:
                        options_end[numOptions-1] = i - 1
                        if i != len(route)-1:
                            tail = route[i+1:]
                        break
                    else:
                        numParens -= 1
                elif route[i] == '|':
                    if numParens == 0:
                        options_end[numOptions-1] = i - 1
                        options_start.append(i+1)
                        options_end.append(-1)
                        numOptions += 1

        # all is just one sequence. set head_sequence_end to the 
        if inHead and head_sequence_end == -1:
            head_sequence_end = len(route)-1
        
        head = route[head_sequence_start:head_sequence_end+1]
        #print("Head is:",head)
        endHead = self.work_sequence(head, start, rooms);
        
        #TODO: Check for situation where one option is net-zero (NWES) and other option is nothing. In that case, skip the nothing option.
        options = [route[options_start[i]:options_end[i]+1] for i in range(0,numOptions)]
        options = self.optimize_options(options)
        
        for option in options:
            self.process_sequences_recursively(option+tail, endHead, rooms, depth+1)
    
    def part1(self, filename, extra_args):
        start_data = fileutils.read_as_string(filename)
        start_room = Day20Room((0, 0))
        start_room.distance = 0
        rooms = {(0,0):start_room}
        #paths = self.make_options(start_data[1:-1])
        #print(paths)
        self.process_sequences_recursively(start_data[1:-1], start_room, rooms,0)
        self.set_distances_from_start(start_room)
        maxDistance = max([room.distance for room in rooms.values()])
        return maxDistance
    
    