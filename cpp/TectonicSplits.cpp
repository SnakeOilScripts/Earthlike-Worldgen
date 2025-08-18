#include "TectonicSplits.hpp"

namespace world_base {

    TectonicSplits::TectonicSplits() {
        
    }


    TectonicSplits::TectonicSplits(coordinate d, float dcr, int d_len) {
        dimensions = d;
        direction_change_rate = dcr;
        direction_len = d_len;
        split_id = 0;
        std::set<int> s;
        split_map = SetMap(dimensions, s);
    }


    void TectonicSplits::initialize_split(coordinate base) {
        coordinate first_neighbor;
        std::vector<coordinate> options = split_map.get_adjacent_coordinates(base, true, false);
        first_neighbor = options.at(rand() % options.size());
        std::vector<coordinate> init;
        init.push_back(base);
        init.push_back(first_neighbor);
        split_map.add_coordinate_value(base, split_id);
        split_map.add_coordinate_value(first_neighbor, split_id);
        Split s(&split_map, split_id, init);
        split_id++;
        splits.push_back(s);
        return;
    }


    void TectonicSplits::add_initial_split(float min_split_distance, int max_attempts) {
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
                break;
            }
        }
        return;
    }


    std::vector<Split*> TectonicSplits::get_active_splits() {
        std::vector<Split*> ret;
        for (auto it=splits.begin(); it!=splits.end(); ++it) {
            if (it->is_active())
                ret.push_back(&(*it));
        }
        return ret;
    }

    
    std::vector<coordinate> TectonicSplits::get_split_options(Split *s, coordinate end) {
        int dl = direction_len;
        std::vector<coordinate> ret;
        for (auto c: split_map.get_adjacent_coordinates(end, true, false)) {
            if (split_map.get_neighbors_containing_value(c, s->id).size() >= 2) {
                //no loopbacks or 90 degree angles
                continue;
            } else if (split_map.coordinate_contains_value(c, s->id)) {
                //no re-adding of existing points
                continue;
            } else if (s->coordinate_blacklisted(c)) {
                //guarantee that after backtracking, impossible points are not explored again
                continue;
            }
            ret.push_back(c);
        }
        if (ret.size() == 0) {
                s->backtrack_end(end);
                return ret;
        }
        std::sort(ret.begin(), ret.end(), [&s, end, dl](coordinate a, coordinate b){
            return (s->angle_towards_nth_end_neighbor(end, dl, a) < s->angle_towards_nth_end_neighbor(end, dl, b));
        });
        coordinate bias_option = ret.at(0);
        if (ret.size() > 1) {
            int bias_option_length = static_cast<int>((ret.size()-1) / direction_change_rate) - (ret.size()-1);
            for (int i=1; i<bias_option_length; i++)    //i=1 because one bias option is already present
                ret.push_back(bias_option);
        }
        return ret;
    }


    int TectonicSplits::develop_splits() {
        std::vector<Split*> active = get_active_splits();
        if (active.size() == 0) {
            return 1;
        }

        Split *choice = active.at(rand() % active.size());
        coordinate chosen_end = choice->get_active_ends().at(rand() % choice->get_active_ends().size());
        std::vector<coordinate> options = get_split_options(choice, chosen_end);
        if (options.size() == 0) {
            return 0;
        }
        coordinate chosen_option = options.at(rand() % options.size());
        choice->add_point(chosen_option);
        return 0;
    }


    SetMap *TectonicSplits::get_split_map() {
        return &split_map;
    }


    void TectonicSplits::print_split_map() {
        coordinate p{};
        while (p.y < dimensions.y) {
            p.x=0;
            while (p.x < dimensions.x) {
                if (split_map.get_coordinate_value(p).size() > 0)
                    std::cout<<"#";
                else
                    std::cout<<":";
                p.x++;
            }
            std::cout<<"\n";
            p.y++;
        }
        for (int i=0; i<dimensions.x; i++)
            std::cout<<"_";
        std::cout<<"\n";
    }
}