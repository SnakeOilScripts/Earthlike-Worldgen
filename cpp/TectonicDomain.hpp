#include <vector>
#include <algorithm>
#include "coordinate.hpp"
#include "UpdateMap.hpp"

#ifndef _TECTONICDOMAIN_H_
#define _TECTONICDOMAIN_H_

namespace world_base {

    template <typename T>
    class TectonicDomain {
        private:
            float subduction_ratio = 0.5;
            float fold_ratio = 0.5;
            int volcanism_potency = 3;
            int cylce_ticker = 0;
            int cycle_interval = 100;
            UpdateMap<T> value_map;
            T base_unit;
            coordinate dimensions;
        public:
            TectonicDomain();
            TectonicDomain(coordinate d, T b);
            void apply_volcanism(coordinate c);
            T get_transfer_unit(T value, float ratio);
            UpdateMap<T> get_map();
            void apply_changes();
            void point_interaction(coordinate from, coordinate to, std::string mode, float ratio);
            void falloff_interaction(coordinate to, T transfer_unit);
            void transfer_interaction(coordinate from, coordinate to, T transfer_unit);
            void transform_interaction(coordinate from, coordinate to, T transfer_unit);
            void divergent_interaction(coordinate from, coordinate to, T transfer_unit, float ratio);
            void convergent_interaction(coordinate from, coordinate to, T transfer_unit);
            void subduction_interaction(coordinate from, coordinate to, T transfer_unit);
            T create_new_unit();
            void increment_cycle_ticker();
            void cycle_action();
            //placeholders meant to be overwritten by child class
            fvector generate_magma_current_vector(std::vector<coordinate> *plate);
            float get_height(coordinate c);
    }

}

#endif