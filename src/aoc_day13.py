import aoc_day
import aoc_screen
import aoc_screen_overlay
import fileutils
import sys

class AocDay13(aoc_day.AocDay):
    def __init__(self):
        aoc_day.AocDay.__init__(self, 13)
    
    cart_chars = [">", "<", "v", "^"]
    cart_track_replacement = {">":"-", "<":"-", "v":"|", "^":"|"}
    cart_char_directions = {">":"east", "east":">", "<":"west", "west":"<", \
                            "^":"north", "north":"^", "v":"south", "south":"v"}
    direction_next_offsets = {"east":{"x":1,"y":0}, "west":{"x":-1,"y":0}, "north":{"x":0,"y":-1}, "south":{"x":0,"y":1}}
    
    def split_carts_from_map(self, map, carts_map):
        carts = []
        for y in range(0,map.height):
            for x in range(0,map.width):
                if map.textmap[y][x] in self.cart_chars:
                    char = map.textmap[y][x]
                    carts_map.set(x,y,char)
                    cart = {"x":x, "y":y, "direction":self.cart_char_directions[char]}
                    carts.append(cart)
                    map.set(x,y,self.cart_track_replacement[char])
        return carts
    
    def part1(self, filename, extra_args):
        instructions = fileutils.read_as_list_of_strings(filename)
        map = aoc_screen.AocScreen(' ')
        map.load(instructions)
        carts_map = aoc_screen_overlay.AocScreenOverlay(map)
        carts = self.split_carts_from_map(map, carts_map)
        print("Base map:")
        map.display()
        print("Carts only map:")
        carts_map.display()
        print("Overlaid map:")
        carts_map.display_overlay()
        print("Carts details:", carts)
