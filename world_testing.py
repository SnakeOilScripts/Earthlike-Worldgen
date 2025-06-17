from world_creation import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pickle
import sys, time
import numpy as np

green_spectrum = colors.LinearSegmentedColormap.from_list("mycmap1", ["xkcd:light green", "xkcd:green"]).resampled(128)
brown_spectrum = colors.LinearSegmentedColormap.from_list("mycmap2", ["xkcd:pale yellow", "xkcd:tan", "xkcd:brown"]).resampled(128)
green_list = list(green_spectrum(range(128)))
brown_list = list(brown_spectrum(range(128)))
combination_list = green_list + brown_list
#print(combination_list, len(combination_list))

#sys.exit(0)
new_terrain = colors.ListedColormap(combination_list)
new_terrain.set_under("xkcd:cerulean")

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


def generate():
    #random.seed("plateau")
    random.seed("highland")
    #random.seed("flowergarden")

    #dimensions = ((0, 50),(0, 50))
    dimensions = ((0,100), (0,100))
    tectonic_splits = TectonicSplits(dimensions, 0.5)
    for i in range(20):
        tectonic_splits.add_initial_split(10)
    while tectonic_splits.develop_splits() == 0:
        continue
    print("splits finished")
    plates = TectonicPlates(dimensions)
    plates.generate_from_splits(tectonic_splits.split_map)
    topography = Topography(dimensions)
    magma_currents = MagmaCurrentMap(dimensions, topography.get_map())
    movements = TectonicMovements(magma_currents, plates, topography)
    magma_vectors = magma_currents.generate_magma_current_vectors()
    direction = plates.get_plate_direction(0, magma_vectors)
    topography.value_map.increment_coordinate_value(1,3, 100.0)
    topography.value_map.apply_changes()
    #for i in range(700):
    for i in range(30000):
        figname = f"plots/fig{i}"
        start = time.time()
        movements.simulate_plate_movement()
        stop = time.time()
        print(i, stop-start)
        #print_topography_rounded(topography)
        if i % 1000 == 0:
            sea_level = float(topography.get_sea_level())
            plt.imshow(topography.value_map.coordinates, cmap=new_terrain, interpolation='gaussian', vmin=sea_level)
            plt.savefig(figname)
            print(figname, stop-start)
        #plt.show()

def avg_height(topography:Topography):
    heights = np.copy(topography.value_map.coordinates)
    heights = heights.reshape(-1)
    return sum(heights)/len(heights)

#sea_level = float(topography.get_sea_level())
#plt.imshow(topography.topo_map.coordinates, cmap='terrain', interpolation='gaussian', vmin=sea_level)
#plt.imshow(topography.value_map.coordinates, cmap='terrain', vmin=sea_level)
#plt.savefig("plots/continents.png")

#save_object(topography, "topography.pickle")
topography = load_object("topography.pickle")
print(avg_height(topography))

for i in range(4):

    topography.expand_dimensions_transitional_gaussian(2)
    #print(avg_height(topography))

    sea_level = float(topography.get_sea_level())
    #print("\t", sea_level)
    plt.imshow(topography.value_map.coordinates, cmap=new_terrain, vmin=sea_level)
    plt.savefig(f"plots/continents_gaussian{i}.png")
