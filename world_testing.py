from world_creation import *

dimensions = ((0,3),(0,3))

plates = TectonicPlates(dimensions)

n = Points(dimensions)
n.points = {(1,1):1}

c = plates.extract_cycle(n, (1,1))

print(n.points)
print(c.points)