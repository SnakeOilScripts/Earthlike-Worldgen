#include "TectonicPlates.hpp"

namespace world_base {
    
    TectonicPlates::TectonicPlates() {

    }
    

    TectonicPlates::TectonicPlates(coordinate d) {
        dimensions = d;
        plate_map = SetMap(dimensions, {});
        plate_id = 0;
        ObjectMap<bool> m(d, false);
        boundary_map = m;
    }


    std::set<int> TectonicPlates::get_all_neighbor_values(coordinate c) {
        std::set<int> values;
        for (auto n: plate_map.get_adjacent_coordinates(c, true, false))
            values.merge(plate_map.get_coordinate_value(n));
        return values;
    }


    void TectonicPlates::spread_value_within_boundary(SetMap *split_map, int value, coordinate start) {
        std::set<coordinate> next_round{start};
        std::set<coordinate> neighbors;
        while (next_round.size() > 0) {
            neighbors = {};
            for (auto c: next_round) {
                plate_map.add_coordinate_value(c, value);
                for (auto p: plate_map.get_adjacent_coordinates(c, true, true)) {
                    if (split_map->get_coordinate_value(p).size() == 0 && plate_map.get_coordinate_value(p).size() == 0) {
                        //only insert neighbors that are not part of another plate or part of a split
                        neighbors.insert(p);
                    }
                }
            }
            next_round = neighbors;
            //~neighbors(); //destructor necessary???
        }
    }            


    void TectonicPlates::generate_from_splits(SetMap *split_map) {
        for (int y=0; y<dimensions.y; y++) {
            for (int x=0; x<dimensions.x; x++) {
                if (split_map->get_coordinate_value({x,y}).size() > 0)
                    continue;
                if (plate_map.get_coordinate_value({x,y}).size() == 0) {
                    spread_value_within_boundary(split_map, plate_id, {x,y});
                    plates.push_back({});
                    plate_id++;
                }
            }
        }
        // create vectors containing coordinates of one plate, and one vector containing coordinates identified as boundaries
        // this will make several methods in other classes obsolete
        for (auto c: plate_map.get_all_coordinates()) {
            std::set<int> value = plate_map.get_coordinate_value(c);
            if (value.size() > 0) {
            auto min = std::min_element(value.begin(), value.end());
            plates.at(*min).push_back(c);
            }
            // assign split coordinates to plates without changing the split_map (ensures proper neighbor relations)
            if (split_map->get_coordinate_value(c).size() > 0) {
                boundary_map.set_coordinate_value(c, true);
                auto all_neighbor_values = get_all_neighbor_values(c);
                auto min = std::min_element(all_neighbor_values.begin(), all_neighbor_values.end());
                plates.at(*min).push_back(c);
            }
        }
        return;
    }


    std::vector<coordinate> TectonicPlates::get_plate(int id) {
        return plates.at(id);
    }


    bool TectonicPlates::is_boundary(coordinate c) {
        return boundary_map.get_coordinate_value(c);
    }


    int TectonicPlates::get_plate_count() {
        return plate_id;
    }

    std::set<int> TectonicPlates::get_coordinate_value(coordinate c) {
        return plate_map.get_coordinate_value(c);
    }

    void TectonicPlates::print_plate(int id) {
        auto plate = plates.at(id);
        coordinate c{};
        bool found = false;
        while (c.y < dimensions.y) {
            while (c.x<dimensions.x) {
                for (auto p:plate) {
                    if (p == c)
                        found = true;
                }
                if (found)
                    std::cout<<"#";
                else
                    std::cout<<":";
                found = false;
                c.x++;
            }
            std::cout<<"\n";
            c.x=0;
            c.y++;
        }
    }

}