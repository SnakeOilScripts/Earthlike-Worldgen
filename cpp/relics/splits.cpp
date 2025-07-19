#include <iostream>
#include <cstdlib>
#include <algorithm>
#include "coordinates.cpp"

namespace world_base {

    class Split{
        private:
            SetMap *shared_map;
            std::vector<coordinate> coordinates;
            //TODO: use vector instead of set here
        public:
            int id;
            std::set<coordinate> option_blacklist;
            Split() {

            }


            Split(SetMap *map, int value, std::vector<coordinate> base) {
                shared_map = map;
                id = value;
                coordinates = base;
            }


            int add_point(coordinate c) {
                //push back or push front depending on which end the neighbor is
                for (auto p: (*shared_map).get_adjacent_coordinates(coordinates.front(), true, false)) {
                    if (p == c) {
                        coordinates.insert(coordinates.begin(), c);
                        (*shared_map).add_coordinate_value(c, id);
                        return 0;
                    }
                }
                for (auto p: (*shared_map).get_adjacent_coordinates(coordinates.back(), true, false)) {
                    if (p == c) {
                        coordinates.push_back(c);
                        (*shared_map).add_coordinate_value(c, id);
                        return 0;
                    }
                }
                return -1;
            }


            coordinate get_center() {
                coordinate v;
                v.x = static_cast<int>((coordinates.front().x - coordinates.back().x)/2);
                v.y = static_cast<int>((coordinates.front().y - coordinates.back().y)/2);
                v += coordinates.front();
                return v;
            }


            float get_center_distance(coordinate c) {
                coordinate center = get_center();
                return (*shared_map).get_distance(center, c);
            }


            bool end_inactive(coordinate end) {
                for (auto p: (*shared_map).get_adjacent_coordinates(end, false, false)) {
                    if ((*shared_map).coordinate_outside_dimensions(p))
                        return true;
                    std::set<int> value = (*shared_map).get_coordinate_value(p);
                    if(value.size() != 0 && value.find(id) != value.end())
                        return true;
                }
                return false;
            }


            std::vector<coordinate> get_active_ends() {
                std::vector<coordinate> v;
                if (!end_inactive(coordinates.front()))
                    v.push_back(coordinates.front());
                if (!end_inactive(coordinates.back()))
                    v.push_back(coordinates.back());
                return v;
            }

            bool is_active() {
                return (get_active_ends().size() > 0);
            }


            void backtrack_end(coordinate c) {
                if (c == coordinates.front()) {
                    (*shared_map).remove_coordinate_value(c, id);
                    coordinates.erase(coordinates.begin());
                    option_blacklist.insert(c);
                } else if (c == coordinates.back()) {
                    (*shared_map).remove_coordinate_value(c, id);
                    coordinates.pop_back();
                    option_blacklist.insert(c);
                }
                return;
            }


            coordinate get_nth_end_neighbor(coordinate end, int n) {
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

            }

            float angle_towards_nth_end_neighbor(coordinate end, int n, coordinate c) {
                coordinate nth_neighbor = get_nth_end_neighbor(end, n);
                coordinate end_vector = end - nth_neighbor;
                coordinate angled_vector = c - nth_neighbor;
                return (*shared_map).base_vector_angle(end_vector, angled_vector);
            }
    };


    class TectonicSplits {
        
        private:

            coordinate dimensions;
            float direction_change_rate;
            int direction_len;
            int split_id;
            SetMap split_map;
            std::vector<Split> splits;

        public:

            TectonicSplits(coordinate d, float dcr=0.25, int d_len=8) {
                dimensions = d;
                direction_change_rate = dcr;
                direction_len = d_len;
                split_id = 0;
                std::set<int> s;
                split_map = SetMap(dimensions, s);
            }


            void initialize_split(coordinate base) {
                coordinate first_neighbor;
                std::vector<coordinate> options = split_map.get_adjacent_coordinates(base, true, false);
                first_neighbor = options.at(rand() % options.size());
                std::vector<coordinate> init;
                init.push_back(base);
                init.push_back(first_neighbor);
                Split s(&split_map, split_id, init);
                split_id++;
                splits.push_back(s);
                return;
            }


            void add_initial_split(float min_split_distance, int max_attempts=100) {
                bool rejected;
                coordinate new_center;
                for(int i=0; i<max_attempts; i++) {
                    rejected = false;
                    new_center = {rand() % dimensions.x, rand() % dimensions.y};
                    for (auto s: splits) {
                        if(s.get_center_distance(new_center) < min_split_distance) {
                            rejected = true;
                            break;
                        }
                    }
                    if (!rejected) {
                        initialize_split(new_center);
                    }
                }
                return;
            }


            std::vector<Split> get_active_splits() {
                std::vector<Split> ret;
                for (auto s: splits) {
                    if (s.is_active())
                        ret.push_back(s);
                }
                return ret;
            }

            std::vector<coordinate> get_split_options(Split s, coordinate end) {
                int dl = direction_len;
                std::vector<coordinate> ret;
                for (auto c: split_map.get_adjacent_coordinates(end, true, false)) {
                    if (split_map.get_neighbors_containing_value(c, s.id).size() >= 2) {
                        //no loopbacks or 90 degree angles
                        continue;
                    } else if (split_map.get_coordinate_value(c).find(s.id) != split_map.get_coordinate_value(c).end()) {
                        //no re-adding of existing points
                        continue;
                    } else if (s.option_blacklist.find(c) != s.option_blacklist.end()) {
                        //guarantee that after backtracking, impossible points are not explored again
                        continue;
                    }
                    ret.push_back(c);
                }
                if (ret.size() == 0) {
                        s.backtrack_end(end);
                        return ret;
                }
                std::sort(ret.begin(), ret.end(), [&s, end, dl](coordinate a, coordinate b){
                    return (s.angle_towards_nth_end_neighbor(end, dl, a) < s.angle_towards_nth_end_neighbor(end, dl, b));
                });
                coordinate bias_option = ret.at(0);
                if (ret.size() > 1) {
                    int bias_option_length = static_cast<int>(float(ret.size()-1) * direction_change_rate);
                    for (int i=1; i<bias_option_length; i++)    //i=1 because one bias option is already present
                        ret.push_back(bias_option);
                }
                return ret;
            }

            int develop_splits() {
                std::vector<Split> active = get_active_splits();
                if (active.size() == 0)
                    return 1;
                Split choice = active.at(rand() % active.size());
                coordinate chosen_end = choice.get_active_ends().at(choice.get_active_ends().size());
                std::vector<coordinate> options = get_split_options(choice, chosen_end);
                if (options.size() == 0)
                    return 0;
                coordinate chosen_option = options.at(rand() % options.size());
                choice.add_point(chosen_option);
                return 0;
            }
            
            
            
    };

}