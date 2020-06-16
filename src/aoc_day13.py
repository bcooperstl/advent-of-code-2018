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
    cart_char_directions = {">":"right", "right":">", "<":"left", "left":"<", \
                            "^":"up", "up":"^", "v":"down", "down":"v"}
    direction_next_offsets = {"right":{"x":1,"y":0}, "left":{"x":-1,"y":0}, "up":{"x":0,"y":-1}, "down":{"x":0,"y":1}}
    
    direction_corners = {"right":{"\\":"down", "/":"up"}, \
                         "left":{"\\":"up", "/":"down"}, \
                         "up":{"\\":"left", "/":"right"}, \
                         "down":{"\\":"right", "/":"left"}, }
    
    # order in this array is for left, straight, right
    direction_intersection = {"right":["up","right","down"], \
                              "left":["down","left","up"], \
                              "up":["left","up","right"], \
                              "down":["right","down","left"], }
    
    def is_corner(self, c):
        return c in ["\\","/"]
    
    def is_intersection(self, c):
        return c == "+"
    
    def split_carts_from_map(self, map, carts_map):
        carts = []
        for y in range(0,map.height):
            for x in range(0,map.width):
                if map.textmap[y][x] in self.cart_chars:
                    char = map.textmap[y][x]
                    carts_map.set(x,y,char)
                    cart = {"x":x, "y":y, "direction":self.cart_char_directions[char], "num_turns":0, "is_collision":False}
                    carts.append(cart)
                    map.set(x,y,self.cart_track_replacement[char])
        return carts
    
    def find_collision(self, x, y, carts):
        for cart in carts:
            if x == cart["x"] and y == cart["y"]:
                return cart
        return None
    
    # return (False, None) if no collisions
    # return (True, collision_cart) if a collision has occurred    
    def work_tick(self, map, carts_map, carts):
        sorted_carts = sorted(carts, key=lambda c:(c["y"],c["x"]))
        first_collision = None
        for cart in sorted_carts:
            if cart["is_collision"]:
                continue
            next_x = cart["x"] + self.direction_next_offsets[cart["direction"]]["x"]
            next_y = cart["y"] + self.direction_next_offsets[cart["direction"]]["y"]
            next_direction = cart["direction"]
            track = map.get(next_x, next_y)
            if self.is_corner(track):
                next_direction = self.direction_corners[cart["direction"]][track]
            elif self.is_intersection(track):
                next_direction = self.direction_intersection[cart["direction"]][cart["num_turns"]%3]
                cart["num_turns"] += 1
            print("Cart facing",cart["direction"],"at (",cart["x"],",",cart["y"],") moving to (",next_x,",",next_y,") facing",next_direction)
            carts_map.clear(cart["x"], cart["y"])
            carts_map.set(next_x, next_y, self.cart_char_directions[cart["direction"]])
            collision = self.find_collision(next_x, next_y, carts)
            cart["x"] = next_x
            cart["y"] = next_y
            cart["direction"] = next_direction
            if collision != None:
                print("COLLISION at (",next_x,",",next_y,")", cart, collision)
                if first_collision == None:
                    first_collision = collision
                cart["is_collision"] = True
                collision["is_collision"] = True
                carts_map.set(next_x, next_y, 'X')
        if first_collision != None:
            return [True, first_collision]
        return [False, None]
    
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
        collision = False
        tick_count = 0
        while not collision:
            tick_count += 1
            collision, collision_cart = self.work_tick(map, carts_map, carts)
            print("***Tick",tick_count)
            print("Base map:")
            map.display()
            print("Carts only map:")
            carts_map.display()
            print("Overlaid map:")
            carts_map.display_overlay()
            print("Carts details:", carts)
        return str(collision_cart["x"])+","+str(collision_cart["y"])
    
    def part2(self, filename, extra_args):
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
        collision = False
        tick_count = 0
        while len(carts) > 1:
            tick_count += 1
            collision, collision_cart = self.work_tick(map, carts_map, carts)
            for cart in carts:
                if cart["is_collision"] == True:
                    carts_map.clear(cart["x"], cart["y"])
            carts = [cart for cart in carts if cart["is_collision"] != True]
            print("***Tick",tick_count)
            #print("Base map:")
            #map.display()
            #print("Carts only map:")
            #carts_map.display()
            #print("Overlaid map:")
            #carts_map.display_overlay()
            print("Carts details:", carts)
        return str(carts[0]["x"])+","+str(carts[0]["y"])
