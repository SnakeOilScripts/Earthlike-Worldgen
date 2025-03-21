from world_creation import World
import sys

def print_tectonics_ascii(world):
    dimensions = world.dimensions
    unified_points = world.tectonics.unify_splits()
    for y in range(dimensions[1][0], dimensions[1][1]):
        print("|", end="")
        for x in range(dimensions[0][0], dimensions[0][1]):
            if (x,y) in unified_points.points.keys():
                print(unified_points.points[(x,y)], end="")
            else:
                print(":", end="")
        print("\n", end="")
    for x in range(dimensions[0][0], dimensions[0][1]+1):
        print("_", end="")
    print("\n", end="")


dimensions = ((0, 50),(0, 50))

w = World(dimensions)
w.prepare_tectonics(4, 10)

print_tectonics_ascii(w)


while w.tectonics.develop_splits() == 0:
    continue

print_tectonics_ascii(w)

w.tectonics.activate_unfinished_splits()
w.tectonics.distance_irrelevant()

while w.tectonics.develop_splits() == 0:
    continue

print_tectonics_ascii(w)

w.tectonics.activate_unfinished_splits()
w.tectonics.allow_circles()

while w.tectonics.develop_splits() == 0:
    continue

print_tectonics_ascii(w)

for split in w.tectonics.splits:
    print(split.value, split.distance_irrelevant, split.circles_allowed)