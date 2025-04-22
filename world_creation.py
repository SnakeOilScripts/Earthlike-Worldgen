import random
import math
import sys
import numpy as np
import copy

#random.seed()


#TODO:  1) general elevation levels (via plate tectonics) -> identify plate by randomly chosen point within it & vectors to all reachable points/closest neighbors
#          then simulate movement of plates by moving middle point & adjusting vectors
#       2) general erision to get classic foothill shapes (abstract wind&water) -> make map more detailed
#       3) add x units of water to every point, travel to lowest reachable point, simulate sea level and bodies of water with it
#       4) water cycle and river/lake formation
#       5) local climate, (ground type), humidity
#       6) local flora/fauna

# missing: mineral deposits?
#           read up on this here: geologyin.com



class ObjectMap:

    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
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


    def coordinate_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])


    def get_adjacent_coordinates(self, x, y):
        return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]


    def get_adjacent_nondiagonal_coordinates(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if c[0] == x or c[1] == y]


    def get_adjacent_coordinates_within_dimensions(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1])]

    
    def get_adjacent_nondiagonal_coordinates_within_dimensions(self, x, y):
        return [c for c in self.get_adjacent_nondiagonal_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1])]
    

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


class UpdateMap(ObjectMap):
    
    
    def __init__(self, dimensions, base_object):
        self.dimensions = dimensions
        self.base_object = base_object
        self.coordinates = self.create_coordinates(dimensions, base_object)
        self.coordinates_update = np.copy(self.coordinates)

    
    def increment_coordinate_value(self, x, y, value):
        if not self.coordinate_outside_dimensions(x, y):
            self.coordinates_update[x,y] += value
        else:
            return -1


    def apply_changes(self):
        self.coordinates = self.coordinates_update
        self.coordinates_update = np.copy(self.coordinates)


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
        #l_end_vector = self.shared_map.get_distance(0,0,end_vector[0],end_vector[1])
        #l_angled_vector = self.shared_map.get_distance(0,0,angled_vector[0],angled_vector[1])
        #dot_product = end_vector[0]*angled_vector[0] + end_vector[1]*angled_vector[1]
        #angle = math.acos(round((dot_product) / (l_end_vector * l_angled_vector), 2))
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



# TODO: implement, duh
class Topography:
    # types of plate boundaries:
    # - convergent (without subduction) -> fold mountains
    # - convergent (with subduction) -> trench + mountains/volcanos
    # - divergent -> mid-ocean ridge / rift valleys, volcanism
    # - transform -> strike-slip-fault
    # - volcanism
    # https://www.geologyin.com/2014/03/types-of-continental-boundaries.html
    def __init__(self, dimensions, base_height=100.0, volcanism_chance=0.01):
        self.dimensions = dimensions
        self.base_height = base_height
        self.volcanism_chance = volcanism_chance
        self.topo_map = UpdateMap(self.dimensions, 0.0)
        for coordinate in self.topo_map.get_all_coordinates():
            self.topo_map.increment_coordinate_value(coordinate[0], coordinate[1], self.base_height)
        self.topo_map.apply_changes()

    
    def apply_general_erosion(self, erosion_rate):
        for coordinate in self.topo_map.get_all_coordinates():
            self.apply_erosion(coordinate[0], coordinate[1], erosion_rate)
        self.topo_map.apply_changes()

    
    def apply_erosion(self, x, y, erosion_rate):
        available_neighbors = [n for n in self.topo_map.get_adjacent_coordinates_within_dimensions(x,y)
                                if self.topo_map.get_coordinate_value(n[0], [1]) >= self.topo_map.get_coordinate_value(x,y)]


    def apply_volcanism(self, x, y):
        volcanism_potency = 3
        self.topo_map.increment_coordinate_value(x, y, self.base_height * volcanism_potency)


    def point_interaction(self, x1, y1, x2, y2, mode, ratio):
        # point_interaction must check if the coordinate is within dimensions because of how the interaction calculation works
        # having the plate boundary occupying a coordinate breaks all systems I could come up with, here is the new plan:
        #   - for a coordinate with more than one plate_id in it, it belongs to the plate of the lowest plate_id
        #   - the ACTUAL plate boundary is a line of thickness 0 between two coordinates
        transfer_unit = round(self.topo_map.get_coordinate_value(x1, y1) * ratio, 2)
        if self.topo_map.coordinate_outside_dimensions(x2, y2):
            # if the interaction_point is out of dimensions, just remove the units to the transferred
            self.topo_map.increment_coordinate_value(x1, y1, (-1) * transfer_unit)      #needs a dedicated decrement for sub-0 heights
        elif mode == 'transform' or mode == 'transfer':
            self.topo_map.increment_coordinate_value(x1, y1, (-1) * transfer_unit)
            self.topo_map.increment_coordinate_value(x2, y2, transfer_unit)
        elif mode == 'divergent':
            self.topo_map.increment_coordinate_value(x1, y1, (-1)*transfer_unit)
            self.topo_map.increment_coordinate_value(x2, y2, transfer_unit)
            self.topo_map.increment_coordinate_value(x1, y1, self.base_height * ratio)
            # the thin replacement plate at the edge has a high volcanism risk
            self.apply_volcanism(x1, y1)
        elif mode == 'convergent':
            # the convergent coordinate will receive units from behind
            # give back fold_ratio * transfer_unit back to where it would come from
            reverse_neighbor = (x2-x1*(-1), y2-y1*(-1))
            fold_ratio = 0.5
            self.topo_map.increment_coordinate_value(x1, y1, (-1) * transfer_unit * fold_ratio)
            self.topo_map.increment_coordinate_value(reverse_neighbor[0], reverse_neighbor[1], transfer_unit * fold_ratio)
        elif mode == 'subduction':
            subduction_ratio = 0.5
            self.topo_map.increment_coordinate_value(x1, y1, (-1 - subduction_ratio) * transfer_unit)   # create trenches by creating less than 0 values
            self.topo_map.increment_coordinate_value(x2, y2, transfer_unit * subduction_ratio)
            # the mountain range that is raised by subduction has a high volcanism risk
            self.apply_volcanism(x2, y2)
        return

    
    def get_height(self, x, y):
        return self.topo_map.get_coordinate_value(x, y)


    def apply_changes(self):
        self.topo_map.apply_changes()


    def get_sea_level(self, coverage):
        # assuming coverage % of the world are covered in water, what is the corresponding sea level (i.e. the n-median)?
        b = np.copy(self.topo_map.coordinates)
        a = b.reshape(-1)
        a.sort()
        sea_level = a[int(len(a) * coverage)]
        return sea_level
    

    def get_highest_peak(self):
        b = np.copy(self.topo_map.coordinates)
        a = b.reshape(-1)
        return max(a)


class Geology:

    def __init__(self):
        pass

    def point_interaction(self, x1, y1, x2, y2, interaction, ratio):
        # point_interaction must check if the coordinate is within dimensions because of how the interaction calculation works
        pass


class TectonicMovements:

    def __init__(self, magma_currents:MagmaCurrentMap, tectonic_plates:TectonicPlates, topography:Topography):
        self.currents = magma_currents
        self.plates = tectonic_plates
        self.topography = topography
        self.map_helper = ObjectMap(((0,1), (0,1)), 0)
        self.subduction_ratio = 0.1
        self.generate_plate_coordinate_lists()
        self.volcanism_chance = 0.1


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
        # perform other interactions if necessary


    def apply_changes(self):
        self.topography.apply_changes()
        # perform this operation in other objects if needed


    def apply_volcanism(self, x, y):
        if random.random() <= self.volcanism_chance:
            self.topography.apply_volcanism(x,y)

    # to avoid the scenario of plates running away from each other (and the 3 or more intersecting plate issue), only one plate is moving at a time
    def simulate_plate_movement(self):
        # pick a plate randomly:
        plate_id = random.choice(list(range(self.plates.plate_id)))
        vector_map = self.currents.generate_magma_current_vectors()
        vector = self.plates.get_plate_direction(plate_id, vector_map)
        self.apply_vector_to_plate(vector, plate_id)


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
    

    def domain_expansion(self, expansion_factor):
        # make a map more detailed by inserting expansion_factor new coordinates between each coordinate and linear transfer of values
        pass