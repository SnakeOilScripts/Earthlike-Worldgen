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
    

    def prepare_tectonics(self, n_splits, min_split_distance, min_goal_distance):
        self.tectonic_splits = TectonicSplits(self.dimensions)
        for i in range(n_splits):
            self.tectonic_splits.add_initial_split(min_split_distance, min_goal_distance)


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


class Split:
    def __init__(self, shared_map:SplitMap, value):
        self.shared_map = shared_map
        self.value = value
        self.option_blacklist = set()
        self.ends = dict()


    def add_point(self, x, y):
        self.shared_map.add_coordinate_value(x, y, self.value)
    

    def set_end(self, x, y, goal):
        self.ends[(x,y)] = goal
    

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
        goal = self.get_end_goal(old_end)
        self.remove_end(old_end)
        self.set_end(x, y, goal)
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
        l_end_vector = self.shared_map.get_distance(0,0,end_vector[0],end_vector[1])
        l_angled_vector = self.shared_map.get_distance(0,0,angled_vector[0],angled_vector[1])
        dot_product = end_vector[0]*angled_vector[0] + end_vector[1]*angled_vector[1]
        angle = math.acos(round((dot_product) / (l_end_vector * l_angled_vector), 2))
        return angle


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
        goal = self.get_end_goal((x,y))
        self.remove_end((x, y))
        self.set_end(previous_end[0], previous_end[1], goal)
        self.option_blacklist.add((x,y))


class TectonicSplits:
    def __init__(self, dimensions, direction_change_rate=0.3, direction_calc_n=8):
        self.dimensions = dimensions
        self.direction_change_rate = direction_change_rate
        self.direction_calc_n = direction_calc_n
        self.split_map = SplitMap(dimensions)
        self.split_id = 0
        self.splits = []
    

    def initialize_split(self, base, min_goal_distance, max_attempts):
        new_split = Split(self.split_map, self.split_id)
        goals = self.generate_end_goals(min_goal_distance, max_attempts)
        new_split.add_point(base[0], base[1])
        new_split.set_end(base[0], base[1], goals[0])
        first_neighbor = random.choice(self.split_map.get_adjacent_coordinates_within_dimensions(base[0], base[1]))
        new_split.add_point(first_neighbor[0], first_neighbor[1])
        new_split.set_end(first_neighbor[0], first_neighbor[1], goals[1])
        self.splits.append(new_split)
        self.split_id += 1
    

    def generate_end_goals(self, min_goal_distance, max_attempts):
        for i in range(max_attempts):
            # this ensures that goals are not on the same axis, which makes one-thick-plates less likely to occur
            options = [
                        (self.dimensions[0][0], random.randint(self.dimensions[1][0], self.dimensions[1][1]-1)),
                        (self.dimensions[0][1]-1, random.randint(self.dimensions[1][0], self.dimensions[1][1]-1)),
                        (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), self.dimensions[1][0]),
                        (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), self.dimensions[1][1]-1)
                    ]
            goals = random.sample(options, k=2)
            if self.split_map.get_distance(goals[0][0], goals[0][1], goals[1][0], goals[1][1]) >= min_goal_distance:
                return goals
        return goals



    def add_initial_split(self, min_split_distance, min_goal_distance, max_attempts=100):
        for attempt in range(max_attempts):
            rejected = False
            new_center = (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), random.randint(self.dimensions[1][0], self.dimensions[1][1]-1))
            for s in self.splits:
                if s.get_center_distance(new_center[0], new_center[1]) < min_split_distance:
                    rejected = True
                    break
            if not rejected:
                self.initialize_split(new_center, min_goal_distance, max_attempts)
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



# TODO: double-check that this works with the new ObjectMap class
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

# TODO: implement, duh
class SurfaceMap:
    # types of plate boundaries:
    # - convergent (without subduction) -> fold mountains
    # - convergent (with subduction) -> trench + mountains/volcanos
    # - divergent -> mid-ocean ridge / rift valleys, volcanism
    # - transform -> strike-slip-fault
    # https://www.geologyin.com/2014/03/types-of-continental-boundaries.html
    def apply_erosion(self):
        pass
    
