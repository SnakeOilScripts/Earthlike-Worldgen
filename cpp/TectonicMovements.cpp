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
        for (auto it=hotspots.begin(); it!=hotspots.end(); ++it) {
            while (it->second <= 0) //lifespan <= 0
                hotspots.erase(it);
        }
        for (int i=0; i<n_hotspots-hotspots.size(); i++) {
            hotspots.push_back(generate_hotspot());           //idgaf anymore if two hotspots share the same coordinates
        }
    }

    
    void TectonicMovements::apply_hotspots() {
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
        for (auto it=available_neighbors.begin(); it!=available_neighbors.end(); ++it) {
            helper = ctofv(*it);
            while (map_helper.get_distance(goal_point, helper) >= 1) {
                available_neighbors.erase(it);
            }
        }
        if (available_neighbors.size() == 0) {
    
        } else if (available_neighbors.size() == 1) {
            std::pair<coordinate,float> p;
            p.first.x = static_cast<float>(available_neighbors[0].x);
            p.first.y = static_cast<float>(available_neighbors[0].y);
            p.second = 1.0;
            ret.push_back(p);
        } else if (available_neighbors.size() == 2) {
            float sum_distance = map_helper.get_distance(goal_point, ctofv(available_neighbors[0])) + map_helper.get_distance(goal_point, ctofv(available_neighbors[1]));
            for (auto n:available_neighbors) {
                std::pair<coordinate,float> p;
                p.first = n;
                p.second = static_cast<int>(100.0 * map_helper.get_distance(goal_point, ctofv(n)) / sum_distance) / 100.0;  //round to second decimal
                ret.push_back(p);
            }
        }
        return ret;
    }


    /*bool TectonicMovements::is_boundary(coordinate c) {
        return plates_object->is_boundary(c);
    }*/


    std::string TectonicMovements::identify_interaction(coordinate from, coordinate to) {
        int from_plateid, to_plateid;
        from_plateid = *(plates_object->get_coordinate_value(from).begin());
        if (plates_object->get_coordinate_value(to).empty())
            return "transform";
        to_plateid = *(plates_object->get_coordinate_value(to).begin());
        
        if (from_plateid == to_plateid) {
            if (plates_object->is_boundary(from) && plates_object->is_boundary(to)) {
                return "transform";
            } else if (plates_object->is_boundary(from)) {
                return "divergent";
            } else {
                return "transfer";
            }
        } else {
            if (geology_object->get_height(from) <= geology_object->get_height(to)*subduction_requirement) {
                return "subduction";
            } else {
                return "convergent";
            }
        }
    }


    void TectonicMovements::point_interaction(coordinate from, coordinate to, std::string interaction_type, float ratio) {
        geology_object->point_interaction(from, to, interaction_type, ratio);
    }


    void TectonicMovements::apply_changes() {
        geology_object->apply_changes();
    }


    void TectonicMovements::apply_volcanism(coordinate c) {
        if (((float)rand())/RAND_MAX <= volcanism_chance)
            geology_object->apply_volcanism(c);
    }


    void TectonicMovements::simulate_plate_movement() {
        int plate_id = rand() % plates_object->get_plate_count();
        std::cout<<"picked plate id\n";
        auto plate = plates_object->get_plate(plate_id);
        std::cout<<"obtained plate coordinates vector\n";
        fvector plate_movement = geology_object->generate_magma_current_vector(&plate);
        std::cout<<"obtained movement vector\n";
        apply_vector_to_plate(plate_movement, plate);
        std::cout<<"applied vector to plate\n";
        geology_object->increment_cycle_ticker();
        std::cout<<"incremented cycle ticker\n";
        apply_hotspots();
        std::cout<<"applied hotspots\n";
        manage_hotspots();
        std::cout<<"managed_hotspots\n";
        apply_changes();
        std::cout<<"applied changes\n";
    }


    void TectonicMovements::apply_vector_to_plate(fvector v, std::vector<coordinate> plate) {
        std::string interaction_type;
        for (auto c:plate) {
            auto interactions = get_neighbor_interactions(c, v);
            for (auto interaction:interactions) {
                interaction_type = identify_interaction(c, interaction.first);
                point_interaction(c, interaction.first, interaction_type, interaction.second);
                if (interaction_type.compare("divergent") == 0)
                    apply_volcanism(c);
                else if (interaction_type.compare("subduction") == 0)
                    apply_volcanism(interaction.first);
            }
        }
    }

}