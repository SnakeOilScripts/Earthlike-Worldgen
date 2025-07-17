#include "splits.cpp"

namespace world_base {


    class TectonicPlates {
        
        private:
            coordinate dimensions;
            SetMap plate_map;
            int plate_id;
            std::vector<std::vector<coordinate>> plates;
        public:
        
            TectonicPlates(coordinate d) {
                dimensions = d;
                plate_map = SetMap(dimensions, {});
                plate_id = 0;
            }


            std::set<coordinate> get_all_neighbor_values(coordinate c) {
                std::set<int> values;
                for (auto n: plate_map.get_adjacent_coordinates(c, true, false))
                    values.merge(plate_map.get_coordinate_value(n));
                return values;
            }


            void fill_plate_boundaries() {
                for (int y=0; y<dimensions.y; y++) {
                    for (int x=0; x<dimensions.x; x++) {
                        if(plate_map.get_coordinate_value({x,y}).size() == 0)
                            plate_map.update_coordinate_value({x,y}, get_all_neighbor_values([x,y]));
                    }
                }
                return;
            }


            void spread_value_within_boundary(SetMap *split_map, int value, coordinate start) {
                std::set<coordinate> next_round{start};
                while (next_round.size() > 0) {
                    std::set<coordinate> neighbors;
                    for (auto c: next_round) {
                        plate_map.add_coordinate_value(c, value);
                        for (auto p: plate_map.get_adjacent_coordinates(c, true, true))
                            if (split_map.get_coordinate_value(p).size() == 0   //coordinate is not part of a split
                            && plate_map.get_coordinate_value(p).size() == 0)   //coordinate is not already filled
                                neighbors.insert(p);
                    }
                    next_round = neighbors;
                    //~neighbors(); //destructor necessary???
                }
            }            


            void generate_from_splits(SetMap *split_map) {
                for (int y=0; y<dimensions.y; y++) {
                    for (int x=0; x<dimensions.x, x++) {
                        if ((*split_map).get_coordinate_value({x,y}).size() > 0)
                            continue;
                        if (plate_map.get_coordinate_value({x,y}).size() == 0) {
                            spread_value_within_boundary(split_map, plate_id, {x,y});
                            plate_id++;
                        }
                    }
                }
                fill_plate_boundaries();
                return;
            }


            coordinate get_plate_direction() {}


            std::set<coordinate> get_coordinate_value(coordinate c) {
                return plate_map.get_coordinate_value(c);
            }
    };

}