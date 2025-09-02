#include <vector>
#include <algorithm>
#include "coordinate.hpp"
#include "UpdateMap.hpp"

#ifndef _TECTONICDOMAIN_H_
#define _TECTONICDOMAIN_H_

namespace world_base {

    template <typename T>
    class TectonicDomain {
        protected:
            float subduction_ratio = 0.5;
            float fold_ratio = 0.5;
            int volcanism_potency = 3;
            int cycle_ticker = 0;
            int cycle_interval = 100;
            UpdateMap<T> value_map;
            T base_unit;
            coordinate dimensions;
        public:
            TectonicDomain();
            TectonicDomain(coordinate d, T b);
            virtual void apply_volcanism(coordinate c);
            virtual T get_transfer_unit(T value, float ratio);
            UpdateMap<T> get_map();
            void apply_changes();
            void point_interaction(coordinate from, coordinate to, std::string mode, float ratio);
            virtual void falloff_interaction(coordinate from, T transfer_unit);
            virtual void transfer_interaction(coordinate from, coordinate to, T transfer_unit);
            virtual void transform_interaction(coordinate from, coordinate to, T transfer_unit);
            virtual void divergent_interaction(coordinate from, coordinate to, T transfer_unit, float ratio);
            virtual void convergent_interaction(coordinate from, coordinate to, T transfer_unit);
            virtual void subduction_interaction(coordinate from, coordinate to, T transfer_unit);
            virtual T create_new_unit();
            void increment_cycle_ticker();
            virtual void cycle_action();
            //placeholders meant to be overwritten by child class
            virtual fvector generate_magma_current_vector(std::vector<coordinate> *plate);
            virtual float get_height(coordinate c);
    };

}

#endif