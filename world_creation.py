import random
import math
import sys
import numpy as np
import copy
from scipy import stats

#random.seed()


#TODO:  
#       2) general erosion to get classic foothill shapes (abstract wind&water) -> make map more detailed
#       3) add x units of water to every point, travel to lowest reachable point, simulate sea level and bodies of water with it
#       4) water cycle and river/lake formation
#       5) local climate, (ground type), humidity
#       6) local flora/fauna

# missing: mineral deposits?
#           read up on this here: geologyin.com



class ObjectMap:

    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
        self.base_object = base_object
        self.coordinates = self.create_coordinates(dimensions, base_object) 


    def create_coordinates(self, dimensions, base_object):
        coordinates_list = []
        for y in range(dimensions[1][0], dimensions[1][1]):
            x_list = []
            for x in range(dimensions[0][0], dimensions[0][1]):
                x_list.append(copy.deepcopy(base_object))
            coordinates_list.append(x_list)
        coordinates = np.array(coordinates_list)
        return coordinates


    def get_all_coordinates(self):
        coordinates = []
        for x in range(self.dimensions[0][0], self.dimensions[0][1]):
            for y in range(self.dimensions[1][0], self.dimensions[1][1]):
                coordinates.append((x,y))
        return coordinates


    def coordinate_outside_dimensions(self, x, y, dimensions=None):
        if dimensions is None:
            dimensions = self.dimensions
        return (x < dimensions[0][0] or x >= dimensions[0][1] or y < dimensions[1][0] or y >= dimensions[1][1])


    def get_adjacent_coordinates(self, x, y):
        return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]


    def get_adjacent_nondiagonal_coordinates(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if c[0] == x or c[1] == y]


    def get_adjacent_coordinates_within_dimensions(self, x, y, dimensions=None):
        if dimensions is None:
            dimensions = self.dimensions
        return [c for c in self.get_adjacent_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1], dimensions)]

    
    def get_adjacent_nondiagonal_coordinates_within_dimensions(self, x, y, dimensions=None):
        if dimensions is None:
            dimensions = self.dimensions
        return [c for c in self.get_adjacent_nondiagonal_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1], dimensions)]
    

    def get_coordinate_value(self, x, y):
        if self.coordinate_outside_dimensions(x, y):
            return None
        return self.coordinates[x,y]


    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
    

    # for a point, assume it is a vector from (0,0) to x,y and calculate the angle between two such vectors
    def base_vector_angle(self, x1, y1, x2, y2):
        l1 = self.get_distance(0,0,x1,y1)
        l2 = self.get_distance(0,0,x2,y2)
        dot_product = x1*x2 + y1*y2
        angle = math.acos(round((dot_product) / (l1 * l2), 2))
        return angle
    

    def resize_vector(self, x, y, length):
        if self.get_distance(0,0,x,y) == 0:
            return (0,0)
        return (x * (length / self.get_distance(0, 0, x, y)), y * (length / self.get_distance(0, 0, x, y)))


    def standardize_vector(self, x, y):
        if x == 0 and y != 0:
            return (0, y/abs(y))
        elif x != 0 and y == 0:
            return (x/abs(x), y)
        elif x == 0 and y == 0:
            return (0,0)
        elif abs(x) > abs(y):
            return (x/abs(x), y/abs(x))
        else:
            return (x/abs(y), y/abs(y))
    

    def get_expanded_dimensions(self, expansion_factor):
        return ((self.dimensions[0][0], self.dimensions[0][1]*expansion_factor), (self.dimensions[1][0], self.dimensions[1][1]*expansion_factor))


    def dimension_expansion(self, expansion_factor):
        # a square of expansion_factor * expansion_factor points will inherit the value of a single coordinate from the old coordinates
        expanded_dimensions = self.get_expanded_dimensions(expansion_factor)
        new_coordinates = self.create_coordinates(expanded_dimensions, self.base_object)
        for coordinate in self.get_all_coordinates():
            for x in range(coordinate[0]*expansion_factor, (coordinate[0]+1)*expansion_factor):
                for y in range(coordinate[1]*expansion_factor, (coordinate[1]+1)*expansion_factor):
                    new_coordinates[x,y] = self.get_coordinate_value(coordinate[0], coordinate[1])
        self.coordinates = new_coordinates
        self.dimensions = expanded_dimensions


    def fill_gaussian_coordinate(self, x, y, xlocal, ylocal, maximum_value, xmean, ymean, standard_deviation):
        if not self.coordinate_outside_dimensions(x,y):
            self.coordinates[x,y] = maximum_value * (stats.norm.pdf(xlocal+1, xmean, standard_deviation) + stats.norm.pdf(ylocal+1, ymean, standard_deviation))
        else:
            return -1


    def fill_gaussian_square(self, xstart, ystart, length, maximum_value, xmean, ymean, standard_deviation):
        # creates a normal distribution along the x and the y axis with maximum_value as constant factor, 
        # length/6 as standard deviation (edges are 3rd standard deviation and near 0)
        # and x + length/2 or y + length/2 as mean
        for x in range(xstart, xstart+length):
            for y in range(ystart, ystart+length):
                self.fill_gaussian_coordinate(x, y, x, y, maximum_value, xmean, ymean, standard_deviation)


    def gaussian_dimension_expansion(self, expansion_factor):
        expanded_dimensions = self.get_expanded_dimensions(expansion_factor)
        old_coordinates = np.copy(self.coordinates)
        self.coordinates = self.create_coordinates(expanded_dimensions, self.base_object)
        for coordinate in self.get_all_coordinates():
            maximum_value = old_coordinates[coordinate[0],coordinate[1]]
            xmean = coordinate[0]*expansion_factor + (expansion_factor+1)/2
            ymean = coordinate[1]*expansion_factor + (expansion_factor+1)/2
            standard_deviation = expansion_factor/6
            self.fill_gaussian_square(coordinate[0]*expansion_factor, coordinate[1]*expansion_factor, expansion_factor, maximum_value, xmean, ymean, standard_deviation)
        self.dimensions = expanded_dimensions


class UpdateMap(ObjectMap):
    
    
    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
        self.update_dimensions = dimensions
        self.base_object = base_object
        self.coordinates = self.create_coordinates(dimensions, base_object)
        self.coordinates_update = np.copy(self.coordinates)

    
    def increment_coordinate_value(self, x, y, value):
        if not self.coordinate_outside_dimensions(x, y, self.update_dimensions):
            self.coordinates_update[x,y] += value
        else:
            return -1


    def apply_changes(self):
        self.coordinates = self.coordinates_update
        self.coordinates_update = np.copy(self.coordinates)
        self.dimensions = self.update_dimensions

    
    def dimension_expansion(self, expansion_factor):
        super().dimension_expansion(expansion_factor)
        self.coordinates_update = np.copy(self.coordinates)


    def gaussian_dimension_expansion(self, expansion_factor):
        super().gaussian_dimension_expansion(expansion_factor)
        self.coordinates_update = np.copy(self.coordinates)
    

    def transitional_gaussian_dimension_expansion(self, expansion_factor):
        standard_deviation = expansion_factor/2
        dp_array = np.full((expansion_factor*3, expansion_factor*3), 0.0)
        for x in range(expansion_factor*3):
            for y in range(expansion_factor*3):
                dp_array[x,y] = stats.norm.pdf(x+1, expansion_factor + (expansion_factor+1)/2, standard_deviation) + stats.norm.pdf(y+1, expansion_factor + (expansion_factor+1)/2, standard_deviation)
        self.update_dimensions = self.get_expanded_dimensions(expansion_factor)
        self.coordinates_update = self.create_coordinates(self.update_dimensions, self.base_object)
        for coordinate in self.get_all_coordinates():
            multiplier = self.get_coordinate_value(coordinate[0], coordinate[1])
            for x in range(expansion_factor*3):
                for y in range(expansion_factor*3):
                    self.increment_coordinate_value((coordinate[0]-1)*expansion_factor + x, (coordinate[1]-1)*expansion_factor + y, dp_array[x,y]*multiplier)
        self.apply_changes()



class UpdateDictMap(UpdateMap):

    def __init__(self, dimensions, base_object:dict):
        super().__ini__(dimensions, base_object)

    
    def increment_coordinate_value(self, x, y, values):
        for key in values:
            self.coordinates_update[x,y][key] += values[key]


    def fill_gaussian_coordinate(self, x, y, xlocal, ylocal, maximum_values, xmean, ymean, standard_deviation):
        for key in maximum_values:
            value = maximum_values[key] * (stats.norm.pdf(xlocal+1, xmean, standard_deviation) + stats.norm.pdf(ylocal+1, ymean, standard_deviation))
            self.increment_coordinate_value(x, y, {key:value})


class SetMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, set())


    def add_coordinate_value(self, x, y, value):
        self.coordinates[x,y].add(value)
    

    def update_coordinate_value(self, x, y, values:set):
        self.coordinates[x,y].update(values)
    

    def remove_coordinate_value(self, x, y, value):
        self.coordinates[x,y].remove(value)


    def get_adjacent_neighbors_of_value(self, x, y, value):
        return [c for c in self.get_adjacent_coordinates_within_dimensions(x, y) if value in self.get_coordinate_value(c[0], c[1])]

    
    def get_all_coordinates_containing_value(self, value):
        coordinates = []
        for y in range(self.dimensions[1][0], self.dimensions[1][1]):
            for x in range(self.dimensions[0][0], self.dimensions[0][1]):
                if value in self.get_coordinate_value(x, y):
                    coordinates.append((x,y))
        return coordinates


class VectorMap(ObjectMap):
    def __init__(self, dimensions):
        super().__init__(dimensions, (0,0))

    
    def set_coordinate_value(self, x, y, value):
        self.coordinates[x,y] = value


# TODO: move ends back to set instead of dict
class Split:
    def __init__(self, shared_map:SetMap, value):
        self.shared_map = shared_map
        self.value = value
        self.option_blacklist = set()
        self.ends = dict()


    def add_point(self, x, y):
        self.shared_map.add_coordinate_value(x, y, self.value)
    

    def set_end(self, x, y):
        self.ends[(x,y)] = 1
    

    def get_end_goal(self, end):
        if end in self.ends:
            return self.ends[end]
        else:
            return None


    def remove_end(self, end):
        if end in self.ends:
            del self.ends[end]
            return 1
        else:
            return -1


    def extend_at_end(self, old_end, x, y):
        self.remove_end(old_end)
        self.set_end(x, y)
        self.add_point(x, y)


    def get_end_goal_distance(self, end, x, y):
        goal = self.get_end_goal(end)
        if goal is not None:
            return self.shared_map.get_distance(goal[0], goal[1], x, y)
        else:
            return -1


    def get_center(self):
        ends = list(self.ends)
        vector = (int((ends[0][0] - ends[1][0])/2), int((ends[0][1] - ends[1][1])/2))
        return (ends[0][0]+vector[0], ends[0][1]+vector[1])


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


    def get_end_neighbor(self, x, y):
        for n in self.shared_map.get_adjacent_coordinates_within_dimensions(x, y):
            if self.value in self.shared_map.get_coordinate_value(n[0], n[1]):
                return n


    def get_nth_end_neighbor(self, end, n):
        known_neighbors = set()
        neighbor = end
        for i in range(n):
            known_neighbors.add(neighbor)
            candidates = self.shared_map.get_adjacent_neighbors_of_value(neighbor[0], neighbor[1], self.value)
            for candidate in candidates:
                if candidate not in known_neighbors:
                    neighbor = candidate
        return neighbor


    def get_end_direction(self, end, n):
        nth_neighbor = self.get_nth_end_neighbor(end, n)
        vector = (end[0]-nth_neighbor[0], end[1]-nth_neighbor[1])

    
    # assuming there exists a vector between the end and its nth neighbor, for (x,y) calculate the angle between nth-neighbir->end and nth-neighbor->(x,y)
    def angle_towards_nth_end_neighbor(self, end, n, x, y):
        nth_neighbor = self.get_nth_end_neighbor(end, n)
        end_vector = (end[0]-nth_neighbor[0], end[1]-nth_neighbor[1])
        angled_vector = (x-nth_neighbor[0], y-nth_neighbor[1])
        return self.shared_map.base_vector_angle(end_vector[0], end_vector[1], angled_vector[0], angled_vector[1])


    def is_active(self):
        return len(self.get_active_ends()) > 0


    def get_other_end(self, end):
        ends = list(self.ends)
        if end == ends[0]:
            return ends[1]
        elif end == ends[1]:
            return ends[0]
        else:
            return -1


    def backtrack_end(self, x, y):
        # the option choice guarantees that each end only has one neighbor in the same split
        previous_end = self.get_end_neighbor(x, y)
        self.shared_map.remove_coordinate_value(x, y, self.value)
        self.remove_end((x, y))
        self.set_end(previous_end[0], previous_end[1])
        self.option_blacklist.add((x,y))


class TectonicSplits:
    def __init__(self, dimensions, direction_change_rate=0.25, direction_calc_n=8):
        self.dimensions = dimensions
        self.direction_change_rate = direction_change_rate
        self.direction_calc_n = direction_calc_n
        self.split_map = SetMap(dimensions)
        self.split_id = 0
        self.splits = []
    

    def initialize_split(self, base, max_attempts):
        new_split = Split(self.split_map, self.split_id)
        new_split.add_point(base[0], base[1])
        new_split.set_end(base[0], base[1])
        first_neighbor = random.choice(self.split_map.get_adjacent_coordinates_within_dimensions(base[0], base[1]))
        new_split.add_point(first_neighbor[0], first_neighbor[1])
        new_split.set_end(first_neighbor[0], first_neighbor[1])
        self.splits.append(new_split)
        self.split_id += 1
    

    def add_initial_split(self, min_split_distance, max_attempts=100):
        for attempt in range(max_attempts):
            rejected = False
            new_center = (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), random.randint(self.dimensions[1][0], self.dimensions[1][1]-1))
            for s in self.splits:
                if s.get_center_distance(new_center[0], new_center[1]) < min_split_distance:
                    rejected = True
                    break
            if not rejected:
                self.initialize_split(new_center, max_attempts)
                break
    

    def get_active_splits(self):
        return [s for s in self.splits if s.is_active()]


    def develop_splits(self):
        active_splits = self.get_active_splits()
        if active_splits == []:
            return 1
        split = random.choice(active_splits)
        chosen_end = random.choice(split.get_active_ends())
        options = self.get_split_options(split, chosen_end) # options are artificially padded to fit the direction_change_rate
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
        options.sort(key=lambda x: split.angle_towards_nth_end_neighbor(end, self.direction_calc_n, x[0], x[1]))
        bias_option = options[0]
        direction_change_options = options[1:]
        if len(direction_change_options) > 0:
            option_length = int(len(direction_change_options) / self.direction_change_rate)
            options = direction_change_options + [bias_option] * (option_length - len(direction_change_options))
        return options


class TectonicPlates:
    
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.plate_map = SetMap(dimensions)
        self.plate_id = 0
    

    def generate_from_splits(self, split_map:SetMap):
        for y in range(self.dimensions[1][0], self.dimensions[1][1]):
            for x in range(self.dimensions[0][0], self.dimensions[0][1]):
                if len(split_map.get_coordinate_value(x,y)) > 0:
                    continue
                if len(self.plate_map.get_coordinate_value(x,y)) == 0:
                    self.spread_value_within_boundary(split_map, self.plate_id, x, y)
                    self.plate_id += 1
        self.fill_plate_boundaries()


    def fill_plate_boundaries(self):
        for y in range(self.dimensions[1][0], self.dimensions[1][1]):
            for x in range(self.dimensions[0][0], self.dimensions[0][1]):
                if len(self.plate_map.get_coordinate_value(x,y)) == 0:
                    self.plate_map.update_coordinate_value(x,y,self.get_all_neighbor_values(x,y))
        return

    
    def spread_value_within_boundary(self, split_map:SetMap, value, x, y):
        # x,y is the first point where the spreading starts
        next_round = {(x,y)}
        while len(next_round) > 0:
            neighbors = set()
            for c in next_round:
                self.plate_map.add_coordinate_value(c[0], c[1], value)
                spreadable_neighbors = [n for n in self.plate_map.get_adjacent_nondiagonal_coordinates_within_dimensions(c[0], c[1])
                                            if len(split_map.get_coordinate_value(n[0],n[1])) == 0 and      # coordinate is not a split
                                            len(self.plate_map.get_coordinate_value(n[0], n[1])) == 0    # coordinate is not already filled
                                        ]
                neighbors.update(spreadable_neighbors)
            next_round = neighbors
    

    def get_all_neighbor_values(self, x, y):
        values = set()
        for n in self.plate_map.get_adjacent_coordinates_within_dimensions(x, y):
            values.update(self.plate_map.get_coordinate_value(n[0],n[1]))
        return values
    

    # the direction vector should have one coordinate of value 1 (either x or y), because angles will not work in this scenario
    def get_plate_direction(self, plate_id:int, magma_vectors:VectorMap):
        vectors = []
        for x in range(self.dimensions[0][0], self.dimensions[0][1]):
            for y in range(self.dimensions[1][0], self.dimensions[1][1]):
                if plate_id in self.plate_map.get_coordinate_value(x,y):
                    vectors.append(magma_vectors.get_coordinate_value(x,y))
        sum_vector = (int(sum([v[0] for v in vectors])), int(sum([v[1] for v in vectors])))
        return sum_vector
    

    def get_coordinate_value(self, x, y):
        return self.plate_map.get_coordinate_value(x,y)
    


# TODO: double-check that this works with the new ObjectMap class
class MagmaCurrentMap:
    # suction from subduction seems to be the strongest factor for plate movement, while magma currents explain the megacontinent-cycle
    def __init__(self, dimensions, base_surface:ObjectMap):
        self.surface_map = base_surface
        self.dimensions = dimensions


    def generate_magma_current_vectors(self):
        vector_map = VectorMap(self.dimensions)
        for x in range(self.dimensions[0][0], self.dimensions[0][1]):
            for y in range(self.dimensions[1][0], self.dimensions[1][1]):
                neighbors = self.surface_map.get_adjacent_coordinates_within_dimensions(x, y)
                neighbors.sort(key=lambda param: self.surface_map.get_coordinate_value(param[0],param[1]))
                if self.surface_map.get_coordinate_value(neighbors[0][0], neighbors[0][1]) < self.surface_map.get_coordinate_value(x,y):
                    vector_map.set_coordinate_value(x, y, (neighbors[0][0] - x, neighbors[0][1] - y))
                else:
                    vector_map.set_coordinate_value(x, y, (0,0))
        return vector_map


    def update_surface_map(self, new_map:ObjectMap):
        self.surface_map = copy.deepcopy(new_map)


class TectonicDomain:
    def __init__(self, dimensions, base_unit):
        self.dimensions = dimensions
        self.base_unit = base_unit
        self.value_map = UpdateMap(self.dimensions, base_unit)
    

    def apply_volcanism(self, x, y):
        volcanism_potency = 3
        self.value_map.increment_coordinate_value(x, y, self.base_unit * volcanism_potency)


    def get_transfer_unit(self, value, ratio):
        return value * ratio


    def get_map(self):
        return self.value_map


    def apply_changes(self):
        self.value_map.apply_changes()


    # TODO: make this base class fitting for both Topography and Geology
    def point_interaction(self, x1, y1, x2, y2, mode, ratio):
        # point_interaction must check if the coordinate is within dimensions because of how the interaction calculation works
        # having the plate boundary occupying a coordinate breaks all systems I could come up with, here is the new plan:
        #   - for a coordinate with more than one plate_id in it, it belongs to the plate of the lowest plate_id
        #   - the ACTUAL plate boundary is a line of thickness 0 between two coordinates
        transfer_unit = round(self.get_transfer_unit(self.value_map.get_coordinate_value(x1, y1), ratio), 2)
        if self.value_map.coordinate_outside_dimensions(x2, y2):
            # if the interaction_point is out of dimensions, just remove the units to the transferred
            self.falloff_interaction(x1, y1, transfer_unit)
        elif mode == 'transfer':
            self.transfer_interaction(x1, y1, x2, y2, transfer_unit)
        elif mode == 'transform':
            self.transform_interaction(x1, y1, x2, y2, transfer_unit, ratio)
        elif mode == 'divergent':
            self.divergent_interaction(x1, y1, x2, y2, transfer_unit, ratio)
        elif mode == 'convergent':
            self.convergent_interaction(x1, y1, x2, y2, transfer_unit, ratio)
        elif mode == 'subduction':
            self.subduction_interaction(x1, y1, x2, y2, transfer_unit, ratio)
        return
    

    def falloff_interaction(self, x1, y1, transfer_unit):
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, -1))


    def transfer_interaction(self, x1, y1, x2, y2, transfer_unit):
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, -1))
        self.value_map.increment_coordinate_value(x2, y2, transfer_unit)


    def transform_interaction(self, x1, y1, x2, y2, transfer_unit, ratio):
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, -1))
        self.value_map.increment_coordinate_value(x2, y2, transfer_unit)


    def divergent_interaction(self, x1, y1, x2, y2, transfer_unit, ratio):
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, -1))
        self.value_map.increment_coordinate_value(x2, y2, transfer_unit)
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(self.base_unit, ratio))


    def convergent_interaction(self, x1, y1, x2, y2, transfer_unit, ratio):
        # the convergent coordinate will receive units from behind
        # give back fold_ratio * transfer_unit back to where it would come from
        reverse_neighbor = (x2-x1*(-1), y2-y1*(-1))
        fold_ratio = 0.5
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, fold_ratio * -1))
        self.value_map.increment_coordinate_value(reverse_neighbor[0], reverse_neighbor[1], self.get_transfer_unit(transfer_unit, fold_ratio))


    def subduction_interaction(self, x1, y1, x2, y2, transfer_unit, ratio):
        subduction_ratio = 0.5
        self.value_map.increment_coordinate_value(x1, y1, self.get_transfer_unit(transfer_unit, -1 - subduction_ratio))   # create trenches by creating less than 0 values
        self.value_map.increment_coordinate_value(x2, y2, self.get_transfer_unit(transfer_unit, subduction_ratio))


# TODO: implement, duh
class Topography(TectonicDomain):
    # types of plate boundaries:
    # - convergent (without subduction) -> fold mountains
    # - convergent (with subduction) -> trench + mountains/volcanos
    # - divergent -> mid-ocean ridge / rift valleys, volcanism
    # - transform -> strike-slip-fault
    # - volcanism
    # https://www.geologyin.com/2014/03/types-of-continental-boundaries.html
    def __init__(self, dimensions, base_height=100.0):
        self.dimensions = dimensions
        self.base_unit = base_height
        self.value_map = UpdateMap(self.dimensions, self.base_unit)
        

    def apply_volcanism(self, x, y):
        volcanism_potency = 3
        self.value_map.increment_coordinate_value(x, y, self.base_unit * volcanism_potency)

    
    def get_height(self, x, y):
        return self.value_map.get_coordinate_value(x, y)


    def apply_changes(self):
        self.value_map.apply_changes()


    def get_sea_level(self, coverage):
        # assuming coverage % of the world are covered in water, what is the corresponding sea level (i.e. the n-median)?
        b = np.copy(self.value_map.coordinates)
        a = b.reshape(-1)
        a.sort()
        sea_level = a[int(len(a) * coverage)]
        return sea_level
    

    def get_highest_peak(self):
        b = np.copy(self.value_map.coordinates)
        a = b.reshape(-1)
        return max(a)


    def expand_dimensions(self, factor):
        self.value_map.dimension_expansion(factor)
    

    def expand_dimensions_gaussian(self, factor):
        self.value_map.gaussian_dimension_expansion(factor)


    def expand_dimensions_transitional_gaussian(self, factor):
        self.value_map.transitional_gaussian_dimension_expansion(factor)


class Geology(TectonicDomain):
    # TODO: rock cycle: igneous -> sedimentary -> polymorphic (time-based)
        # igneous rocks occur at volcanism and divergent boundaries
        # igneous rock turns into sedimentary rock based on time, sedimentary rock turns into polymorphic rock
    # TODO: metal occurrences at the surface, possibly related to different types of rock
        # metals of interest: Fe, Cu, Pb, Sn, Ag, Au, Pt, Zn, Bi
        # weight determines where the metals are in the crust, overall abundance also plays a role
        # https://iperiodictable.com/wp-content/uploads/2020/06/Periodic-Table-of-Elements-with-Names.png
        # https://en.wikipedia.org/wiki/Abundance_of_elements_in_Earth's_crust
        # https://www.geologyin.com/2014/05/tectonic-settings-of-metal-deposits.html
        # https://www.geologyin.com/2023/07/how-rocks-are-made-rock-cycle-explained.html
        # https://opengeology.org/Mineralogy/9-ore-deposits-and-economic-minerals/
        # https://www.geologyin.com/2023/09/mafic-vs-felsic-rocks-difference.html
        # mafic vs felsic rock seems a very sensible metric to distinguish iron deposits from other deposits, it is consistent with earth's ore deposits
        # https://www.geologyin.com/2015/11/how-ore-deposits-are-formed.html
        # - copper veins form 2000m beneath the surface because of water precipitation, i.e. veins are only realistically accessible in mountains
        # https://www.youtube.com/@sprottedu2478/search?query=ore%20deposits
        # https://geologyscience.com/ore-minerals/copper-cu-ore/#Copper_Cu_Ore_Deposits
    def __init__(self, dimensions):
        self.dimensions = dimensions
        # TODO: model mafic vs felsic rocks (100 element representations in list, calculate the silica content) with random.choices
        # also model intrusive vs volcanic rock, point interactions could do this - erosion shifts a intrusive/extrusive ratio towards intrusive, newly formed formations shift it back
        # the ratio models the surface accessible rock type
    
    def determine_rock_type(self):
        abundant_elements = {"O":0.641, "Si":0.282, "Al":0.0823, "Fe":0.0563, "Ca":0.0415, "Na":0.0236, "Mg":0.0233, "K":0.0209}
        abundand_elements = ["O", "Si", "Al", "Fe", "Ca", "Na", "Mg", "K"]
        abundances = [0.641, 0.282, 0.0823, 0.0563, 0.0415, 0.0236, 0.0233, 0.0209]
        magma_contents = {"O":0, "Si":0, "Al":0, "Fe":0, "Ca":0, "Na":0, "Mg":0, "K":0}
        for i in range(1000):
            magma_contents[random.choices(abundant_elements, weights=abundances)[0]] += 1
        if magma_contents["O"] + magma_contents["Si"] >= 650:
            return "felsic"
        elif magma_contents["O"] + magma_contents["Si"] >= 550:
            return "intermediate"
        elif magma_contents["O"] + magma_contents["Si"] >= 450:
            return "mafic"
        else:
            return "ultramafic"

    # types of copper deposits:
    #   - porphyry -> intrusive igneous rock + hot fluid (volcanism)
    #   - VMS -> volcanism in the ocean (historically significant, associated with subduction zones)
    #   . skarn -> intrusive igneous rock + carbonate sedimentary rock + volcanism (also contains all other base metals + precious metals, depending on host rock)
    #   - hydrothermal -> volcanic activity + limestone/dolomite "and other rocks"
    # malachite forms as oxidation of exposed copper from many of these different deposits, especially VMS since sulfides are likely to turn into malachite

    # types of tin deposits:
    #

    # types of lead deposits:
    #

    # types of silver deposits:
    #

    # types of gold deposits:
    #

    # types of iron deposits:
    #


    def apply_volcanism(self, x, y):
        #TODO: for more variety in rock types (and thereby mineral occurrence), random percentages of elements in magma are possible, based on solar abundance
        volcanism_potency = 3
        self.value_map.increment_coordinate_value(x, y, self.get_transfer_unit(self.base_unit, volcanism_potency))


    def transform_interaction(self, x1, y1, x2, y2, transfer_unit, ratio):
        # TODO: creates gorges where intrusive rock becomes visible - strong shift in the intrusive/extrusive ratio
        pass


    def get_transfer_unit(self, value, ratio):
        pass


    def apply_rock_cycle(self):
        pass


class TectonicMovements:

    def __init__(self, magma_currents:MagmaCurrentMap, tectonic_plates:TectonicPlates, topography:Topography):
        self.currents = magma_currents
        self.plates = tectonic_plates
        self.topography = topography
        #self.geology = geology
        self.map_helper = ObjectMap(((0,1), (0,1)), 0)
        self.subduction_ratio = 0.1
        self.generate_plate_coordinate_lists()
        self.volcanism_chance = 0.1
        self.hotspots = []
        self.n_hotspots = 5
        self.hotspot_min_age = 50
        self.hotspot_max_age = 500


    def generate_hotspot(self, min_age, max_age):
        return {
                "x":random.randint(self.topography.dimensions[0][0], self.topography.dimensions[0][1]),
                "y":random.randint(self.topography.dimensions[1][0], self.topography.dimensions[1][1]),
                "lifespan":random.randint(min_age, max_age)
        }


    def manage_hotspots(self):
        self.hotspots = [h for h in self.hotspots if h["lifespan"] > 0]
        while len(self.hotspots) < self.n_hotspots:
            hotspot = self.generate_hotspot(self.hotspot_min_age, self.hotspot_max_age)
            if not hotspot in self.hotspots:
                self.hotspots.append(hotspot)


    def apply_hotspots(self):
        for hotspot in self.hotspots:
            self.apply_volcanism(hotspot["x"], hotspot["y"])
            hotspot["lifespan"] -= 1


    # TODO: adjust this so that the boundaries no longer occupy coordinate points
    # a boundary coordinate belongs to the plate of the lowest plate_id
    # this can be achieved without changing the tectonic plate implementation by disregarding some coordinates in this method
    # a bool is_adjacent_to_boundary must exist (basically does a coordinate neighbor another coordinate with two or more plate ids)
    def generate_plate_coordinate_lists(self):
        plate_coordinates = {}
        for i in range(self.plates.plate_id):
            plate_coordinates[i] = []
        for coordinate in self.plates.plate_map.get_all_coordinates():
            # the plate of lowest plate_id owns the coordinate
            owner = min(self.plates.get_coordinate_value(coordinate[0], coordinate[1]))
            plate_coordinates[owner].append(coordinate)
        self.plate_coordinates = plate_coordinates
        

    def get_plate_coordinates(self, plate_id):
        return self.plate_coordinates[plate_id]


    def get_neighbor_interactions(self, x, y, vector):
        resized_vector = self.map_helper.standardize_vector(vector[0], vector[1])
        #available_neighbors = [n for n in self.map_helper.get_adjacent_coordinates(x, y) if ]
        
        goal_point = (x+resized_vector[0], y+resized_vector[1])
        available_neighbors = [n for n in self.map_helper.get_adjacent_coordinates(x, y)
                                if self.map_helper.get_distance(goal_point[0], goal_point[1], n[0], n[1]) < 1]
        if len(available_neighbors) == 1:
            return {available_neighbors[0]:1.0}
        elif len(available_neighbors) == 0:
            return {}
        sum_distance = sum([self.map_helper.get_distance(goal_point[0], goal_point[1], n[0], n[1]) for n in available_neighbors])
        neighbor_movements = {n:round((1 - (self.map_helper.get_distance(goal_point[0], goal_point[1], n[0], n[1])/sum_distance)), 2) for n in available_neighbors}
        return neighbor_movements


    def is_boundary(self, x, y):
        # returns True either if plates contains two or more values OR if any neighbor checks that box, BECAUSE boundaries no longer occupy a point,
        # and only one plate can own the point with two or more plate_ids
        owner_id = min(self.plates.get_coordinate_value(x,y))
        return any([owner_id != min(self.plates.get_coordinate_value(c[0], c[1])) for c in self.plates.plate_map.get_adjacent_coordinates_within_dimensions(x,y)])


    def identify_interaction(self, x1, y1, x2, y2):
        origin_value = self.plates.get_coordinate_value(x1, y1)
        origin_id = min(origin_value)
        destination_value = self.plates.get_coordinate_value(x2, y2)
        if destination_value is None:
            return 'transform'

        if origin_id == min(destination_value):
            # inter-plate interaction
            if self.is_boundary(x1, y1) and self.is_boundary(x2, y2):
                return 'transform'
            elif self.is_boundary(x1, y1):
                return 'divergent'
            else:
                return 'transfer'
        else:
            # plate-2-plate interaction
            if self.topography.get_height(x1, y1) <= self.topography.get_height(x2, y2) * self.subduction_ratio:
                return 'subduction'
            else:
                return 'convergent'
            

    
    def point_interaction(self, x1, y1, x2, y2, interaction_type, ratio):
        self.topography.point_interaction(x1, y1, x2, y2, interaction_type, ratio)
        #self.geology.point_interaction(x1, y1, x2, y2, interaction_type, ratio)
        # perform other interactions if necessary


    def apply_changes(self):
        self.topography.apply_changes()
        #self.geology.apply_changes()
        # perform this operation in other objects if needed


    def apply_volcanism(self, x, y):
        #TODO: add hotspots as a means of encouragin inter-plate mountain ranges and peninsulae / island archipelagos
        if random.random() <= self.volcanism_chance:
            self.topography.apply_volcanism(x,y)

    # to avoid the scenario of plates running away from each other (and the 3 or more intersecting plate issue), only one plate is moving at a time
    def simulate_plate_movement(self):
        # pick a plate randomly:
        plate_id = random.choice(list(range(self.plates.plate_id)))
        vector_map = self.currents.generate_magma_current_vectors()
        vector = self.plates.get_plate_direction(plate_id, vector_map)
        self.apply_vector_to_plate(vector, plate_id)
        self.apply_hotspots()
        self.manage_hotspots()
        


    def apply_vector_to_plate(self, vector, plate_id):
        coordinates = self.get_plate_coordinates(plate_id)
        for coordinate in coordinates:
            interactions = self.get_neighbor_interactions(coordinate[0], coordinate[1], vector)
            for interaction_point in interactions:
                interaction_type = self.identify_interaction(coordinate[0], coordinate[1], interaction_point[0], interaction_point[1])
                self.point_interaction(coordinate[0], coordinate[1], interaction_point[0], interaction_point[1], interaction_type, interactions[interaction_point])
                if interaction_type == 'divergent':
                    self.apply_volcanism(coordinate[0], coordinate[1])
                elif interaction_type == 'subduction':
                    self.apply_volcanism(interaction_point[0], interaction_point[1])
        self.apply_changes()


class World:

    def __init__(self, dimensions, seed):
        self.dimensions = dimensions
        random.seed(seed)
    

    def prepare_tectonics(self, n_splits, min_split_distance):
        self.tectonic_splits = TectonicSplits(self.dimensions)
        for i in range(n_splits):
            self.tectonic_splits.add_initial_split(min_split_distance)
    

    def develop_splits(self):
        finished = 0
        while finished == 0:
            self.tectonic_splits.develop_splits()

    
    def prepare_tectonic_movements(self):
        self.tectonic_plates = TectonicPlates(self.dimensions)
        self.tectonic_plates.generate_from_splits(self.tectonic_splits.split_map)
        self.topography = Topography(self.dimensions)
        self.magma_currents = MagmaCurrentMap(self.topography.topo_map)
        self.tectonic_movements = TectonicMovements(self.magma_currents, self.tectonic_plates, self.topography)

    
    def simulate_tectonic_movement(self):
        self.tectonic_movements.simulate_plate_movement()
    