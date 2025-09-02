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

//#TODO: divide values by 3 when using dimension expansion???

int main() {
    
    //world_base::World w({5,5}, "backpack");
    //w.prepare_tectonics(1, 10.0);
    
    world_base::World w({100,100}, "capital");
    w.prepare_tectonics(20, 20.0);
    
    //TODO: reactivate hotspots in tectonicmovements

    w.develop_splits();
    w.splits_object.print_split_map();
    w.prepare_tectonic_movements();

    //return 0;
    for (int i=0; i<10000; i++) {
        w.simulate_tectonic_movements();
    }
    std::cout<<w.geology_object.get_sea_level()<<" "<<w.geology_object.get_sea_coverage()<<"\n";
    

    w.expand_dimensions(2);
    std::cout<<"finished dimensions expansion\n";
    std::cout<<w.geology_object.get_sea_level()<<" "<<w.geology_object.get_sea_coverage()<<"\n";

    return 0;
}