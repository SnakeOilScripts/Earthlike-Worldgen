from world_creation import *
import sys

def print_splitmap_ascii(split_map):
    for y in range(split_map.dimensions[1][0], split_map.dimensions[1][1]):
        for x in range(split_map.dimensions[0][0], split_map.dimensions[0][1]):
            if len(split_map.get_coordinate_value(x, y)) > 0:
                print("#", end="")
            else:
                print(":", end="")
        print("")
    for x in range(split_map.dimensions[0][0], split_map.dimensions[0][1]):
        print("_", end="")
    print("")
    


dimensions = ((0, 500),(0, 500))

w = World(dimensions)
w.prepare_tectonics(10, 30)

#print_splitmap_ascii(w.tectonic_splits.split_map)

while w.tectonic_splits.develop_splits() == 0:
    continue

#print_splitmap_ascii(w.tectonic_splits.split_map)
