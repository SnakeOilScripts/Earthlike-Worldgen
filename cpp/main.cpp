#include <iostream>
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

int main() {
    world_base::ObjectMap<int> m({2,2},0);
    std::cout<<m.get_coordinate_value({0,0})<<" "<<m.get_coordinate_value({1,1})<<"\n";
    world_base::ObjectMap<char> m2({2,2}, 'a');
    std::cout<<m2.get_coordinate_value({0,0})<<" "<<m2.get_coordinate_value({1,1})<<"\n";
    world_base::UpdateMap<int> m3({2,2}, 1);
    world_base::SetMap m4({2,2}, {1});
    return 0;
}