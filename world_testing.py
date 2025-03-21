from world_creation import *

dimensions = ((0,50),(0,50))

t = Tectonics(dimensions)
split1 = Line(dimensions, 1)
split2 = Line(dimensions, 2)

split1.points = {(1,1):1, (1,2):1, (1,3):1}
split2.points = {(2,2):2, (3,2):2, (4,2):2}

print(split1.get_ends())
print(split2.get_ends())

t.splits.append(split1)
t.splits.append(split2)

print(t.get_split_options(t.splits[1]))