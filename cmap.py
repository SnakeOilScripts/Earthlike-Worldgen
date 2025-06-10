import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import sys
import pickle
import time

def save_object(object, filename):
    with open(filename, "wb") as fp:
        pickle.dump(object, fp)


def load_object(filename):
    with open(filename, "rb") as fp:
        o = pickle.load(fp)
    return o

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

color_list = [ "xkcd:green", "xkcd:pale yellow", "xkcd:tan", "xkcd:brown"]

cmap1 = colors.LinearSegmentedColormap.from_list("mycmap", color_list)
green_spectrum = colors.LinearSegmentedColormap.from_list("mycmap1", ["xkcd:light green", "xkcd:green"]).resampled(128)
brown_spectrum = colors.LinearSegmentedColormap.from_list("mycmap2", ["xkcd:pale yellow", "xkcd:tan", "xkcd:brown"]).resampled(128)
green_list = list(green_spectrum(range(128)))
brown_list = list(brown_spectrum(range(128)))
combination_list = green_list + brown_list
#print(combination_list, len(combination_list))

#sys.exit(0)
combined_cmap = colors.ListedColormap(combination_list)
combined_cmap.set_under("xkcd:cerulean")

#arr = np.linspace(0, 10, 100).reshape((10, 10))
#fig, ax = plt.subplots(ncols=2)

#cmap = plt.get_cmap('terrain')
#new_cmap = truncate_colormap(cmap, 0.25, 1.0)
#new_cmap.set_under("blue")
#new_cmap.set_clim(20, 80)
#ax[0].imshow(arr, interpolation='nearest', cmap=cmap)
#ax[1].imshow(arr, interpolation='nearest', cmap=cmap1)
#plt.savefig("cmap.png")

topography = load_object("topography.pickle")
#print(topography.get_sea_level())

#sea_level = topography.get_sea_level()
for i in range(1):
    topography.expand_dimensions_transitional_gaussian(2)
    
sea_level = topography.get_sea_level()
print(sea_level)

plt.imshow(topography.value_map.coordinates, cmap=combined_cmap, vmin=sea_level)
plt.savefig("cmap_terrain.png")
#print(sea_level)