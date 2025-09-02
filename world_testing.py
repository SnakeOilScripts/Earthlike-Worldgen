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


def save_object(object, filename):
    with open(filename, "wb") as fp:
        pickle.dump(object, fp)


def load_object(filename):
    with open(filename, "rb") as fp:
        o = pickle.load(fp)
    return o


def initialize_world(seed, dimensions, n_splits, split_distance):
    random.seed(seed)
    tectonic_splits = TectonicSplits(dimensions, 0.5)
    for i in range(n_splits):
        tectonic_splits.add_initial_split(split_distance)
    while tectonic_splits.develop_splits() == 0:
        continue
    print("splits finished")
    return tectonic_splits


def generate(dimensions, tectonic_splits):
    plates = TectonicPlates(dimensions)
    plates.generate_from_splits(tectonic_splits.split_map)
    geology = Geology(dimensions)
    magma_currents = MagmaCurrentMap(dimensions, geology)
    movements = TectonicMovements(magma_currents, plates, geology)
    geology.value_map.increment_coordinate_value(1,3,{"igneous":100.0})
    geology.value_map.apply_changes()
    for i in range(1000):
        figname = f"plots/fig{i}"
        start = time.time()
        movements.simulate_plate_movement()
        stop = time.time()
        print(i, stop-start)
        if i % 1000 == 0:
            visualize_geology_terrain(geology, figname)
            print(figname, stop-start)
    return geology

def avg_height(coordinates):
    heights = np.copy(coordinates)
    heights = heights.reshape(-1)
    return sum(heights)/len(heights)

def visualize_geology_terrain(geology, figname):
    sea_level = float(geology.get_sea_level())
    plt.imshow(geology.generate_topography(), cmap=new_terrain, interpolation="gaussian", vmin=sea_level)
    plt.savefig(figname+"_geoterrain")

def visualize_geology_rocks(geology, figname):
    fig, ax = plt.subplots(ncols=7)
    felsic_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:red"])
    ax[0].imshow(geology.get_single_attribute_value_map("felsic"), cmap=felsic_map, interpolation='gaussian')
    intermediate_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:brown"])
    ax[1].imshow(geology.get_single_attribute_value_map("intermediate"), cmap=intermediate_map, interpolation='gaussian')
    mafic_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:gray"])
    ax[2].imshow(geology.get_single_attribute_value_map("mafic"), cmap=mafic_map, interpolation='gaussian')
    ultramafic_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:green"])
    ax[3].imshow(geology.get_single_attribute_value_map("ultramafic"), cmap=ultramafic_map, interpolation='gaussian')
    igneous_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:cyan"])
    ax[4].imshow(geology.get_single_attribute_value_map("igneous"), cmap=igneous_map, interpolation='gaussian')
    sedimentary_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:orange"])
    ax[5].imshow(geology.get_single_attribute_value_map("sedimentary"), cmap=sedimentary_map, interpolation='gaussian')
    metamorphic_map = colors.LinearSegmentedColormap.from_list("mycmap1", ["white", "tab:pink"])
    ax[6].imshow(geology.get_single_attribute_value_map("metamorphic"), cmap=metamorphic_map, interpolation='gaussian')
    plt.savefig(figname+"_rocktypes")


dimensions = ((0,100),(0,100))
splits = initialize_world("ernalia", dimensions, 20, 20)
geology = generate(dimensions, splits)


for i in range(4):
    geology.expand_dimensions_transitional_gaussian(2)
    sea_level = float(geology.get_sea_level())
    plt.imshow(geology.generate_topography(), cmap=new_terrain, vmin=sea_level)
    plt.savefig(f"plots/continents_gaussian{i}.png")
