from world_creation import *
import matplotlib.pyplot as plt
import pickle
import sys, time


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


def save_object(object, filename):
    with open(filename, "wb") as fp:
        pickle.dump(object, fp)


def load_object(filename):
    with open(filename, "rb") as fp:
        o = pickle.load(fp)
    return o



random.seed("coinage")
#random.seed("flowergarden")


#dimensions = ((0, 50),(0, 50))
dimensions = ((0,100), (0,100))

tectonic_splits = TectonicSplits(dimensions, 0.5)
for i in range(10):
    tectonic_splits.add_initial_split(10)
while tectonic_splits.develop_splits() == 0:
    continue

print("splits finished")

#tectonic_splits = load_object("splits.pickle")
#print_splitmap_ascii(tectonic_splits.split_map)
#save_object(tectonic_splits, "splits.pickle")

#sys.exit(0)

plates = TectonicPlates(dimensions)
plates.generate_from_splits(tectonic_splits.split_map)

topography = Topography(dimensions)
magma_currents = MagmaCurrentMap(dimensions, topography.get_map())
movements = TectonicMovements(magma_currents, plates, topography)

magma_vectors = magma_currents.generate_magma_current_vectors()
direction = plates.get_plate_direction(0, magma_vectors)

topography.value_map.increment_coordinate_value(1,3, 100.0)
topography.value_map.apply_changes()

#movements.apply_vector_to_plate((3,-21), 3)
#plt.imshow(topography.topo_map.coordinates, cmap='terrain', interpolation='gaussian', vmin=-500, vmax=1000)
#plt.savefig("test.png")




#for i in range(700):
for i in range(1400):
    #figname = f"plots/fig{i}"
    start = time.time()
    movements.simulate_plate_movement()
    stop = time.time()
    print(i, stop-start)
    #print_topography_rounded(topography)
    #if i % 100 == 0:
        #plt.imshow(topography.topo_map.coordinates, cmap='terrain', interpolation='gaussian', vmin=0, vmax=600)
        #plt.savefig(figname)
        #print(figname, stop-start)
    #plt.show()

sea_level = float(topography.get_sea_level(0.2))
#plt.imshow(topography.topo_map.coordinates, cmap='terrain', interpolation='gaussian', vmin=sea_level)
plt.imshow(topography.value_map.coordinates, cmap='terrain', vmin=sea_level)
plt.savefig("plots/continents.png")

for i in range(4):

    topography.expand_dimensions_transitional_gaussian(2)


    sea_level = float(topography.get_sea_level(0.2))
    plt.imshow(topography.value_map.coordinates, cmap='terrain', vmin=sea_level)
    plt.savefig(f"plots/continents_gaussian{i}.png")
