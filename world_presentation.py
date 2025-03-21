from world_creation import World
import sys

def print_tectonics_ascii(world):
    dimensions = world.dimensions
    unified_points = world.tectonics.unify_splits()
    for y in range(dimensions[1][0], dimensions[1][1]):
        print("|", end="")
        for x in range(dimensions[0][0], dimensions[0][1]):
            if (x,y) in unified_points.points.keys():
                print("#", end="")
            else:
                print(":", end="")
        print("\n", end="")
    for x in range(dimensions[0][0], dimensions[0][1]+1):
        print("_", end="")
    print("\n", end="")


dimensions = ((0, 50),(0, 50))

w = World(dimensions)

w.tectincs = Tectonics(dimensions)


w.prepare_tectonics(7, 5)

print_tectonics_ascii(w)

#for i in range(500):
#    w.tectonics.develop_splits()

while w.tectonics.develop_splits() == 0:
    continue

print_tectonics_ascii(w)
