#include <string>
#include "coordinate.hpp"
#include "TectonicSplits.hpp"
#include "TectonicPlates.hpp"
#include "TectonicMovements.hpp"

#ifndef _WORLD_H_
#define _WORLD_H_

namespace world_base {

    class World {
        protected:
            coordinate dimensions;
        public:
            TectonicSplits splits_object;
            TectonicPlates plates_object;
            Geology geology_object;
            TectonicMovements movements_object;
            World(coordinate d, std::string seed);
            void prepare_tectonics(int n_splits, float min_split_distance);
            void develop_splits();
            void prepare_tectonic_movements();
            void simulate_tectonic_movements();
    };
}

#endif