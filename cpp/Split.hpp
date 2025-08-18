#include <vector>
#include "coordinate.hpp"
#include "SetMap.hpp"

#ifndef _SPLIT_H_
#define _SPLIT_H_

namespace world_base {

    class Split{
        protected:
            SetMap *shared_map;
            std::vector<coordinate> coordinates;
            //TODO: use vector instead of set here
        public:
            int id;
            std::set<coordinate> option_blacklist;
            Split();
            Split(SetMap *map, int value, std::vector<coordinate> base);
            int add_point(coordinate c);
            coordinate get_center();
            float get_center_distance(coordinate c);
            bool end_inactive(coordinate end);
            std::vector<coordinate> get_active_ends();
            bool is_active();
            bool coordinate_blacklisted(coordinate c);
            void backtrack_end(coordinate c);
            coordinate get_nth_end_neighbor(coordinate end, int n);
            float angle_towards_nth_end_neighbor(coordinate end, int n, coordinate c);
    };
}
#endif