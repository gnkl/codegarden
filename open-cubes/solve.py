
# we represent each cube as a binary number
# each number represtents an edge


# the cube should be 
# * connected: all edges should have a contact point
# * 3-dimensional: at least one edge in x, y, and z
# * connected
"""
We are looking the cube from above:

Lower part of the cube
.1.
0 2
.3.

Then the vertical edges

5.6
. .
4.7

Then the upper part of the cube

9.10
. .
8.11

"""


"""
Another way is to give each corner a letter/number 
And express the edges as pairs of corners

lower 
b..c
.  .
.  .
a..d  

upper 
f..g
.  .
.  .
e..h  
"""

"""
Another way is to represent each corener as a 3-bit number

"""

class Corner:
    def __init__(self, x:bool, y:bool, z:bool):
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return f"{self.to_int():03b}"
        # return bin(self.to_int())[2:]
        # return f"({int(self.x)}, {int(self.y)}, {int(self.z)})"
    
    __str__ = __repr__

    # @staticmethod
    def to_int(self):
        return (int(self.x) << 2) | (int(self.y) << 1) | int(self.z)

    @staticmethod
    def from_int(n):
        return Corner((n >> 2) & 1, (n >> 1) & 1, n & 1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # checks if two corners are neighbors
    def nbr(self, other):
        if self == other:
            return False
        is_x_same = int(self.x == other.x)
        is_y_same = int(self.y == other.y)
        is_z_same = int(self.z == other.z)
        return (is_x_same + is_y_same + is_z_same) == 2

all_corners = [
    Corner.from_int(i) for i in range(8)
]

print(all_corners)

class Edge:
    def __init__(self, c1:Corner, c2:Corner):
        if not c1.nbr(c2):
            raise ValueError("Corners are not neighbors")
        c1_smaller = c1.to_int() < c2.to_int()
        self.c1 = c1 if c1_smaller else c2
        self.c2 = c2 if c1_smaller else c1

    def __hash__(self):
        return hash((self.c1.to_int(), self.c2.to_int()))

    def __repr__(self):
        # return f"{(self.c1.to_int(),self.c2.to_int())}"
        return f"({self.c1}, {self.c2})"

    __str__ = __repr__

    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2  

    def nbr(self, other):
        if self == other:
            return False
        return self.c1 == other.c1 or self.c2 == other.c2  

    def is_x_dir(self):
        return self.c1.x != self.c2.x

    def is_y_dir(self):
        return self.c1.y != self.c2.y

    def is_z_dir(self):
        return self.c1.z != self.c2.z

all_edges = list(set(Edge(c1, c2) for c1 in all_corners for c2 in all_corners if c1.nbr(c2)))
print(all_edges)


# all edges should have a contact point with at least one other edge
def are_connected(edges: list[Edge]) -> bool:
    for e1 in edges:
        found_nbr = False
        for e2 in edges:
            if e1.nbr(e2):
                found_nbr = True
                break
        if not found_nbr:
            return False
    return True

# should have at least one edge in each direction
def are_3d(edges: list[Edge]) -> bool:
    if len(edges) < 3:
        return False
    has_x = any(e.is_x_dir() for e in edges)
    has_y = any(e.is_y_dir() for e in edges)
    has_z = any(e.is_z_dir() for e in edges)
    return has_x and has_y and has_z

# TODO: define cube as a set of edges
# TODO: create all possible cubes and check if a different orientation of the same cube is already in the list 
# I think that there are 24 orientations of a cube (6 faces * 4 rotations each)
# I actually thought that there were 12 (as many as edges) but I guess that was wrong, copilot corrected me