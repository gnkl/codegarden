
# inspired by this youtube video in 3b1b: https://youtu.be/_BrFKp-U8GI

# we represent each cube as a binary number
# each number represtents an edge
import random
from itertools import combinations

# the cube should be 
# * connected: all edges should have a contact point
# * 3-dimensional: at least one edge in x, y, and z
# * rotationally distinct: no two cubes should be the same when rotated

"""
One way is to represent each corener as a 3-bit number.
Think of the cube in the 3D space with coordinates (x,y,z). Using the thumb rule:
* x = 0 is left, x = 1 is right
* y = 0 is down, y = 1 is up
* z = 0 is back, z = 1 is front

Back:
2.3
. .
0.1

Front:
6.7
. .
4.5

x_rotation = (2,3,6,7,0,1,4,5)
y_rotation = (4,0,6,2,5,1,7,3)
z_rotation = (1,3,0,2,5,7,4,6)
"""


EightInts = tuple[int,int,int,int,int,int,int,int]

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
    
    __hash__ = to_int

    @staticmethod
    def from_int(n):
        return Corner((n >> 2) & 1, (n >> 1) & 1, n & 1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __lt__(self, other):
        return self.to_int() < other.to_int()

    # checks if two corners are neighbors
    def nbr(self, other):
        if self == other:
            return False
        is_x_same = int(self.x == other.x)
        is_y_same = int(self.y == other.y)
        is_z_same = int(self.z == other.z)
        return (is_x_same + is_y_same + is_z_same) == 2
    
    def move_corner(self, orientation: EightInts) -> "Corner":
        after_move = Corner.from_int(orientation[self.to_int()])
        breakpoint()
        return after_move


all_corners = [
    Corner.from_int(i) for i in range(8)
]

print(f"All corners: {all_corners} (len={len(all_corners)})")
# All corners: [000, 001, 010, 011, 100, 101, 110, 111] (len=8)

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
        return f"{(self.c1.to_int(),self.c2.to_int())}"
        # return f"({self.c1}, {self.c2})"

    __str__ = __repr__

    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2  
    
    def __lt__(self, other):
        return self.c1 < other.c1 or (self.c1 == other.c1 and self.c2 < other.c2)

    def get_corners(self):
        return [self.c1, self.c2]

    def nbr(self, other):
        if self == other:
            return False
        return self.c1 == other.c1 or self.c2 == other.c2  
    
    def move_edge(self, orientation: EightInts) -> "Edge":
        c1_moved = self.c1.move_corner(orientation)
        c2_moved = self.c2.move_corner(orientation)
        return Edge(c1_moved, c2_moved)

    def is_x_dir(self):
        return self.c1.x != self.c2.x

    def is_y_dir(self):
        return self.c1.y != self.c2.y

    def is_z_dir(self):
        return self.c1.z != self.c2.z

all_edges = list(set(Edge(c1, c2) for c1 in all_corners for c2 in all_corners if c1.nbr(c2)))
print(f"All edges: {all_edges} (len={len(all_edges)})")
# All edges: [(0, 1), (0, 4), (1, 5), (3, 7), (4, 6), (5, 7), (2, 3), (6, 7), (0, 2), (4, 5), (2, 6), (1, 3)] (len=12)

"""
Using corner 0, with edges 01, 02, 04 can simplify our thinking process
* this corner can be placed in 8 different possible locations (total corners of cube) 
* for each location, there are 3 possible permutations/orientations for the edges
In total, we get 3*8 = 24 transformations

Using the corner 0 (with edges 01,02,04) gives us an unambiguous way to represent the cube orientation:
* we know that corner 3 goes where edges 01,02 meet
* we know that corner 5 goes where edges 01,04 meet
* we know that corner 6 goes where edges 02,04 meet
* we know that corner 7 goes in the last remaining corner

"""

# using the ints of corners
rotation_input = (0,1,2,3,4,5,6,7)
x_rotation = (2,3,6,7,0,1,4,5)
y_rotation = (4,0,6,2,5,1,7,3)
z_rotation = (1,3,0,2,5,7,4,6)
rotations = [x_rotation, y_rotation,z_rotation]

def rotate(corners: EightInts, rotation: EightInts) -> EightInts:
    return tuple(corners[i] for i in rotation)

def rotate_seq(corners: EightInts, sequence: list[EightInts]) -> EightInts:
    tmp = corners
    for rot in sequence:
        tmp = rotate(tmp, rot)
    return tmp

# randomly use the four rotations to find all 24 orientations of the cube
# by chance, we should come across all 24 orientations
random.seed(42)
all_orientations: set[EightInts] = set()

tmp = (0,1,2,3,4,5,6,7)
for i in range(1000):
    r = random.choice(rotations)
    tmp = rotate(tmp, r)
    all_orientations.add(tmp)
assert len(all_orientations) == 24


class Cube:
    def __init__(self, edges: list[Edge]):
        self.edges: set[Edge] = set(edges)
        self.corners: set[Corner]= set(sorted([c for edge in edges for c in edge.get_corners()]))

    def __repr__(self):
        return f"(Corners = {self.corners}, Edges = {self.edges})"
    
    __str__ = __repr__

    def __eq__(self, other):
        return set(self.edges) == set(other.edges)

    def move_cube(self, orientation: EightInts) -> "Cube":
        return Cube([edge.move_edge(orientation) for edge in self.edges])

    # all edges should have a contact point with at least one other edge
    def is_connected(self) -> bool:
        for e1 in self.edges:
            found_nbr = False
            for e2 in self.edges:
                if e1.nbr(e2):
                    found_nbr = True
                    break
            if not found_nbr:
                return False
        return True

    # should have at least one edge in each direction
    def is_3d(self) -> bool:
        if len(self.edges) < 3:
            return False
        has_x = any(e.is_x_dir() for e in self.edges)
        has_y = any(e.is_y_dir() for e in self.edges)
        has_z = any(e.is_z_dir() for e in self.edges)
        return has_x and has_y and has_z

    # # is rotationally distinct from another cube 
    # def is_rot_distinct(self, other: "Cube") -> bool:
    #     for ort in all_orientations:
    #         moved_cube = self.move_cube(ort)
    #         if moved_cube == other:
    #             return False
    #     return True

    def is_rot_equivalent(self, other: "Cube") -> bool:
        for ort in all_orientations:
            moved_cube = self.move_cube(ort)
            if moved_cube == other:
                return True
        return False

    

solution_cubes: list[Cube] = []
total_cubes_checked = 0
for r in range(0, len(all_edges) + 1):
    for edges_subset in combinations(all_edges, r):
        total_cubes_checked += 1
        cube = Cube(list(edges_subset))
        if not cube.is_connected() or not cube.is_3d():
            continue
        if any(cube.is_rot_equivalent(existing_cube) for existing_cube in solution_cubes):
            continue
        solution_cubes.append(cube)


print(f"Checked {total_cubes_checked} cubes (should be 2^{len(all_edges)} = {2**len(all_edges)})")
print(f"Found {len(solution_cubes)} distinct solutions")