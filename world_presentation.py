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
w.prepare_tectonics(30, 10, 100)
#for split in w.tectonic_splits.splits:
#    print(split.ends)

#print_splitmap_ascii(w.tectonic_splits.split_map)
finished = 0

while finished == 0:
    finished = w.tectonic_splits.develop_splits()
    
print_splitmap_ascii(w.tectonic_splits.split_map)
