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
        //for (int i=0; i<1000; i++) {
            finished = splits_object.develop_splits();
            //splits_object.print_split_map();
        }
        splits_object.print_split_map();
    }


    void World::prepare_tectonic_movements() {
        plates_object = TectonicPlates(dimensions);
        plates_object.generate_from_splits(splits_object.get_split_map());
        geology_object = Geology(dimensions);
        movements_object = TectonicMovements(dimensions, &plates_object, &geology_object);
    }


    void World::simulate_tectonic_movements() {
        movements_object.simulate_plate_movement();
    }
}