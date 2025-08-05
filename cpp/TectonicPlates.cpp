#include "TectonicPlates.hpp"

namespace world_base {
    
    TectonicPlates::TectonicPlates(coordinate d) {
        dimensions = d;
        plate_map = SetMap(dimensions, {});
        plate_id = 0;
        ObjectMap<bool>(d, false) m;
        boundary_map = m;
    }


    std::set<int> TectonicPlates::get_all_neighbor_values(coordinate c) {
        std::set<int> values;
        for (auto n: plate_map.get_adjacent_coordinates(c, true, false))
            values.merge(plate_map.get_coordinate_value(n));
        return values;
    }


    void TectonicPlates::fill_plate_boundaries() {
        for (int y=0; y<dimensions.y; y++) {
            for (int x=0; x<dimensions.x; x++) {
                if (plate_map.get_coordinate_value({x,y}).size() == 0)
                    plate_map.update_coordinate_value({x,y}, get_all_neighbor_values({x,y}));
            }
        }
        return;
    }


    void TectonicPlates::spread_value_within_boundary(SetMap *split_map, int value, coordinate start) {
        std::set<coordinate> next_round{start};
        while (next_round.size() > 0) {
            std::set<coordinate> neighbors;
            for (auto c: next_round) {
                plate_map.add_coordinate_value(c, value);
                for (auto p: plate_map.get_adjacent_coordinates(c, true, true))
                    if ((*split_map).get_coordinate_value(p).size() == 0   //coordinate is not part of a split
                    && plate_map.get_coordinate_value(p).size() == 0)   //coordinate is not already filled
                        neighbors.insert(p);
            }
            next_round = neighbors;
            //~neighbors(); //destructor necessary???
        }
    }            


    void TectonicPlates::generate_from_splits(SetMap *split_map) {
        for (int y=0; y<dimensions.y; y++) {
            for (int x=0; x<dimensions.x; x++) {
                if ((*split_map).get_coordinate_value({x,y}).size() > 0)
                    continue;
                if (plate_map.get_coordinate_value({x,y}).size() == 0) {
                    spread_value_within_boundary(split_map, plate_id, {x,y});
                    plates.push_back({});
                    plate_id++;
                }
            }
        }
        fill_plate_boundaries();
        // create vectors containing coordinates of one plate, and one vector containing coordinates identified as boundaries
        // this will make several methods in other classes obsolete
        for (auto c: plate_map.get_all_coordinates()) {
            std::set<int> value = plate_map.get_coordinate_value(c);
            for (auto it = value.begin(); it != value.end(); ++it)
                plates.at(*it).push_back(c);
            if (value.size() > 1)
                boundary_map.set_coordinate_value(c, true);
                //boundaries.push_back(c);    //TODO: create an objectmap to make boundary lookup constant instead of linear
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
}