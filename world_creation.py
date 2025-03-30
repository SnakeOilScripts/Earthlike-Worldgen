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


    def prepare_tectonics(self, max_splits, min_distance):
        self.tectonics = TectonicSplits(self.dimensions)
        for i in range(max_splits):
            self.tectonics.generate_random_split(min_distance)


    def generate_plates(self):
        self.plates = TectonicPlates(self.dimensions)
        self.plates.generate_from_splits(self.tectonics.unify_splits())
        self.plates.generate_all_filled_plates()


    def simulate_plate_movement(self):
        pass


class Coordinates:
    # intended for cases where every point of the coordinate system has to have a value, like elevation
    def __init__(self, dimensions):
        coordinates_list = [[0]*(dimensions[1][1] - dimensions[1][0])] * (dimensions[0][1] - dimensions[0][0])
        self.coordinates = np.array(coordinates_list)
        self.dimensions = dimensions


    def coordinate_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])


    def set_coordinate_value(self, x, y, value):
        if not self.coordinate_outside_dimensions(x, y):
            self.coordinates[x,y] = value
            return 0
        else:
            return -1


    def get_adjacent_coordinates(self, x, y):
        return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]


    def get_adjacent_coordinates_within_dimensions(self, x, y):
        return [c for c in self.get_adjacent_coordinates(x,y) if not self.coordinate_outside_dimensions(c[0], c[1])]
    

    def get_coordinate_value(self, x, y):
        return self.coordinates[x,y]


class VectorMap(Coordinates):

    def __init__(self, dimensions):
        super().__init__(dimensions)
        base_vectors = [[(0,0)] * (dimensions[1][1] - dimensions[1][0])] * (dimensions[0][1] - dimensions[0][0])
        self.coordinates = np.array(base_vectors)


class Points:
    # indented for cases where only some points need a value, like "is volcano" = 0/1
    def __init__(self, dimensions):
        # dimensions are [(xmin,xmax),(ymin,ymax)]
        self.dimensions = dimensions
        self.points = {}
    

    def point_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])
    
    
    def add_point(self, x, y, value):
        if self.point_outside_dimensions(x,y):
            return -1
        if (x,y) not in self.points:
            self.points[(x,y)] = value
        else:
            return -1


    def merge_points(self, merge:dict):
        self.points = self.points.copy()
        self.points.update(merge.copy())


    def get_distance(self, point1, point2):
        return math.sqrt(math.pow(point1[0] - point2[0],2)+math.pow(point1[1] - point2[1],2))


    def change_value(self, x, y, value):
        if (x,y) in self.points:
            self.points[(x,y)] = value
        else:
            return -1


    def get_adjacent_points(self, x, y):
        adjacent_points = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
        return adjacent_points


    def get_adjacent_points_within_dimensions(self, x, y):
        adjacent_points = self.get_adjacent_points(x, y)
        return [p for p in adjacent_points if not self.point_outside_dimensions(p[0], p[1])]


    def get_adjacent_empty_within_dimensions(self, x, y):
        adjacent_points = self.get_adjacent_points_within_dimensions(x, y)
        return [p for p in adjacent_points if p not in self.points]


    def get_adjacent_neighbors(self, x, y):
        possible_neighbors = self.get_adjacent_points(x, y)
        neighbors = []
        for p in possible_neighbors:
            if p in self.points:
                neighbors.append(p)
        return neighbors
    

    def get_adjacent_nondiagonal_neighbors(self, x, y):
        neighbors = self.get_adjacent_neighbors(x, y)
        return [n for n in neighbors if n[0] == x or n[1] == y]


    def get_adjacent_neighbors_by_value(self, x, y, value):
        possible_neighbors = self.get_adjacent_points(x, y)
        neighbors = []
        for p in possible_neighbors:
            if p in self.points:
                if self.points[p] == value:
                    neighbors.append(p)
        return neighbors


    def get_closest_neighbor(self, base_point):
        # base_point = (x,y)
        clostest_neighbor = (self.dimensions[0][1] * 10, self.dimensions[1][0]) # impossible to reach therefore highest distance
        for p in self.points:
            if p == base_point:
                continue
            if self.get_distance(p, base_point) < self.get_distance(clostest_neighbor, base_point):
                clostest_neighbor = p
        return clostest_neighbor



class Line(Points):

    def __init__(self, dimensions, value):
        self.value = value
        self.active = True
        self.distance_irrelevant = False
        self.circles_allowed = False
        super().__init__(dimensions)


    def get_ends(self):
        return [p for p in self.points if len(self.get_adjacent_neighbors(p[0], p[1])) < 2]


    def set_distance_irrelevant(self, relevancy:bool):
        self.distance_irrelevant = relevancy


    def set_circle_allowed(self, forbidden:bool):
        self.circles_allowed = forbidden


    def get_middle_point(self):
        ends = self.get_ends()
        vector = (ends[0][0] - ends[1][0], ends[0][1] - ends[1][1])
        return (int(ends[0][0] + vector[0]/2), int(ends[0][1] + vector[1]/2))


    def add_point(self, x, y):
        super().add_point(x, y, self.value)


        
class TectonicSplits():

    def __init__(self, dimensions, straight_line_bias=0.8):
        self.dimensions = dimensions
        self.split_bases = Points(dimensions)   # for distance calculation in initial split generation
        self.splits = []                        # for development of splits
        self.split_id = 1
        self.straight_line_bias = straight_line_bias


    def generate(self):
        tectonics_finished = 0
        while tectonics_finished == 0:
            teconics_finished = self.develop_splits()
        self.activate_unfinished_splits()
        self.distance_irrelevant()
        while tectonics_finished == 0:
            teconics_finished = self.tectonics.develop_splits()

    def add_split(self, x, y):
        self.split_bases.add_point(x, y, self.split_id)
        l = Line(self.dimensions, self.split_id)
        l.add_point(x, y)
        random_neighbor = random.choice(l.get_adjacent_points_within_dimensions(x, y))
        l.add_point(random_neighbor[0], random_neighbor[1])
        self.splits.append(l)
        self.split_id += 1


    def generate_random_split(self, minimum_distance, max_attempts=50):
        # randomly pick a point for a tectonic break/volcano, with a minimum distance from all other previous points
        attempts = 0
        point = (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), random.randint(self.dimensions[1][0], self.dimensions[1][1]-1))
        if len(self.split_bases.points) == 0:
            self.add_split(point[0], point[1])
        else:
            while self.split_bases.get_distance(point, self.split_bases.get_closest_neighbor(point)) < minimum_distance:
                point = (random.randint(self.dimensions[0][0], self.dimensions[0][1]-1), random.randint(self.dimensions[1][0], self.dimensions[1][1]-1))
                attempts += 1
                if attempts >= max_attempts:
                    return -1
            self.add_split(point[0], point[1])
    

    def get_split_options(self, split:Line):
        options = []
        for end in split.get_ends():        # both ends need to be treated separately for activity monitoring
            end_distance = split.get_distance(end, split.get_middle_point())
            # eligible neighbors are all adjacent points that have a higher or equal distance from the middle point than the specified end
            allowed_neighbors = [  p for p in split.get_adjacent_points_within_dimensions(end[0], end[1])
                                    if (split.get_distance(p, split.get_middle_point()) >= end_distance or split.distance_irrelevant)
                                    and (len(split.get_adjacent_neighbors(p[0], p[1])) < 2 or split.circles_allowed)
                                    and not any([p in s.points for s in self.splits])
                                ]
            if allowed_neighbors == []:
                continue
            for s in self.splits:
                if all([n in s.points for n in allowed_neighbors]):
                    # check if all eligible neighbors are already part of another split
                    continue
            options += allowed_neighbors
        return options


    def check_split_activity(self):
        for s in self.splits:    
            options = self.get_split_options(s)
            if options == []:
                s.active = False
        return any(s.active for s in self.splits)


    def get_active_splits(self):
        return [s for s in self.splits if s.active == True]

            
    def develop_splits(self):
        if not self.check_split_activity():
            return -1
        # pick a random split-line
        split = random.choice(self.get_active_splits())
        # pick a random end of the split
        split_options = self.get_split_options(split)
        split_options.sort(key=lambda x: split.get_distance(split.get_middle_point(), x), reverse=True)
        # create a bias towards maximum distance from middle point i.e. straight line bias
        if random.random() <= self.straight_line_bias or len(split_options) <= 2:
            chosen_option = random.choice(split_options[:2])
        else:
            chosen_option = random.choice(split_options[2:])
        split.add_point(chosen_option[0], chosen_option[1])
        return 0
    

    def split_unfinished(self, split):
        ends = split.get_ends()
        for end in ends:
            for n in split.get_adjacent_points(end[0], end[1]):
                if split.point_outside_dimensions(n[0], n[1]) or any([n in s.points for s in self.splits if s.value != split.value]):
                    break
                return True
        return False


    def activate_unfinished_splits(self):
        for split in self.splits:
            if self.split_unfinished(split):
                split.active = True


    def allow_circles(self):
        for split in self.splits:
            split.set_circle_allowed(True)

    
    def distance_irrelevant(self):
        for split in self.splits:
            split.set_distance_irrelevant(True)


    def unify_splits(self):
        united_points = Points(self.dimensions)
        for split in self.splits:
            for p in split.points:
                united_points.add_point(p[0], p[1], split.value)
        return united_points



class TectonicPlates():
    
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.plates = []
        self.filled_plates = []


    def add_boundaries(self, points:Points, value=1):
        for x in range(self.dimensions[0][0], self.dimensions[0][1]):
            points.add_point(x, self.dimensions[1][0], value)
            points.add_point(x, self.dimensions[1][1]-1, value)     # these boundaries are supposed to be WITHIN the boundaries of the Points-Object
        for y in range(self.dimensions[1][0], self.dimensions[1][1]):
            points.add_point(self.dimensions[0][0], y, value)
            points.add_point(self.dimensions[0][1]-1, y, value)
        return points


    def generate_inverse_neighbors(self, base:Points, value=1):
        neighbors = Points(self.dimensions)
        for p in base.points:
            for n in base.get_adjacent_empty_within_dimensions(p[0], p[1]):
                neighbors.add_point(n[0], n[1], value)
        return neighbors


    def extract_cycle(self, base:Points, start):
        cycle = Points(self.dimensions)
        self.follow_cycle(cycle, base, start)
        for p in cycle.points:
            del base.points[p]
        return cycle


    def follow_cycle(self, cycle:Points, base:Points, start):
        point_added = cycle.add_point(start[0], start[1], base.points[start])
        if point_added == -1:
            return
        else:
            for neighbor in base.get_adjacent_nondiagonal_neighbors(start[0], start[1]):
                self.follow_cycle(cycle, base, neighbor)
        return


    def create_aligned_plate(self, splits:Points, cycle:Points, plate_id):
        plate = Points(self.dimensions)
        for p in splits.points:
            if cycle.get_adjacent_neighbors(p[0], p[1]) != []:
                plate.add_point(p[0], p[1], plate_id)
        return plate


    def generate_from_splits(self, splits:Points):
        # splits is the output of unify_splits() in TectonicSplits
        plate_id = 1
        splits = self.add_boundaries(splits)
        inverse_neighbors = self.generate_inverse_neighbors(splits)
        while inverse_neighbors.points != {}:
            cycle = self.extract_cycle(inverse_neighbors, random.choice(list(inverse_neighbors.points.keys())))
            self.plates.append(self.create_aligned_plate(splits, cycle, plate_id))
            plate_id += 1
    

    def find_plate_interior_neighbors(self, plate:Points):
        # finds the neighbors of the plate boundary which stand on the inside of the plate - useful for gathering all points of the plate
        inverse_neighbors = self.generate_inverse_neighbors(plate)
        neighbor_cycles = []
        for i in range(2):
            try: # fails if no two cycles (or none at all) can be extracted - this is only the case if the "base" is a line or double line, instead of a cycle itself
                cycle = self.extract_cycle(inverse_neighbors, random.choice(list(inverse_neighbors.points.keys())))
            except:
                return -1
            neighbor_cycles.append(cycle)
        if len(neighbor_cycles[0].points) < len(neighbor_cycles[1].points):
            return neighbor_cycles[0]
        else:
            return neighbor_cycles[1]
    

    def generate_filled_plate(self, plate:Points):
        filled_plate = Points(self.dimensions)
        while plate != -1:
            filled_plate.merge_points(plate.points)
            plate = self.find_plate_interior_neighbors(plate)
    

    def generate_all_filled_plates(self):
        for plate in self.plates:
            self.filled_plates.append(self.generate_filled_plate(plate))


class MagmaCurrentMap(Coordinates):

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

    def apply_erosion(self):
        pass
    
