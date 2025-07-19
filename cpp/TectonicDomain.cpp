#include "TectonicDomain.hpp"

namespace world_base {

    template <typename T>
    TectonicDomain<T>::TectonicDomain() {

    }


    template <typename T>
    TectonicDomain<T>::TectonicDomain(coordinate d, T b) {
        dimensions = d;
        T base_unit = b;
        value_map = UpdateMap<T>(dimensions, base_unit);
    }


    template <typename T>
    void TectonicDomain<T>::apply_volcanism(coordinate c) {
        value_map.increment_coordinate_value(c, get_transfer_unit(create_new_unit(), volcanism_potency));
    }


    template <typename T>
    T TectonicDomain<T>::get_transfer_unit(T value, float ratio) {
        //meant to be overwritten
        return value;
    }


    template <typename T>
    UpdateMap<T> TectonicDomain<T>::get_map() {
        return value_map;
    }


    template <typename T>
    void TectonicDomain<T>::apply_changes() {
        value_map.apply_changes();
    }


    /*
    point_interaction must check if the coordinate is within dimensions because of how the interaction calculation works
    having the plate boundary occupying a coordinate breaks all systems I could come up with, here is the new plan:
       - for a coordinate with more than one plate_id in it, it belongs to the plate of the lowest plate_id
       - the ACTUAL plate boundary is a line of thickness 0 between two coordinates
    */
    template <typename T>
    void TectonicDomain<T>::point_interaction(coordinate from, coordinate to, std::string mode, float ratio) {
        T transfer_unit = get_transfer_unit(value_map.get_coordinate_value(from), ratio);
        if (value_map.coordinate_outside_dimensions(to))
            falloff_interaction(to, transfer_unit);
        else if (mode.compare("transfer") == 0)
            transfer_interaction(from, to, transfer_unit);
        else if (mode.compare("transform") == 0)
            transform_interaction(from, to, transfer_unit);
        else if (mode.compare("divergent") == 0)
            divergent_interaction(from, to, transfer_unit, ratio);
        else if (mode.compare("convergent") == 0)
            convergent_interaction(from, to, transfer_unit);
        else if (mode.compare("subduction") == 0)
            subduction_interaction(from, to, transfer_unit);
    }


    template <typename T>
    void TectonicDomain<T>::falloff_interaction(coordinate to, T transfer_unit) {
        value_map.increment_coordinate_value(to, get_transfer_unit(transfer_unit, -1.0));
    }


    template <typename T>
    void TectonicDomain<T>::transfer_interaction(coordinate from, coordinate to, T transfer_unit) {
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, -1.0));
        value_map.increment_coordinate_value(to, transfer_unit);
    }


    template <typename T>
    void TectonicDomain<T>::transform_interaction(coordinate from, coordinate to, T transfer_unit) {
        //placeholder for changing the ratios of intrusive/extrusive rock types
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, -1.0));
        value_map.increment_coordinate_value(to, transfer_unit);
    }


    template <typename T>
    void TectonicDomain<T>::divergent_interaction(coordinate from, coordinate to, T transfer_unit, float ratio) {
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, -1.0));
        value_map.increment_coordinate_value(to, transfer_unit);
        value_map.increment_coordinate_value(from, get_transfer_unit(create_new_unit(), ratio));
    }

    /*
    - the convergent coordinate will receive units from behind
    - give back fold_ratio * transfer_unit back to where it would come from
    */
    template <typename T>
    void TectonicDomain<T>::convergent_interaction(coordinate from, coordinate to, T transfer_unit) {
        coordinate reverse_neighbor{to.x-from.x*(-1), to.y-from.y*(-1)};
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, fold_ratio * -1.0));
        value_map.increment_coordinate_value(reverse_neighbor, get_transfer_unit(transfer_unit, fold_ratio));
    }


    template <typename T>
    void TectonicDomain<T>::subduction_interaction(coordinate from, coordinate to, T transfer_unit) {
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, -1.0 - subduction_ratio));
        value_map.increment_coordinate_value(to, get_transfer_unit(transfer_unit, subduction_ratio));
    }


    template <typename T>
    T TectonicDomain<T>::create_new_unit() {
        return base_unit;
    }


    template <typename T>
    void TectonicDomain<T>::increment_cycle_ticker() {
        cycle_ticker++;
        if (cycle_ticker % cycle_interval == 0)
            cycle_action();
    }


    template <typename T>
    void TectonicDomain<T>::cycle_action() {
        return;
    }


    //fully generates the standardized direction vector for a given plate
    template <typename T>
    fvector TectonicDomain<T>::generate_magma_current_vector(std::vector<coordinate> *plate) {
        fvector plate_vector = {0.0, 0.0};
        std::vector<coordinate> neighbors;
        for (auto it = plate->begin(); it != plate->end(); it++) {
            neighbors = value_map.get_adjacent_coordinates(*it, true, false);
            std::sort(neighbors.begin(), neighbors.end(), [this](coordinate a, coordinate b){return this->get_height(a) < this->get_height(b);});
            if (get_height(neighbors.at(0)) < get_height(*it))
                plate_vector += {neighbors.at(0).x - it->x, neighbors.at(0).y - it->y};
        }
        return value_map.standardize_vector(plate_vector);
    }
    

    template <typename T>
    float TectonicDomain<T>::get_height(coordinate c) {
        return {0,0};
    }
}