#include "ObjectMap.hpp"

namespace world_base {
    template <typename T>

    ObjectMap<T>::ObjectMap() {
                
    }

    template <typename T>
    ObjectMap<T>::ObjectMap(coordinate d, T b) {
        dimensions = d;
        map = create_coordinates(dimensions, b);
        base_object = b;
    }


    template <typename T>
    std::vector<std::vector<T>> ObjectMap<T>::create_coordinates(coordinate dimensions, T base_object) {
        std::vector<std::vector<T>> m;
        for (int x=0; x<dimensions.x; x++) {
            std::vector<T> v;
            m.push_back(v);
            for (int y=0; y<dimensions.y; y++) {
                m.at(x).push_back(base_object);
            }
        }
        return m;
    }

    template <typename T>
    std::vector<coordinate> ObjectMap<T>::get_all_coordinates() {
        std::vector<coordinate> v;
        for (int x=0; x<dimensions.x; x++) {
            for (int y=0; y<dimensions.y; y++) {
                coordinate c = {x,y};
                v.push_back(c);
            }
        }
        return v;
    }

    template <typename T>
    bool ObjectMap<T>::coordinate_outside_dimensions(coordinate p) {
        if (p.x < 0 || p.y < 0)
            return true;
        else if (p.x >= dimensions.x || p.y >= dimensions.y)
            return true;
        else
            return false;
    }

    template <typename T>
    std::vector<coordinate> ObjectMap<T>::get_adjacent_coordinates(coordinate p, bool within_dimensions, bool nondiagonal) {
        std::vector<coordinate> v;
        for (int x=p.x-1; x<=p.x+1; x++) {
            for (int y=p.y-1; y<=p.y+1; y++) {
                coordinate c = {x,y};
                if (within_dimensions && coordinate_outside_dimensions(c)) {
                    continue;
                }
                if (nondiagonal && (x != p.x && y != p.y)) {
                    continue;
                }
                if (c.x == p.x && c.y == p.y) {
                    continue;
                }
                v.push_back(c);
            }
        }
        return v;
    }

    template <typename T>
    T ObjectMap<T>::get_coordinate_value(coordinate p) {
        if (coordinate_outside_dimensions(p) == true)
            return base_object;
        else 
            return map.at(p.x).at(p.y);
    }

    template <typename T>
    int ObjectMap<T>::set_coordinate_value(coordinate p, T value) {
        if (coordinate_outside_dimensions(p) == true) {
            return -1;
        }
        map.at(p.x).at(p.y) = value;
        return 0;
    }

    template <typename T>
    float ObjectMap<T>::get_distance(coordinate p1, coordinate p2) {
        return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
    }

    template <typename T>
    float ObjectMap<T>::get_distance(fvector v1, fvector v2) {
        return std::sqrt(std::pow(v1.x - v2.x, 2) + std::pow(v1.y - v2.y, 2));
    }

    template <typename T>
    float ObjectMap<T>::base_vector_angle(coordinate v1, coordinate v2) {
        coordinate base = {0,0};
        float d1 = get_distance(base, v1);
        float d2 = get_distance(base, v2);
        float dot_product = v1.x * v2.x + v1.y * v2.y;
        // improvising a rounding to 2nd decimal
        //float angle = std::round(std::acos((dot_product / (d1*d2)) * std::pow(10, 2))) * std::pow(10, 2);
        float angle = std::round(std::acos(dot_product / (d1*d2)) * std::pow(10, 2)) / std::pow(10,2);
        return angle;
    }
    /*
    template <typename T>
    fvector ObjectMap<T>::resize_vector(fvector v, float length) {
        fvector b = {0.0,0.0};
        if (get_distance(b, v) == 0)
            return b;
        vector r = {v.x * (length / get_distance(b, v)), v.y * (length / get_distance(b, v))};
        return r;
    }
    */

    template <typename T>
    fvector ObjectMap<T>::standardize_vector(fvector v) {
        fvector ret = {};
        if (v.x == 0 and v.y != 0) {
            ret.y = v.y/std::abs(v.y);
        }
        else if (v.x != 0 and v.y == 0) {
            ret.x = v.x/std::abs(v.x);
        }
        else if (v.x == 0 and v.y == 0) {
            
        }
        else if (std::abs(v.x) > std::abs(v.y)) {
            ret.x = v.x/std::abs(v.x);
            ret.y = v.y/std::abs(v.x);
        }
        else {
            ret.x = v.x/std::abs(v.y);
            ret.y = v.y/std::abs(v.y);
        }
        return ret;
    }

    template <typename T>
    coordinate ObjectMap<T>::get_expanded_dimensions(int factor) {
        coordinate d = dimensions;
        d.x *= factor;
        d.y *= factor;
        return d;
    }


    template <typename T>
    coordinate ObjectMap<T>::get_dimensions() {
        return dimensions;
    }
}