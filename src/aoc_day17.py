import aoc_day
import fileutils
import sys
import aoc_screen, aoc_screen_overlay

class AocDay17(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 17)

    CLAY = "#"
    SAND = "."
    SPRING = "+"
    FLOWING = "|"
    SPREADING = "~"
    
    SPRING_LOCATION = (500,0)
    
    flow_points_queue = []
    
    # line is either:
    #  x=495, y=2..7
    #  y=7, x=495..501
    #  will return xLow=495, xHigh=495, yLow=2, yHigh=7
    #              xLow=495, xHigh=501, yLow=7, yHigh=7
    def parse_line(self, line):
        parts = line.split(", ")
        range = parts[1][2:].split("..")
        
        return {parts[0][0]+"Low":int(parts[0][2:]), \
                parts[0][0]+"High":int(parts[0][2:]), \
                parts[1][0]+"Low":int(range[0]), \
                parts[1][0]+"High":int(range[1])} 
    
    def find_min_max(self, clay_locations, spring_location):
        ret = {}
        ret["minClayX"] = min(cl["xLow"] for cl in clay_locations)
        ret["maxClayX"] = max(cl["xHigh"] for cl in clay_locations)
        ret["minClayY"] = min(cl["yLow"] for cl in clay_locations)
        ret["maxClayY"] = max(cl["yHigh"] for cl in clay_locations)
        ret["minScreenX"] = ret["minClayX"] - 2
        ret["maxScreenX"] = ret["maxClayX"] + 2
        ret["minScreenY"] = spring_location[1]
        ret["maxScreenY"] = ret["maxClayY"] + 4
        
        return ret
        
    def build_base_screen(self, ranges, clay_locations, spring_location):
        base = aoc_screen.AocScreen(self.SAND, ranges["minScreenX"], ranges["maxScreenX"], ranges["minScreenY"], ranges["maxScreenY"])
        base.set(spring_location[0], spring_location[1], self.SPRING)
        for cl in clay_locations:
            for x in range(cl["xLow"], cl["xHigh"]+1):
                for y in range(cl["yLow"],cl["yHigh"]+1):
                    base.set(x, y, self.CLAY)
        return base
    
    def work_flow_point(self, base_screen, flow_point, ranges):
        print("Working flow from", flow_point)
        new_flow_points = []
        current_down_point = flow_point
        current_left_point = None
        current_right_point = None
        # See how far down we can go
        while base_screen.get(current_down_point[0], current_down_point[1]) in (self.SAND, self.FLOWING):
            base_screen.set(current_down_point[0], current_down_point[1], self.FLOWING)
            current_down_point = (current_down_point[0], current_down_point[1]+1)
            if current_down_point[1]>ranges["maxScreenY"]:
                print("Flowing offscreen heading down from ",flow_point,"at",current_down_point)
                return []
        #print("Got down to",current_down_point)
        # need to go up one here. it's at the clay
        current_down_point = (current_down_point[0], current_down_point[1]-1)
        while not new_flow_points:
            left_edge_point = None
            right_edge_point = None
            left_flow_point = None
            right_flow_point = None
            # work left first
            can_work_left = True
            current_left_point = (current_down_point[0]-1, current_down_point[1])
            while can_work_left:
                # if there is clay to the left, we found an edge
                if base_screen.get(current_left_point[0], current_left_point[1]) == self.CLAY:
                    can_work_left = False
                    #print("Left edge for",current_down_point,"at",current_left_point)
                    left_edge_point = current_left_point
                # if there is sand underneath, that is a new flow point to head down
                elif base_screen.get(current_left_point[0], current_left_point[1]+1) == self.SAND:
                    can_work_left = False
                    left_flow_point = current_left_point
                    #print("Left flow for",current_down_point,"at",current_left_point)
                    new_flow_points.append(left_flow_point)
                # if there is a flow underneath, join it. no need to add a new flow point
                elif base_screen.get(current_left_point[0], current_left_point[1]+1) == self.FLOWING:
                    can_work_left = False
                    left_flow_point = current_left_point
                    #print("Left flow for",current_down_point,"at",current_left_point)
                else:
                    current_left_point = (current_left_point[0]-1, current_left_point[1])
            can_work_right = True
            current_right_point = (current_down_point[0]+1, current_down_point[1])
            while can_work_right:
                # if there is clay to the right, we found an edge
                if base_screen.get(current_right_point[0], current_right_point[1]) == self.CLAY:
                    can_work_right = False
                    #print("right edge for",current_down_point,"at",current_right_point)
                    right_edge_point = current_right_point
                # if there is sand underneath or a flow, that is a new flow point to head down
                elif base_screen.get(current_right_point[0], current_right_point[1]+1) == self.SAND:
                    can_work_right = False
                    right_flow_point = current_right_point
                    #print("right flow for",current_down_point,"at",current_right_point)
                    new_flow_points.append(right_flow_point)
                # if there is a flow underneath, join it. no need to add a new flow point
                elif base_screen.get(current_right_point[0], current_left_point[1]+1) == self.FLOWING:
                    can_work_right = False
                    right_flow_point = current_right_point
                    #print("Right flow for",current_down_point,"at",current_right_point)
                else:
                    current_right_point = (current_right_point[0]+1, current_right_point[1])
            
            # if we have two edge points, fill in the standing water and move up
            if left_edge_point and right_edge_point:
                for x in range(left_edge_point[0]+1, right_edge_point[0]):
                    base_screen.set(x, current_down_point[1], self.SPREADING)
                current_down_point = (current_down_point[0], current_down_point[1]-1)
            else:
                if left_edge_point:
                    left_fill = left_edge_point[0]+1
                else:
                    left_fill = left_flow_point[0]
                if right_edge_point:
                    right_fill = right_edge_point[0]
                else:
                    right_fill = right_flow_point[0]+1
                for x in range(left_fill, right_fill):
                    base_screen.set(x, current_down_point[1], self.FLOWING)
        return new_flow_points
    
    def calc_filled_area(self, base_screen, ranges):
        total = 0
        for x in range(ranges["minClayX"], ranges["maxClayX"]+1):
            for y in range(ranges["minClayY"], ranges["maxClayY"]+1):
                if base_screen.get(x,y) in [self.SPREADING, self.FLOWING]:
                    total += 1
        return total
        
    def part1(self, filename, extra_args):
        clay_locations = [self.parse_line(loc) for loc in fileutils.read_as_list_of_strings(filename)]
        ranges = self.find_min_max(clay_locations, self.SPRING_LOCATION)
        print(ranges)
        base_screen = self.build_base_screen(ranges, clay_locations, self.SPRING_LOCATION)
        base_screen.display()
        flow_points = [(self.SPRING_LOCATION[0], self.SPRING_LOCATION[1]+1)]
        worked_flows = []
        while flow_points:
            flow_point = flow_points.pop(0)
            if flow_point not in worked_flows:
                flow_points.extend(self.work_flow_point(base_screen, flow_point, ranges))
            worked_flows.append(flow_point)
            base_screen.display()
        return self.calc_filled_area(base_screen, ranges)
    