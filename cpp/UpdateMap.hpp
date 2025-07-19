#include <vector>
#include "ObjectMap.hpp"

#ifndef _UPDATEMAP_H_
#define _UPDATEMAP_H_

// TODO make it fully inherit from ObjectMap

namespace world_base {

    template <typename T>
    class UpdateMap {
        private:
            ObjectMap<T> map;
            ObjectMap<T> update;
        public:
            coordinate dimensions;
            coordinate update_dimensions;
            UpdateMap(coordinate d, T base_object);
            ObjectMap<T> create_map(coordinate d, T base_object);
            // requires the base_object to have a + and += operator defined!!! especially for new structs
            void increment_coordinate_value(coordinate c, T value);
            void apply_changes();
            T get_coordinate_value(coordinate c);
};

}
#endif