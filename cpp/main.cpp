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
    
    world_base::coordinate d{100,100};
    world_base::World w(d, "flowergarden");
    //world_base::World w(d, "empire");
    w.prepare_tectonics(20, 20.0);
    std::cout << "splits prepared\n";
    w.develop_splits();
    std::cout << "splits finished\n";
    
    /*
    std::set<world_base::coordinate> cset;
    cset.insert({87,39});
    cset.insert({86,39});
    std::cout<<cset.size()<<"\n";
    */
    //w.prepare_tectonic_movements();
    //w.simulate_tectonic_movements();

    return 0;
}