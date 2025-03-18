import random
import math

random.seed()

class World:

    def __init__(self, dimensions):
        self.dimensions = dimensions


    def prepare_tectonics(self, max_brkpts, min_distance):
        self.tectonics = Tectonics(self.dimensions)
        for i in range(max_brkpts):
            self.tectonics.generate_random_breakpoint(min_distance)


    def generate(self):
        tectonics_finished = 0
        while tectonics_finished == 0:
            teconics_finished = self.tectonics.develop_breaks()



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
        return int(math.sqrt(math.pow(point1[0] - point2[0],2)+math.pow(point1[1] - point2[1],2)))


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
        if any([self.point_outside_dimensions(n[0], n[1]) for n in possible_neighbors]):
            # points at the edge have the maximum number of neighbors
            return possible_neighbors
        neighbors = []
        for p in possible_neighbors:
            if p in self.points.keys():
                neighbors.append(p)
        return neighbors
    

    def get_adjacent_neighbors_by_value(self, x, y, value):
        possible_neighbors = self.get_adjacent_points(x, y)
        if any([self.point_outside_dimensions(n[0], n[1]) for n in possible_neighbors]):
            # points at the edge have the maximum number of neighbors
            return []
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

        
        
class Tectonics(Points):

    def __init__(self, dimensions):
        self.break_id = 1
        self.breakpoint_blacklist = {}
        super().__init__(dimensions)


    def add_breakpoint(self, x, y):
        self.add_point(x, y, self.break_id)
        adjacent_points = self.get_adjacent_points_within_dimensions(x, y)
        first_neighbor = random.choice(adjacent_points)
        self.add_point(first_neighbor[0], first_neighbor[1], self.break_id)
        self.breakpoint_blacklist[self.break_id] = set()
        self.break_id += 1


    def generate_random_breakpoint(self, minimum_distance, max_attempts=50):
        # randomly pick a point for a tectonic break/volcano, with a minimum distance from all other previous points
        attempts = 0
        point = (random.randint(self.dimensions[0][0], self.dimensions[0][1]), random.randint(self.dimensions[1][0], self.dimensions[1][1]))
        if len(self.points.keys()) == 0:
            self.add_breakpoint(point[0], point[1])
        else:
            while self.get_distance(point, self.get_closest_neighbor(point)) < minimum_distance:
                point = (random.randint(self.dimensions[0][0], self.dimensions[0][1]), random.randint(self.dimensions[1][0], self.dimensions[1][1]))
                attempts += 1
                if attempts >= max_attempts:
                    return -1
            self.add_breakpoint(point[0], point[1])
            

    def get_break_options(self, x, y, value):
        adjacent_points = self.get_adjacent_points(x, y)
        break_options = []
        for adj in adjacent_points:
            if adj in self.points.keys():
                continue
            elif adj in self.breakpoint_blacklist[value]:
                continue
            #elif self.point_outside_dimensions(adj[0], adj[1]):
            #    continue
            break_options.append(adj)
        return break_options


    def develop_breaks(self):
        loose_ends = self.get_loose_ends()
        if len(loose_ends) == 0:
            return 1
        for p in loose_ends:
            options = self.get_break_options(p[0], p[1], self.points[p])
            choice = random.choice(options)
            self.add_point(choice[0], choice[1], self.points[p])
            blacklist_points = self.get_adjacent_points(p[0], p[1])
            for b in blacklist_points:
                self.breakpoint_blacklist[self.points[p]].add(b)
        return 0


    def get_loose_ends(self):
        loose_ends = []
        for p in self.points.keys():
            if len(self.get_adjacent_neighbors(p[0], p[1])) < 2:
                loose_ends.append(p)
        return loose_ends