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
    

    def prepare_tectonics(self, n_splits, min_distance):
        self.tectonic_splits = TectonicSplits(self.dimensions)
        for i in range(n_splits):
            self.tectonic_splits.add_initial_split(min_distance)


class ObjectMap:

    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
        coordinates_list = []
        for y in range(dimensions[1][0], dimensions[1][1]):
            x_list = []
            for x in range(dimensions[0][0], dimensions[0][1]):
                x_list.append(copy.deepcopy(base_object))
            coordinates_list.append(x_list)
        #coordinates_list = [[copy.deepcopy(base_object)]*(dimensions[1][1] - dimensions[1][0])] * (dimensions[0][1] - dimensions[0][0])
        self.coordinates = np.array(coordinates_list)
    

    def coordinate_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])


    def get_adjacent_coordinates(self, x, y):
        return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]


    def get_adjacent_coordinates_within_dimensions(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1])]
    

    def get_coordinate_value(self, x, y):
        return self.coordinates[x,y]
    

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))


class SplitMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, set())


    def add_coordinate_value(self, x, y, value):
        self.coordinates[x,y].add(value)
    

    def remove_coordinate_value(self, x, y, value):
        self.coordinates[x,y].remove(value)


    def get_adjacent_neighbors_of_value(self, x, y, value):
        return [c for c in self.get_adjacent_coordinates_within_dimensions(x, y) if value in self.get_coordinate_value(c[0], c[1])]


class VectorMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, (0,0))

    
    def set_coordinate_value(self, x, y, value):
        self.coordinates[x,y] = value


class Split:
    def __init__(self, shared_map:SplitMap, value):
        self.shared_map = shared_map
        self.value = value
        self.option_blacklist = set()
        self.ends = set()


    def add_point(self, x, y):
        self.shared_map.add_coordinate_value(x, y, self.value)
    

    def set_end(self, x, y):
        self.ends.add((x,y))


    def remove_end(self, x, y):
        if (x,y) in self.ends:
            self.ends.remove((x,y))
            return 1
        else:
            return -1


    def extend_at_end(self, old_end, x, y):
        if len(self.ends) == 2:
            self.ends.remove(old_end)
        self.set_end(x, y)
        self.add_point(x, y)

    
    def set_center(self, x, y):
        self.center = (x,y)


    def get_center(self):
        ends = list(self.ends)
        return (int((ends[0][0] - ends[1][0])/2), int((ends[0][1] - ends[1][1])/2))
    

    def get_center_distance(self, x, y):
        center = self.get_center()
        return math.sqrt(math.pow(x - center[0], 2) + math.pow(y - center[1], 2))


    def end_inactive(self, end):
        for n in self.shared_map.get_adjacent_coordinates(end[0], end[1]):
            if self.shared_map.coordinate_outside_dimensions(n[0], n[1]):
                return True
            if len(self.shared_map.get_coordinate_value(n[0], n[1])) != 0 and self.value not in self.shared_map.get_coordinate_value(n[0], n[1]):
                return True
        return False


    def get_active_ends(self):
        return [end for end in self.ends if not self.end_inactive(end)]


    def is_active(self):
        return len(self.get_active_ends()) > 0


    def get_neighbor(self, x, y):
        for n in self.shared_map.get_adjacent_coordinates_within_dimensions(x, y):
            if self.value in self.shared_map.get_coordinate_value(x, y):
                return n


    def backtrack_end(self, x, y):
        # the option choice guarantees that each end only has one neighbor in the same split
        previous_end = self.get_neighbor(x, y)
        self.remove_coordinate_value(x, y, self.value)
        self.remove_end(x, y)
        self.set_end(previous_end)
        self.option_blacklist.add((x,y))


class TectonicSplits:
    def __init__(self, dimensions, line_bias=0.7):
        self.dimensions = dimensions
        self.line_bias = line_bias
        self.split_map = SplitMap(dimensions)
        self.split_id = 0
        self.splits = []
    

    def initialize_split(self, center):
        new_split = Split(self.split_map, self.split_id)
        new_split.add_point(center[0], center[1])
        new_split.set_end(center[0], center[1])
        new_split.set_center(center[0], center[1])
        first_neighbor = random.choice(self.split_map.get_adjacent_coordinates_within_dimensions(center[0], center[1]))
        new_split.extend_at_end(center, first_neighbor[0], first_neighbor[1])
        self.splits.append(new_split)
        self.split_id += 1
    

    def add_initial_split(self, min_distance, max_attempts=100):
        for attempt in range(max_attempts):
            rejected = False
            new_center = (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), random.randint(self.dimensions[1][0], self.dimensions[1][1]-1))
            for s in self.splits:
                if s.get_center_distance(new_center[0], new_center[1]) < min_distance:
                    rejected = True
                    break
            if not rejected:
                self.initialize_split(new_center)
                break
    

    def get_active_splits(self):
        return [s for s in self.splits if s.is_active()]


    def develop_splits(self):
        active_splits = self.get_active_splits()
        if active_splits == []:
            return 1
        split = random.choice(active_splits)
        chosen_end = random.choice(split.get_active_ends())
        options = self.get_split_options(split, chosen_end) # options are artificially padded to fit the straight_bias
        if options == -1:
            return 0
        chosen_option = random.choice(options)
        split.extend_at_end(chosen_end, chosen_option[0], chosen_option[1])
        return 0


    def get_split_options(self, split, end):
        options = []
        for n in self.split_map.get_adjacent_coordinates_within_dimensions(end[0], end[1]):
            if len(self.split_map.get_adjacent_neighbors_of_value(n[0], n[1], split.value)) >= 2:
                # 90 degree angles & loopbacks are forbidden
                continue
            elif split.value in self.split_map.get_coordinate_value(n[0], n[1]):
                # no re-addings of existing coordinates
                continue
            elif n in split.option_blacklist:
                # guarantee that after backtracking, impossible points are not explored again
                continue
            options.append(n)
        
        if options == []:
            split.backtrack_end(end[0], end[1])
            return -1
        options.sort(key=lambda x: split.get_center_distance(x[0], x[1]), reverse=True)
        bias_options = options[0]
        bias_size = len(options[1:]) / (1 - self.line_bias) - len(options[1:])
        options += [bias_options] * int(bias_size)
        return options




class MagmaCurrentMap:
    # suction from subduction seems to be the strongest factor for plate movement, while magma currents explain the megacontinent-cycle
    def __init__(self, dimensions, base_surface:ObjectMap):
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


    def update_surface_map(self, new_map:ObjectMap):
        self.surface_map = copy.deepcopy(new_map)


class SurfaceMap:
    # types of plate boundaries:
    # - convergent (without subduction) -> fold mountains
    # - convergent (with subduction) -> trench + mountains/volcanos
    # - divergent -> mid-ocean ridge / rift valleys, volcanism
    # - transform -> strike-slip-fault
    # https://www.geologyin.com/2014/03/types-of-continental-boundaries.html
    def apply_erosion(self):
        pass
    
