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


def print_coordinates_of_value(object_map, value):
    for y in range(object_map.dimensions[1][0], object_map.dimensions[1][1]):
        for x in range(object_map.dimensions[0][0], object_map.dimensions[0][1]):
            if object_map.get_coordinate_value(x, y) == value:
                print("#", end="")
            else:
                print(":", end="")
        print("")
    for x in range(object_map.dimensions[0][0], object_map.dimensions[0][1]):
        print("_", end="")
    print("")


dimensions = ((0, 50),(0, 50))

w = World(dimensions)
w.prepare_tectonics(15, 10)
#for split in w.tectonic_splits.splits:
#    print(split.ends)

#print_splitmap_ascii(w.tectonic_splits.split_map)
finished = 0

while finished == 0:
    finished = w.tectonic_splits.develop_splits()
    
print_splitmap_ascii(w.tectonic_splits.split_map)

split_map = w.tectonic_splits.split_map
"""
plates = TectonicPlates(dimensions)
plates.generate_from_splits(split_map)
print_coordinates_of_value(plates.plate_map, {0})
print_coordinates_of_value(plates.plate_map, {1})
print_coordinates_of_value(plates.plate_map, {0,1})
"""