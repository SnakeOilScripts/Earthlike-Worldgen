from world_creation import *
import sys

def print_points_ascii(points):
    dimensions = points.dimensions
    for y in range(dimensions[1][0], dimensions[1][1]):
        print("|", end="")
        for x in range(dimensions[0][0], dimensions[0][1]):
            if (x,y) in points.points.keys():
                print("#", end="")
            else:
                print(":", end="")
        print("\n", end="")
    for x in range(dimensions[0][0], dimensions[0][1]+1):
        print("_", end="")
    print("\n", end="")


dimensions = ((0, 100),(0, 100))

w = World(dimensions)
w.prepare_tectonics(8, 20)
print_points_ascii(w.tectonics.unify_splits())

for i in range(5):
    w.tectonics.generate()
    w.tectonics.finalize_and_extend_unfinished_splits()

print_points_ascii(w.tectonics.unify_splits())

#print_points_ascii(w.tectonics.unify_splits())
print("unfinished splits remaining: " + str(len([s for s in w.tectonics.splits if w.tectonics.split_unfinished(s)])))
#for plate in w.plates.plates:
#    print_points_ascii(plate)