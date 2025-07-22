#include <vector>
#include <set>
#include "coordinate.hpp"
#include "SetMap.hpp"
#include "Split.hpp"
#include "TectonicSplits.hpp"

#ifndef _TECTONICPLATES_H_
#define _TECTONICPLATES_H_

namespace world_base {
    
    class TectonicPlates {
        
        protected:
            coordinate dimensions;
            SetMap plate_map;
            int plate_id;
            std::vector<std::vector<coordinate>> plates;
            std::vector<coordinate> boundaries;
        public:
        
            TectonicPlates(coordinate d);
            std::set<int> get_all_neighbor_values(coordinate c);
            void fill_plate_boundaries();
            void spread_value_within_boundary(SetMap *split_map, int value, coordinate start);
            void generate_from_splits(SetMap *split_map);
            std::vector<coordinate> get_plate(int id);
            std::vector<coordinate> get_plate_boundaries();
            int get_plate_count();
    };
}

#endif