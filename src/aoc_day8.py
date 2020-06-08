import aoc_day
import fileutils
import sys

class AocDay8(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 8)

    def build_nodes(self, data, position):
        curr = {}
        child_node_qty = data[position]
        metadata_qty = data[position+1]
        curr["header"] = {"child_node_qty":child_node_qty,"metadata_qty":metadata_qty}
        curr["child_nodes"] = []
        used = 0
        position += 2 # skip past the header info
        used += 2 # used 2 positions for the header info
        for i in range(0, child_node_qty):
            child_node, child_used = self.build_nodes(data, position)
            curr["child_nodes"].append(child_node)
            position += child_used
            used += child_used
        curr["metadata"] = data[position:position+metadata_qty]
        used += metadata_qty
        return curr, used
    
    def sum_metadata(self, node):
        sum = 0
        for metadata in node["metadata"]:
            sum += metadata
        for child_node in node["child_nodes"]:
            sum += self.sum_metadata(child_node)
        return sum
    
    def part1(self, filename, extra_args):
        data = fileutils.read_as_split_integers_one_line(filename, " ","") # space is delimiter, no comments
        nodes, used = self.build_nodes(data, 0)
        sum = self.sum_metadata(nodes)
        return sum
