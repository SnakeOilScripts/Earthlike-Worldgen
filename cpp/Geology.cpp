#include "Geology.hpp"

namespace world_base {

    Geology::Geology() {

    }


    Geology::Geology(coordinate d, float unit_size) {
        abundances = {0.282, 0.0823, 0.0563, 0.0415, 0.0236, 0.0233, 0.0209};
        dimensions = d;
        base_unit_size = unit_size;
        geodat base_unit = create_new_unit();
        last_sea_level = 0;
        value_map = UpdateMap(dimensions, base_unit);
    }


    std::string Geology::determine_rock_type() {
        std::random_device random_device;
        std::mt19937 generator(random_device());
        //0-1:Si 1-2:Al 2-3:Fe 3-4:Ca 4-5:Na 5-6:Mg 6-7:K
        std::array<double,8> intervals{0,1,2,3,4,5,6,7};
        std::piecewise_constant_distribution<double> distribution(intervals.begin(),intervals.end(),abundances.begin());
        int magma_contents[100] = {};
        for (int i=0; i<100; i++) {
            int element = distribution(generator);
            ++magma_contents[element];
        }
        if (magma_contents[0] >= 65)
            return "felsic";
        else if (magma_contents[0] >= 55)
            return "intermediate";
        else if (magma_contents[0] >= 45)
            return "mafic";
        else
            return "ultramafic";
    }


    float Geology::get_height(coordinate c) {
        geodat value = value_map.get_coordinate_value(c);
        return value.igneous + value.metamorphic + value.sedimentary;
    }


    geodat Geology::create_new_unit() {
        geodat unit = {};
        std::string rock_type = determine_rock_type();
        if (rock_type.compare("felsic") == 0)
            unit.felsic += base_unit_size;
        else if (rock_type.compare("intermediate") == 0)
            unit.intermediate += base_unit_size;
        else if (rock_type.compare("mafic") == 0)
            unit.mafic += base_unit_size;
        else
            unit.ultramafic += base_unit_size;
        unit.igneous += base_unit_size;
        return unit;
    }


    geodat Geology::get_transfer_unit(geodat value, float ratio) {
        return value * ratio;
    }


    void Geology::apply_volcanism(coordinate c) {
        for (int i=0; i<volcanism_potency; i++) {
            value_map.increment_coordinate_value(c, create_new_unit());
        }
    }


    void Geology::magmatic_deposition(coordinate c, geodat before, geodat after) {
        geodat unit = {};
        unit.kimberlite = after.ultramafic - before.ultramafic;
        unit.pegmatite = after.felsic - before.felsic;
        value_map.increment_coordinate_value(c, unit);
    }


    void Geology::hydrothermal_deposition(coordinate c) {
        geodat value = value_map.get_coordinate_value(c);
        float height = get_height(c);
        geodat ore = {};
        if (height > last_sea_level) {
            ore.porphyry = base_unit_size * ((value.felsic + value.intermediate) / height);
            ore.skarn = base_unit_size * (value.carbonate / height);
        } else {
            ore.vms = base_unit_size * ((value.igneous + value.metamorphic) / height);
            ore.sedex = base_unit_size * (value.sedimentary / height);
        }
        value_map.increment_coordinate_value(c, ore);
    }


    void Geology::subduction_interaction(coordinate from, coordinate to, geodat transfer_unit) {
        value_map.increment_coordinate_value(from, get_transfer_unit(transfer_unit, -1.0 - subduction_ratio));
        value_map.increment_coordinate_value(to, get_transfer_unit(transfer_unit, subduction_ratio));
        geodat metamorphic_transfer = {};
        metamorphic_transfer.sedimentary = -1*transfer_unit.sedimentary;
        metamorphic_transfer.metamorphic = transfer_unit.sedimentary;
        value_map.increment_coordinate_value(to, get_transfer_unit(metamorphic_transfer, subduction_ratio));
    }


    void Geology::apply_rock_cycle() {
        std::vector<coordinate> all = value_map.get_all_coordinates();
        geodat value, cycle;
        for (auto it=all.begin(); it!=all.end(); ++it) {
            value = value_map.get_coordinate_value(*it);
            if (value.igneous >= value.sedimentary && value.igneous >= value.metamorphic) {
                cycle = {};
                cycle.igneous = -1 * std::min(base_unit_size, cycle.igneous);
                cycle.sedimentary = std::min(base_unit_size, cycle.igneous);
                value_map.increment_coordinate_value(*it, cycle);
            } else if (value.sedimentary > value.igneous && value.sedimentary >= value.metamorphic ) {
                cycle = {};
                cycle.sedimentary = -1 * std::min(base_unit_size, cycle.sedimentary);
                cycle.metamorphic = std::min(base_unit_size, cycle.sedimentary);
                value_map.increment_coordinate_value(*it, cycle);
            } else {
                cycle = {};
                cycle.metamorphic = -1 * std::min(base_unit_size, cycle.metamorphic);
                cycle.igneous = std::min(base_unit_size, cycle.metamorphic);
                value_map.increment_coordinate_value(*it, cycle);
            }
        }
    }


    void Geology::add_carbonate() {
        std::vector<coordinate> all = value_map.get_all_coordinates();
        geodat c = {};
        c.sedimentary = 1;
        c.carbonate = 1;
        for (auto it=all.begin(); it!=all.end(); ++it) {
            if (get_height(*it) < last_sea_level)
                value_map.increment_coordinate_value(*it, c);
        }
    }


    void Geology::cycle_action() {
        last_sea_level = get_sea_level();
        add_carbonate();
        apply_rock_cycle();
    }


    float Geology::get_sea_level(float base_water_factor) {
        std::vector<coordinate> all_coordinates = value_map.get_all_coordinates();
        std::vector<float> all_heights;
        int i,j;
        float sum_of_differences;
        for (auto it=all_coordinates.begin(); it!=all_coordinates.end(); ++it)
            all_heights.push_back(get_height(*it));
        
        std::sort(all_heights.begin(), all_heights.end(), [](float a, float b){return a<b;});
        float water_units = all_heights.size() * base_unit_size * base_water_factor;
        j = static_cast<int>((all_heights.size()-1)/2);
        i = j;
        while (j != 0) {
            sum_of_differences = 0;
            for (int z=0; z<i; z++)
                sum_of_differences += all_heights.at(i) - all_heights.at(z);
            j = static_cast<int>(j/2);
            if (sum_of_differences <= water_units)
                i += j;
            else
                i -= j;
        }
        return all_heights.at(i);
    }


    void Geology::expand_dimensions_transitional_gaussian(int factor) {
        value_map.transitional_gaussian_dimensions_expansion(factor, {});
    }

    geodat Geology::get_coordinate_value(coordinate c) {
        return value_map.get_coordinate_value(c);
    }


    void Geology::print_height_map() {
        coordinate dim = value_map.get_dimensions();
        for (int y=0; y<dim.y; y++) {
            for (int x=0; x<dim.x; x++) {
                std::cout<<"["<<get_height({x,y})<<"]\t";
            }
            std::cout<<"\n";
        }
    }


    float Geology::get_sea_coverage() {
        float sea_level = get_sea_level();
        int coverage_count = 0;
        for (auto c: value_map.get_all_coordinates()) {
            if (get_height(c) > sea_level)
                coverage_count++;
        }
        return (static_cast<float>(coverage_count) / static_cast<float>(value_map.get_all_coordinates().size()));
    }

}