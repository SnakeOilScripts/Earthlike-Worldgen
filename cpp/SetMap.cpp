#include "SetMap.hpp"

namespace world_base {

    int SetMap::add_coordinate_value(coordinate c, int value) {
        if (coordinate_outside_dimensions(c))
            return -1;
        map.at(c.x).at(c.y).insert(value);
        return 0;
    }


    int SetMap::update_coordinate_value(coordinate c, std::set<int> value) {
        if (coordinate_outside_dimensions(c))
            return -1;
        map.at(c.x).at(c.y).merge(value);
        return 0;
    }


    int SetMap::remove_coordinate_value(coordinate c, int value) {
        if (coordinate_outside_dimensions(c))
            return -1;
        map.at(c.x).at(c.y).erase(value);
        return 0;
    }

    
    std::vector<coordinate> SetMap::get_neighbors_containing_value(coordinate c, int value) {
        std::vector<coordinate> v;
        std::vector<coordinate> ret;
        if (coordinate_outside_dimensions(c))
            return ret;
        v = get_adjacent_coordinates(c, true);
        std::cout<<"___\n";
        for (auto it = v.begin(); it != v.end(); ++it) {
            std::set<int> current_set = map.at(it->x).at(it->y);
            if (current_set.find(value) != current_set.end())
                ret.push_back(*it);
        }
        return ret;
    }


    std::vector<coordinate> SetMap::get_all_coordinates_containing_value(int value) {
        std::vector<coordinate> ret;
        std::vector<coordinate> all;

        all = get_all_coordinates();
        for (auto element: all) {
            std::set<int> current_set = map.at(element.x).at(element.y);
            if (current_set.find(value) != current_set.end())
                ret.push_back(element);
        }
        return ret;
    }

}