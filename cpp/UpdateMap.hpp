#include <vector>
#include <cmath>
#include "ObjectMap.hpp"

#ifndef _UPDATEMAP_H_
#define _UPDATEMAP_H_

// TODO make it fully inherit from ObjectMap

namespace world_base {

    template <typename T>
    class UpdateMap: public ObjectMap<T> {
        protected:
            //using ObjectMap<T>::ObjectMap;
            coordinate update_dimensions;
            std::vector<std::vector<T>> update;
        public:
            using ObjectMap<T>::ObjectMap;
            UpdateMap(coordinate d, T base_object);
            // requires the base_object to have a + and += operator defined!!! especially for new structs
            void increment_coordinate_value(coordinate c, T value);
            void apply_changes();
            float normal_pdf(float x, float mean, float standard_deviation);
            void transitional_gaussian_dimensions_expansion(int expansion_factor, T base_object);
            void increment_gaussian_coordinate(coordinate c, int x, int y, int expansion_factor, std::vector<std::vector<float>> *dp, T value);
};

}
#endif