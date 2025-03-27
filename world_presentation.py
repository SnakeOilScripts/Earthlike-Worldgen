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
w.prepare_tectonics(7, 20)

print_points_ascii(w.tectonics.unify_splits())


while w.tectonics.develop_splits() == 0:
    continue

print_points_ascii(w.tectonics.unify_splits())

w.tectonics.activate_unfinished_splits()
w.tectonics.distance_irrelevant()

while w.tectonics.develop_splits() == 0:
    continue

print_points_ascii(w.tectonics.unify_splits())

splits = w.tectonics.unify_splits()
plates = TectonicPlates(dimensions)

complement = plates.generate_from_splits(splits)
print_points_ascii(complement)