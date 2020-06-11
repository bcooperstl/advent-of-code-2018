class AocDay9Node(object):
    def __init__(self, value):
        self.value = value
        self.cw = self #clockwise
        self.ccw = self #counterclockwise
    
    def insert_cw(self, other):
        current_cw = self.cw # current clockwise node from self
        
        ## empty list. make them point to each other both ways
        #if self.cw == None and self.ccw == None:
        #    self.cw = other
        #    self.ccw = other
        #    other.cw = self
        #    other.ccw = self
        ## otherwise, other goes in place clockwise after self. 
        ## a - b has relationships a.cw = b and b.ccw = a
        ## need to make:
        ##     a.cw = other
        ##     other.cw = b
        ##     other.ccw = a
        ##     b.ccw = other
        #else:
        #    self.cw = other
        #    other.cw = current_cw
        #    current_cw.ccw = other
        #    other.ccw = self
        self.cw = other
        other.cw = current_cw
        current_cw.ccw = other
        other.ccw = self
    
    def remove(self):
        # need to remove this node from the chain. set its cw node's ccw to its ccw and vise-versa
        current_cw = self.cw # current clockwise node from self
        current_ccw = self.ccw
        current_cw.ccw = current_ccw
        current_ccw.cw = current_cw
        