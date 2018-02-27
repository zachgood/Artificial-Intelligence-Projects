# Node class used for keeping track of f, g, & h for each state
class Node:
    # Constructor
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h

    # String representation of a node
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

