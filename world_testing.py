from world_creation import *

dimensions = ((0,3),(0,3))

base_surface = Coordinates(dimensions)

magma_currents = MagmaCurrentMap(dimensions, base_surface)
print(magma_currents.surface_map.coordinates)
base_surface.coordinates = np.array([[1,1,1],[0,2,1],[1,1,1]])
magma_currents.update_surface_map(base_surface)
vector_map = magma_currents.generate_magma_current_vectors()
print(vector_map.coordinates[0,0], vector_map.coordinates[0,2], vector_map.coordinates[1,1])