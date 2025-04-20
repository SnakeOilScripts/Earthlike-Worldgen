from world_creation import *


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


def print_topography_rounded(topography:Topography):
    dimensions = topography.dimensions
    for y in range(dimensions[1][0], dimensions[1][1]):
        for x in range(dimensions[0][0], dimensions[0][1]):
            print(round(topography.topo_map.get_coordinate_value(x,y), 2), end='')
            print(' | ', end='')
        print("")


dimensions = ((0, 10),(0, 10))

tectonic_splits = TectonicSplits(dimensions, 0.001)
tectonic_splits.initialize_split((5,5), 10)
while tectonic_splits.develop_splits() == 0:
    continue

print_splitmap_ascii(tectonic_splits.split_map)

plates = TectonicPlates(dimensions)
plates.generate_from_splits(tectonic_splits.split_map)

print_coordinates_of_value(plates.plate_map, {0})
print_coordinates_of_value(plates.plate_map, {1})
print_coordinates_of_value(plates.plate_map, {0,1})

topography = Topography(dimensions)
magma_currents = MagmaCurrentMap(dimensions, topography.topo_map)
movements = TectonicMovements(magma_currents, plates, topography)

magma_vectors = magma_currents.generate_magma_current_vectors()
direction = plates.get_plate_direction(0, magma_vectors)

topography.topo_map.increment_coordinate_value(1,3, 100.0)
topography.topo_map.apply_changes()

movements.simulate_plate_movement()
print_topography_rounded(topography)