#include <vector>
#include <set>
#include <algorithm>
#include <cstdlib>
#include "coordinate.hpp"
#include "Split.hpp"
#include "SetMap.hpp"

#ifndef _TECTONICSPLITS_H_
#define _TECTONICSPLITS_H_

namespace world_base {

    class TectonicSplits {
        
        protected:

            coordinate dimensions;
            float direction_change_rate;
            int direction_len;
            int split_id;
            SetMap split_map;
            std::vector<Split> splits;

        public:
            TectonicSplits();
            TectonicSplits(coordinate d, float dcr=0.5, int d_len=8);
            void initialize_split(coordinate base);
            void add_initial_split(float min_split_distance, int max_attempts=100);
            std::vector<Split*> get_active_splits();
            std::vector<coordinate> get_split_options(Split *s, coordinate end);
            int develop_splits();
            SetMap *get_split_map();
            void print_split_map();
    };
}
#endif