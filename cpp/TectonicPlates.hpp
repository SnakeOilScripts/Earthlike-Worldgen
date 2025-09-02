#include <vector>
#include <set>
#include "coordinate.hpp"
#include "ObjectMap.hpp"
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
            ObjectMap<bool> boundary_map;
        public:
            TectonicPlates();
            TectonicPlates(coordinate d);
            std::set<int> get_all_neighbor_values(coordinate c);
            void spread_value_within_boundary(SetMap *split_map, int value, coordinate start);
            void generate_from_splits(SetMap *split_map);
            std::vector<coordinate> get_plate(int id);
            bool is_boundary(coordinate c);
            int get_plate_count();
            std::set<int> get_coordinate_value(coordinate c);
            void print_plate(int id);
    };
}

#endif