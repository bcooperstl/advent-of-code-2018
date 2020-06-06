import aoc_day
import fileutils
import sys

class AocDay6(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 6)

    def rescale_points_to_offset(self, original_points, offset):
        min_x = min(point[0] for point in original_points)
        min_y = min(point[1] for point in original_points)
        new_points = []
        for point in original_points:
            new_points.append([point[0]-min_x+offset, point[1]-min_y+offset])
        return new_points
    
    def manhattan_distance(self, point1, point2):
        return (abs(point1[0]-point2[0])+abs(point1[1]-point2[1]))
    
    # want to be able to use grid[x][y] to get the points. Need to work in column then row
    def work_grid(self, height, width, points):
        #print("points for work_grid",points)
        grid = []
        for x in range(0,width):
            col = []
            for y in range(0,height):
                cell = {}
                current_point=[x,y]
                cell['x'] = x
                cell['y'] = y
                cell['edge'] = ((x in [0, width-1]) or (y in [0, height-1]))
                cell['min_distance'] = self.manhattan_distance(current_point, points[0])
                cell['total_distance'] = self.manhattan_distance(current_point, points[0])
                cell['min_point_index'] = 0
                cell['min_multi'] = False
                #print("*****",current_point,"starts with distance",cell['min_distance'],"from point",cell['min_point_index'])
                for point_index in range(1, len(points)):
                    #if x==points[point_index][0] and y==points[point_index][1]:
                    #    print("POINT MATCH")
                    distance = self.manhattan_distance(current_point, points[point_index])
                    cell['total_distance'] += distance
                    if distance < cell['min_distance']:
                        cell['min_distance'] = distance
                        cell['min_point_index'] = point_index
                        cell['min_multi'] = False
                    #    print("          lower distance",cell['min_distance'],"from point",cell['min_point_index'])
                    elif distance == cell['min_distance']:
                        cell['min_point_index'] = None
                        cell['min_multi'] = True
                    #    print("           same distance",cell['min_distance'],"from point",point_index)
                col.append(cell)
            grid.append(col)
        return grid
    
    def find_finite_points(self, grid, num_points):
        finite_points = list(range(0, num_points))
        for col in grid:
            for cell in col:
                if ((cell['edge'] == True) and (cell['min_point_index'] is not None) and (cell['min_point_index'] in finite_points)):
                    finite_points.remove(cell['min_point_index'])
        return finite_points
    
    def get_largest_finite(self, original_points, padding):
        min_x = min(point[0] for point in original_points)
        max_x = max(point[0] for point in original_points)
        min_y = min(point[1] for point in original_points)
        max_y = max(point[1] for point in original_points)
        width = max_x-min_x+1
        height = max_y-min_y+1
        my_points = self.rescale_points_to_offset(original_points, padding)
        grid = self.work_grid(height+padding*2, width+padding*2, my_points)
        finite_points = self.find_finite_points(grid, len(my_points))
        #print("finite points", finite_points)
        counts = [0] * len(my_points)
        for col in grid:
            for cell in col:
                #print(cell['x'],cell['y'],cell['min_point_index'])
                if cell['min_point_index'] is not None and cell['min_point_index'] in finite_points:
                    counts[cell['min_point_index']] += 1
        #print("finite points", finite_points)
        return max(counts)
    
    def part1(self, filename, extra_args):
        original_points = fileutils.read_as_split_integers(filename, ", ","") # comma then space is delimiter, no comments
        prior_max=0
        current_max = self.get_largest_finite(original_points, 0)
        padding = 0
        print("Padding",padding,"results in max finite area of",current_max)
        while prior_max != current_max:
            padding+=1
            prior_max = current_max
            current_max = self.get_largest_finite(original_points, padding)
            print("Padding",padding,"results in max finite area of",current_max)
        
        return current_max
    
    def part2(self, filename, extra_args):
        original_points = fileutils.read_as_split_integers(filename, ", ","") # comma then space is delimiter, no comments
        max_distance = int(extra_args[0])
        min_x = min(point[0] for point in original_points)
        max_x = max(point[0] for point in original_points)
        min_y = min(point[1] for point in original_points)
        max_y = max(point[1] for point in original_points)
        width = max_x-min_x+1
        height = max_y-min_y+1
        my_points = self.rescale_points_to_offset(original_points, 0)
        grid = self.work_grid(height, width, my_points)

        safe_region_count = 0
        for col in grid:
            for cell in col:
                if cell['total_distance'] < max_distance:
                    safe_region_count += 1
        return safe_region_count
    
