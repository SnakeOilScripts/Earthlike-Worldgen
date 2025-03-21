import random
import math
import sys

random.seed()

class World:

    def __init__(self, dimensions):
        self.dimensions = dimensions


    def prepare_tectonics(self, max_splits, min_distance):
        self.tectonics = Tectonics(self.dimensions)
        for i in range(max_splits):
            self.tectonics.generate_random_split(min_distance)


    def generate(self):
        tectonics_finished = 0
        while tectonics_finished == 0:
            teconics_finished = self.tectonics.develop_splits()



class Points:
    def __init__(self, dimensions):
        # dimensions are [(xmin,xmax),(ymin,ymax)]
        self.dimensions = dimensions
        self.points = {}
    

    def point_outside_dimensions(self, x, y):
        return (x < self.dimensions[0][0] or x >= self.dimensions[0][1] or y < self.dimensions[1][0] or y >= self.dimensions[1][1])
    
    
    def add_point(self, x, y, value):
        if self.point_outside_dimensions(x,y):
            return -1
        if (x,y) not in self.points.keys():
            self.points[(x,y)] = value
        else:
            return -1


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


    def get_adjacent_neighbors(self, x, y):
        possible_neighbors = self.get_adjacent_points(x, y)
        neighbors = []
        for p in possible_neighbors:
            if p in self.points.keys():
                neighbors.append(p)
        return neighbors
    

    def get_adjacent_neighbors_by_value(self, x, y, value):
        possible_neighbors = self.get_adjacent_points(x, y)
        neighbors = []
        for p in possible_neighbors:
            if p in self.points.keys():
                if self.points[p] == value:
                    neighbors.append(p)
        return neighbors


    def get_closest_neighbor(self, base_point):
        # base_point = (x,y)
        clostest_neighbor = (self.dimensions[0][1] * 10, self.dimensions[1][0]) # impossible to reach therefore highest distance
        for p in self.points.keys():
            if p == base_point:
                continue
            if self.get_distance(p, base_point) < self.get_distance(clostest_neighbor, base_point):
                clostest_neighbor = p
        return clostest_neighbor



class Line(Points):

    def __init__(self, dimensions, value):
        self.value = value
        self.active = True
        super().__init__(dimensions)
    

    def get_ends(self):
        return [p for p in self.points.keys() if len(self.get_adjacent_neighbors(p[0], p[1])) < 2]


    def get_middle_point(self):
        ends = self.get_ends()
        vector = (ends[0][0] - ends[1][0], ends[0][1] - ends[1][1])
        return (int(ends[0][0] + vector[0]/2), int(ends[0][1] + vector[1]/2))


    def add_point(self, x, y):
        super().add_point(x, y, self.value)


        
class Tectonics():

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.split_bases = Points(dimensions)   # for distance calculation in initial split generation
        self.splits = []                        # for development of splits
        self.split_id = 1


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
        if len(self.split_bases.points.keys()) == 0:
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
                                    if split.get_distance(p, split.get_middle_point()) >= end_distance          #has to be replaced to avoid unterminated lines...
                                    and len(split.get_adjacent_neighbors(p[0], p[1])) < 2
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
        straight_line_bias = 0.8
        if random.random() <= straight_line_bias or len(split_options) <= 2:
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


    def unify_splits(self):
        united_points = Points(self.dimensions)
        for split in self.splits:
            for p in split.points:
                united_points.add_point(p[0], p[1], split.value)
        return united_points
