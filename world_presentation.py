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
    


dimensions = ((0, 100),(0, 100))

w = World(dimensions)
w.prepare_tectonics(10, 30)

print_splitmap_ascii(w.tectonic_splits.split_map)
finished = 0

while finished == 0:
    try:
        finished = w.tectonic_splits.develop_splits()
    except:
        print_splitmap_ascii(w.tectonic_splits.split_map)
        active_splits = w.tectonic_splits.get_active_splits()
        for end in active_splits[0].get_active_ends():
            print(end)
            for n in w.tectonic_splits.split_map.get_adjacent_coordinates_within_dimensions(end[0], end[1]):
                print("\t", n, w.tectonic_splits.split_map.get_coordinate_value(n[0], n[1]))
            print(w.tectonic_splits.get_split_options(active_splits[0], end))
        print("failed")
        break

print_splitmap_ascii(w.tectonic_splits.split_map)
