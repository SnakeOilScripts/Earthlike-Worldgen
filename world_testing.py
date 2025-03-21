from world_creation import *

dimensions = ((0,50),(0,50))

t = Tectonics(dimensions)
t.add_split(50,0)

print(t.splits[0].points)