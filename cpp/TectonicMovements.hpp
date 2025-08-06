#include <vector>
#include <pair>
#include <string>
#include <algorithm>
#include <random>
#include "coordinate.hpp"
#include "ObjectMap.hpp"
#include "TectonicPlates.hpp"
#include "Geology.hpp"

#ifndef _TECTONICMOVEMENTS_H_
#define _TECTONICMOVEMENTS_H_

namespace world_base {

    class TectonicMovements {
        protected:
            coordinate dimensions;
            TectonicPlates *plates_object;
            Geology *geology_object;
            ObjectMap<bool> map_helper;
            float subduction_requirement;
            float volcanism_chance;
            std::vector<coordinate> hotspots;
            int n_hotspots;
            int hotspot_min_age;
            int hotspot_max_age;
            std::vector<std::vector<coordinate>> plate_coordinates;
        public:
            TectonicMovements();
            TectonicMovements(coordinate d, TectonicPlates *p, Geology *g);
            std::pair<coordinate,int> generate_hotspot();
            void manage_hotspots();
            void apply_hotspots();
            std::vector<std::pair<coordinate,float>> get_neighbor_interactions(coordinate c, fvector v);
            //bool is_boundary(coordinate c);
            std::string identify_interaction(coordinate from, coordinate to);
            void point_interaction(coordinate from, coordinate to, std::string interaction_type, float ratio);
            void apply_changes();
            void apply_volcanism(coordinate c);
            void simulate_plate_movement();
            void apply_vector_to_plate(fvector v, std::vector<coordinate> plate);
    };
}

#endif