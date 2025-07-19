#include <vector>
#include "ObjectMap.hpp"
#ifndef _SETMAP_H_
#define _SETMAP_H_

namespace world_base {

class SetMap: public ObjectMap<std::set<int>> {
    public:
        using ObjectMap::ObjectMap;
        int add_coordinate_value(coordinate c, int value);
        int update_coordinate_value(coordinate c, std::set<int> value);
        int remove_coordinate_value(coordinate c, int value);
        std::vector<coordinate> get_neighbors_containing_value(coordinate c, int value);
        std::vector<coordinate> get_all_coordinates_containing_value(int value);
};
}
#endif