#include "Split.hpp"

namespace world_base {

    Split::Split() {

    }


    Split::Split(SetMap *map, int value, std::vector<coordinate> base) {
        shared_map = map;
        id = value;
        coordinates = base;
    }


    int Split::add_point(coordinate c) {
        //push back or push front depending on which end the neighbor is
        for (auto p: shared_map->get_adjacent_coordinates(coordinates.front(), true, false)) {
            if (p == c) {
                coordinates.insert(coordinates.begin(), c);
                shared_map->add_coordinate_value(c, id);
                return 0;
            }
        }
        for (auto p: shared_map->get_adjacent_coordinates(coordinates.back(), true, false)) {
            if (p == c) {
                coordinates.push_back(c);
                shared_map->add_coordinate_value(c, id);
                return 0;
            }
        }
        return -1;
    }


    coordinate Split::get_center() {
        coordinate v;
        v.x = static_cast<int>((coordinates.front().x - coordinates.back().x)/2);
        v.y = static_cast<int>((coordinates.front().y - coordinates.back().y)/2);
        v += coordinates.front();
        return v;
    }


    float Split::get_center_distance(coordinate c) {
        coordinate center = get_center();
        return shared_map->get_distance(center, c);
    }


    bool Split::end_inactive(coordinate end) {
        for (auto p: shared_map->get_adjacent_coordinates(end, false, false)) {
            if (shared_map->coordinate_outside_dimensions(p))
                return true;
            std::set<int> value = shared_map->get_coordinate_value(p);
            if(value.size() != 0 && value.find(id) != value.end())
                return true;
        }
        return false;
    }


    std::vector<coordinate> Split::get_active_ends() {
        std::vector<coordinate> v;
        if (!end_inactive(coordinates.front()))
            v.push_back(coordinates.front());
        if (!end_inactive(coordinates.back()))
            v.push_back(coordinates.back());
        return v;
    }


    bool Split::is_active() {
        return (get_active_ends().size() > 0);
    }


    void Split::backtrack_end(coordinate c) {
        if (c == coordinates.front()) {
            shared_map->remove_coordinate_value(c, id);
            coordinates.erase(coordinates.begin());
            option_blacklist.insert(c);
        } else if (c == coordinates.back()) {
            shared_map->remove_coordinate_value(c, id);
            coordinates.pop_back();
            option_blacklist.insert(c);
        }
        return;
    }


    coordinate Split::get_nth_end_neighbor(coordinate end, int n) {
        if (end == coordinates.front()) {
            if (coordinates.size() <= n+1) {
                return coordinates.back();
            } else {
                auto it = coordinates.begin();
                it += n;
                return *it;
            }
        } else if (end == coordinates.back()) {
            if (coordinates.size() <= n+1) {
                return coordinates.front();
            } else {
                auto it = coordinates.end();
                it -= (n+1);
                return *it;
            }
        }
        //to keep the compiler silent ;)
        return {0,0};
    }


    float Split::angle_towards_nth_end_neighbor(coordinate end, int n, coordinate c) {
        coordinate nth_neighbor = get_nth_end_neighbor(end, n);
        coordinate end_vector = end - nth_neighbor;
        coordinate angled_vector = c - nth_neighbor;
        return shared_map->base_vector_angle(end_vector, angled_vector);
    }

}