import aoc_day
import fileutils
import sys

class AocDay6(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 6)

    def rescale_points_to_offset(self, original_points, offset):
        min_x = min(x for x in original_points[0])
        min_y = min(y for y in original_points[1])
        new_points = []
        for point in original_points:
            new_points.append([point[0]-min_x+offset, point[1]-min_y+offset])
        return new_points
    
    def manhattan_distance(self, point1, point2):
        return (abs(point1[0]-point2[0])+abs(point1[1]-point2[1]))
    
    # want to be able to use grid[x][y] to get the points. Need to work in column then row
    def work_grid(self, height, width, points):
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
                cell['min_point_index'] = 0
                cell['min_multi'] = False
                for point_index in range(1, len(points)):
                    distance = self.manhattan_distance([x,y], points[point_index])
                    if distance < cell['min_distance']:
                        cell['min_distance'] = distance
                        cell['min_point_index'] = point_index
                        cell['min_multi'] = False
                    elif distance == cell['min_distance']:
                        cell['min_point_index'] = None
                        cell['min_multi'] = True
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
        counts = [0] * len(my_points)
        for col in grid:
            for cell in col:
                if cell['min_point_index'] is not None and cell['min_point_index'] in finite_points:
                    counts[cell['min_point_index']] += 1
        return max(counts)
    
    def part1(self, filename):
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
    