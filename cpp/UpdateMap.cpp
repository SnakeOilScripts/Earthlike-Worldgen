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


    // requires the base_object to have a + and += operator defined!!! especially for new structs
    template <typename T>
    void UpdateMap<T>::increment_coordinate_value(coordinate c, T value) {
        T inc;
        if (!update.coordinate_outside_dimensions(c)) {
            inc = this->get_coordinate_value(c);
            update.at(c.x).at(c.y)= inc + value;
        }
    }


    template <typename T>
    void UpdateMap<T>::apply_changes() {
        this->map = update;
        this->dimensions = update_dimensions;
    }

}