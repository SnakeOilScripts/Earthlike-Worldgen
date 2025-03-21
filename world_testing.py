from world_creation import *

dimensions = ((0,50),(0,50))

t = Tectonics(dimensions)
split1 = Line(dimensions, 1)
split2 = Line(dimensions, 2)

split1.points = {(0,0):1, (1,1):1, (1,2):1, (2,3):1}
split2.points = {(3,3):2, (2,4):2, (3,2):2, (3,4):2, (1,4):2}

t.splits.append(split1)
t.splits.append(split2)

print(t.get_split_options(split1))
print(t.split_unfinished(split1))