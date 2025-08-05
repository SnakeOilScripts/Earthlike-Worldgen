#include "TectonicMovements.hpp"

namespace world_base {

    TectonicMovements::TectonicMovements() {

    }


    TectonicMovements::TectonicMovements(coordinate d, TectonicPlates *p, Geology *g) {
        plates_object = p;
        geology_object = g;
        map_helper = ObjectMap<bool>({1,1}, false);
        subduction_requirement = 0.1;
        volcanism_chance = 0.2;
        n_hotspots = 5;
        hotspot_min_age = 50;
        hotspot_max_age = 500;
        dimensions = d;

        for(int i=0; i<p->get_plate_count(); i++)
            plate_coordinates.push_back(p->get_plate(i));

    }


    std::pair<coordinate,int> TectonicMovements::generate_hotspot() {
        std::pair<coordinate,int> hotspot;
        hotspot.first = {rand() % dimensions.x, rand() % dimensions.y};
        hotspot.second = hotspot_min_age + (rand() % (hotspot_max_age - hotspot_min_age));
        return hotspot;
    }


    void TectonicMovements::manage_hotspots() {
        for (auto it=hotspots.begin(); it!=hotspots.end(); i++) {
            while (*it.second <= 0) //lifespan <= 0
                hotspots.erase(it);
        }
        for (int i=0; i<n_hotspots-hotspots.size(); i++) {
            hotspots.push_back(generate_hotspot);           //idgaf anymore if two hotspots share the same coordinates
        }
    }

    
    void TectonicMovements::apply_hotspot() {
        for (auto h:hotspots) {
            apply_volcanism(h.first);
            h.second--;
        }
    }


    std::vector<std::pair<coordinate,float>> TectonicMovements::get_neighbor_interactions(coordinate c, fvector v) {
        std::vector<std::pair<coordinate,float>> ret;
        fvector goal_point, helper;
        goal_point = {v.x + c.x, v.y + c.y};
        auto available_neighbors = map_helper.get_adjacent_coordinates(c, false, false);    //out-of-bounds interactions are handled later
        for (auto it=available_neighbors.begin(); it!=available_neighbors.end(); it++) {
            helper = ctofv(*it);
            while (map_helper.get_distance(goal_point, helper) >= 1) {
                available_neighbors.erase(*it);
            }
        }
        if (available_neighbors.size() == 0) {
    
        } else if (available_neighbors.size() == 1) {
            std::pair<coordinate,float> p;
            p.first.x = static_cast<float>available_neighbors[0].x;
            p.first.y = static_cast<float>available_neighbors[0].y;
            p.second = 1.0;
            ret.push_back(p);
        } else if (available_neighbors.size() == 2) {
            float sum_distance = map_helper.get_distance(goal_point, ctovf(available_neighbors[0])) + map_helper.get_distance(goal-point, ctovf(available_neighbors[1]));
            for (auto n:available_neighbors) {
                std::pair<coordinate,float> p;
                p.first = n;
                p.second = static_cast<int>(100.0 * map_helper.get_distance(goal_point, ctofv(n)) / sum_distance) / 100.0;  //round to second decimal
                ret.push_back(p);
            }
        }
        return ret;
    }


    bool TectonicMovements::is_boundary(coordinate c) {
        return plates_object->is_boundary(c);
    }


    std::string TectonicMovements::identify_interaction(coordinate from, coordinate to) {

    }


    void TectonicMovements::point_interaction(coordinate from, coordinate to, std::string interaction_type, float ratio) {

    }


    void TectonicMovements::apply_changes() {

    }


    void TectonicMovements::apply_volcanism(coordinate c) {

    }


    void TectonicMovements::simulate_plate_movement() {

    }


    void TectonicMovements::apply_vector_to_plate(fvector v, int plate_id) {

    }

}