#include "World.hpp"

namespace world_base {
    
    World::World(coordinate d, std::string seed) {
        dimensions = d;
        int iseed, rank;
        iseed = 0;
        rank = seed.size()-1;
        for (auto c:seed) {
            iseed += rank * c;
            rank--;
        }
        srand(iseed);
    }


    void World::prepare_tectonics(int n_splits, float min_split_distance) {
        splits_object = TectonicSplits(dimensions);
        for (int i=0; i<n_splits; i++) {
            splits_object.add_initial_split(min_split_distance);
        }
    }


    void World::develop_splits() {
        int finished = 0;
        while (finished == 0) {
            finished = splits_object.develop_splits();
        }
    }


    void World::prepare_tectonic_movements() {
        plates_object = TectonicPlates(dimensions);
        plates_object.generate_from_splits(splits_object.get_split_map());
        geology_object = Geology(dimensions);
        movements_object = TectonicMovements(dimensions, &plates_object, &geology_object);
        //need to add one initial geological unit, to facilitate plate movement
        geology_object.apply_volcanism({0,0});
        geology_object.apply_changes();
    }


    void World::simulate_tectonic_movements() {
        movements_object.simulate_plate_movement();
    }


    void World::expand_dimensions(int factor) {
        geology_object.expand_dimensions_transitional_gaussian(factor);
    }
}