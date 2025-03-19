from world_creation import World
import sys

def print_tectonics_ascii(world):
    dimensions = world.dimensions
    for y in range(dimensions[1][0], dimensions[1][1]):
        print("|", end="")
        for x in range(dimensions[0][0], dimensions[0][1]):
            if (x,y) in world.tectonics.points.keys():
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")
    for x in range(dimensions[0][0], dimensions[0][1]+1):
        print("_", end="")
    print("\n", end="")


dimensions = ((0, 50),(0, 50))

w = World(dimensions)
w.prepare_tectonics(10, 5)

print_tectonics_ascii(w)

while w.tectonics.develop_breaks() == 0:
    continue

print_tectonics_ascii(w)
