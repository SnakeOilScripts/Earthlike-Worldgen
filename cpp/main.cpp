#include <iostream>
#include "coordinate.hpp"
#include "ObjectMap.hpp"
#include "ObjectMap.cpp"
#include "UpdateMap.hpp"
#include "UpdateMap.cpp"
#include "SetMap.hpp"
#include "SetMap.cpp"
#include "Split.hpp"
#include "Split.cpp"
#include "TectonicSplits.hpp"
#include "TectonicSplits.cpp"
#include "TectonicPlates.hpp"
#include "TectonicPlates.cpp"
#include "TectonicDomain.hpp"
#include "TectonicDomain.cpp"
#include "Geology.hpp"
#include "Geology.cpp"
#include "TectonicMovements.hpp"
#include "TectonicMovements.cpp"
#include "World.hpp"
#include "World.cpp"

int main() {
    
    world_base::World w({5,5}, "backpack");
    w.prepare_tectonics(1, 10.0);
    
    //world_base::World w({50,50}, "capital");
    //w.prepare_tectonics(10, 10.0);
    
    //TODO: reactivate hotspots in tectonicmovements

    w.develop_splits();
    w.splits_object.print_split_map();
    w.prepare_tectonic_movements();
    w.geology_object.apply_volcanism({0,0});
    w.geology_object.apply_volcanism({1,0});
    w.geology_object.apply_changes();

    w.geology_object.print_height_map();
    
    //w.geology_object.falloff_interaction({0,2}, );

    //return 0;
    for (int i=0; i<10; i++) {
        w.simulate_tectonic_movements();
        w.geology_object.print_height_map();
        std::cout<<"____________________________________\n";
    }
    

    //w.expand_dimensions(2);
    //std::cout<<"finished dimensions expansion\n";

    return 0;
}