#include "UpdateMap.hpp"

namespace world_base {
    template <typename T>
    UpdateMap<T>::UpdateMap(coordinate d, T base_object) {
        dimensions = d;
        update_dimensions = d;
        map = create_map(d, base_object);
        update = create_map(d, base_object);
    }


    template <typename T>
    ObjectMap<T> UpdateMap<T>::create_map(coordinate d, T base_object) {
        ObjectMap<T> m(d, base_object);
        return m;
    }

    // requires the base_object to have a + and += operator defined!!! especially for new structs
    template <typename T>
    void UpdateMap<T>::increment_coordinate_value(coordinate c, T value) {
        T inc;
        if (!update.coordinate_outside_dimensions(c)) {
            inc = update.get_coordinate_value(c);
            update.set_coordinate_value(c, inc + value);
        }
    }


    template <typename T>
    void UpdateMap<T>::apply_changes() {
        map = update;
        dimensions = update_dimensions;
    }


    template <typename T>
    T UpdateMap<T>::get_coordinate_value(coordinate c) {
        return map.get_coordinate_value(c);
    }
}