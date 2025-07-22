#include <vector>
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
};

}
#endif