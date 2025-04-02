import random
import math
import sys
import numpy as np
import copy

random.seed()


#TODO:  1) general elevation levels (via plate tectonics) -> identify plate by randomly chosen point within it & vectors to all reachable points/closest neighbors
#          then simulate movement of plates by moving middle point & adjusting vectors
#       2) general erision to get classic foothill shapes (abstract wind&water) -> make map more detailed
#       3) add x units of water to every point, travel to lowest reachable point, simulate sea level and bodies of water with it
#       4) water cycle and river/lake formation
#       5) local climate, (ground type), humidity
#       6) local flora/fauna

# missing: mineral deposits?
#           read up on this here: geologyin.com


class World:

    def __init__(self, dimensions):
        self.dimensions = dimensions


class ObjectMap:

    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
        coordinates_list = [[base_object]*(dimensions[1][1] - dimensions[1][0])] * (dimensions[0][1] - dimensions[0][0])
        self.coordinates = np.array(coordinates_list)
    

    def coordinate_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])


    def get_adjacent_coordinates(self, x, y):
        return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]


    def get_adjacent_coordinates_within_dimensions(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1])]
    

    def get_coordinate_value(self, x, y):
        return self.coordinates[x,y]


class SplitMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, set())


    def add_coordinate_value(self, x, y, value):
        self.coordinates[x,y].add(value)


class VectorMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, (0,0))

    
    def set_coordinate_value(self, x, y, value):
        self.coordinates[x,y] = value


class Split:
    def __init__(self, shared_map:SplitMap, value):
        self.shared_map = shared_map
        self.value = value
        self.ends = set()


    def add_point(self, x, y):
        self.shared_map.add_coordinate_value(x, y, self.value)
    

    def add_end(self, x, y):
        self.ends.add((x,y))


    def extend_at_end(self, old_end, x, y):
        self.ends.remove(old_end)
        self.add_end(x, y)
        self.add_point(x, y)

    
    def add_center(self, x, y):
        self.center = (x,y)

    
    def get_center_distance(x, y):
        return math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))



class MagmaCurrentMap(Coordinates):
    # suction from subduction seems to be the strongest factor for plate movement, while magma currents explain the megacontinent-cycle
    def __init__(self, dimensions, base_surface:Coordinates):
        self.surface_map = copy.deepcopy(base_surface)
        super().__init__(dimensions)


    def generate_magma_current_vectors(self):
        vector_map = VectorMap(self.dimensions)
        for x in range(self.dimensions[0][1] - self.dimensions[0][0]):
            for y in range(self.dimensions[1][1] - self.dimensions[1][0]):
                neighbors = self.get_adjacent_coordinates_within_dimensions(x, y)
                neighbors.sort(key=lambda param: self.surface_map.get_coordinate_value(param[0],param[1]))
                if self.surface_map.get_coordinate_value(neighbors[0][0], neighbors[0][1]) < self.surface_map.get_coordinate_value(x,y):
                    vector_map.set_coordinate_value(x, y, (neighbors[0][0] - x, neighbors[0][1] - y))
                else:
                    vector_map.set_coordinate_value(x, y, (0,0))
        return vector_map


    def update_surface_map(self, new_map:Coordinates):
        self.surface_map = copy.deepcopy(new_map)


class SurfaceMap(Coordinates):
    # types of plate boundaries:
    # - convergent (without subduction) -> fold mountains
    # - convergent (with subduction) -> trench + mountains/volcanos
    # - divergent -> mid-ocean ridge / rift valleys, volcanism
    # - transform -> strike-slip-fault
    # https://www.geologyin.com/2014/03/types-of-continental-boundaries.html
    def apply_erosion(self):
        pass
    
