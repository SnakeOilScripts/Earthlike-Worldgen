#include "coordinate.hpp"
#include <vector>
#include <cmath>
#include <set>
#include <algorithm>

#ifndef _OBJECTMAP_H_
#define _OBJECTMAP_H_

namespace world_base {

    template <typename T>
    class ObjectMap {
        protected:
            //simplifying dimensions by leaving (0,0) implicit
            coordinate dimensions;
            std::vector<std::vector<T>> map;
            T base_object;
        public:
            ObjectMap();
            ObjectMap (coordinate d, T base_object);
            std::vector<std::vector<T>> create_coordinates(coordinate dimensions, T b);
            std::vector<coordinate> get_all_coordinates();
            int coordinate_outside_dimensions(coordinate p);
            std::vector<coordinate> get_adjacent_coordinates(coordinate p, bool within_dimensions=false, bool nondiagonal=false);
            T get_coordinate_value(coordinate p);
            int set_coordinate_value(coordinate p, T value);
            float get_distance(coordinate p1, coordinate p2);
            float get_distance(fvector v1, fvector v2);
            float base_vector_angle(coordinate v1, coordinate v2);
            //fvector resize_vector(fvector v, float length);   -> not called in world_creation.py
            fvector standardize_vector(fvector v);
            coordinate get_expanded_dimensions(int factor);
            coordinate get_dimensions();
    };
}

#endif