#include "UpdateMap.hpp"

// Note to self: class template inheriting from another class template has no access to parent attributes, unless specified with this-> pointer!!!

namespace world_base {
    template <typename T>
    UpdateMap<T>::UpdateMap(coordinate d, T base_object) {
        this->dimensions = d;
        update_dimensions = d;
        this->map = this->create_coordinates(d, base_object);
        update = this->create_coordinates(d, base_object);
    }


    template <typename T>
    bool UpdateMap<T>::update_coordinate_outside_dimensions(coordinate p) {
        return (p.x<0 || p.y<0 || p.x >= update_dimensions.x || p.y >= update_dimensions.y);
    }


    // requires the base_object to have a + and += operator defined!!! especially for new structs
    template <typename T>
    void UpdateMap<T>::increment_coordinate_value(coordinate c, T value) {
        T inc;
        if (!(this->update_coordinate_outside_dimensions(c))) {
            inc = update.at(c.x).at(c.y);
            update.at(c.x).at(c.y)= inc + value;
        }
    }


    template <typename T>
    void UpdateMap<T>::apply_changes() {
        this->map = update;
        this->dimensions = update_dimensions;
    }


    template <typename T>
    float UpdateMap<T>::normal_pdf(float x, float mean, float standard_deviation) {
        static const float inv_sqrt_2pi = 0.3989422804014327;
        float a = (x - mean) / standard_deviation;
        return inv_sqrt_2pi / standard_deviation * std::exp(-0.5f * a * a);
    }


    template <typename T>
    void UpdateMap<T>::transitional_gaussian_dimensions_expansion(int expansion_factor, T base_object) {
        float standard_deviation = expansion_factor/2.0;
        T multiplier;
        std::vector<std::vector<float>> dp;
        std::vector<coordinate> all_coordinates = this->get_all_coordinates();
        for (int x=0; x<expansion_factor*3; x++) {
            std::vector<float> row;
            dp.push_back(row);
            for (int y=0; y<expansion_factor*3; y++) {
                dp.at(x).push_back(normal_pdf(x+1, expansion_factor + (expansion_factor+1)/2, standard_deviation) + normal_pdf(y+1, expansion_factor + (expansion_factor+1)/2, standard_deviation));
            }
        }
        update_dimensions = this->get_expanded_dimensions(expansion_factor);
        update = this->create_coordinates(update_dimensions, base_object);
        for (auto it=all_coordinates.begin(); it!=all_coordinates.end(); ++it) {
            multiplier = this->get_coordinate_value(*it);
            for (int x=0; x<expansion_factor*3; x++) {
                for (int y=0; y<expansion_factor*3; y++) {
                    increment_gaussian_coordinate(*it, x, y, expansion_factor, &dp, multiplier);
                }
            }
        }
        apply_changes();
    }


    template <typename T>
    void UpdateMap<T>::increment_gaussian_coordinate(coordinate c, int x, int y, int expansion_factor, std::vector<std::vector<float>> *dp, T value) {
        coordinate adjusted_coordinate = c;
        adjusted_coordinate.x -= 1;
        adjusted_coordinate.x = adjusted_coordinate.x * expansion_factor + x;
        adjusted_coordinate.y -= 1;
        adjusted_coordinate.y = adjusted_coordinate.y * expansion_factor + y;
        increment_coordinate_value(adjusted_coordinate, ((dp->at(x).at(y)) * value) *(1.0));     //using *0.33 to avoid needing another operator for geodat struct
        //NOTE: using * (1/3) casts 1/3 into an integer, which is 0, and THEN multiplies is, always resulting in 0
    }

}