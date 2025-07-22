
#include <vector>
#include <string>
#include <array>
#include <random>
#include <algorithm>
//#include <cmath>
#include "coordinate.hpp"
#include "TectonicDomain.hpp"

#ifndef _GEOLOGY_H_
#define _GEOLOGY_H_

namespace world_base {

    struct geodat{
        float felsic;
        float intermediate;
        float mafic;
        float ultramafic;
        float igneous;
        float sedimentary;
        float metamorphic;
        float carbonate;
        float pegmatite;
        float kimberlite;
        float porphyry;
        float skarn;
        float vms;
        float sedex;
        float mvt;

        friend geodat operator+(geodat a, const geodat& b) {
            a.felsic += b.felsic;
            a.intermediate += b.intermediate;
            a.mafic += b.mafic;
            a.ultramafic += b.ultramafic;
            a.igneous += b.igneous;
            a.sedimentary += b.sedimentary;
            a.metamorphic += b.metamorphic;
            a.carbonate += b.carbonate;
            a.pegmatite += b.pegmatite;
            a.kimberlite += b.kimberlite;
            a.porphyry += b.porphyry;
            a.skarn += b.skarn;
            a.vms += b.vms;
            a.sedex += b.sedex;
            a.mvt += b.mvt;
            return a;
        }

        geodat& operator+=(const geodat& a) {
            *this = *this + a;
            return *this;
        }

        friend geodat operator*(geodat a, float factor) {
            a.felsic *= factor;
            a.intermediate *= factor;
            a.mafic *= factor;
            a.ultramafic *= factor;
            a.igneous *= factor;
            a.sedimentary *= factor;
            a.metamorphic *= factor;
            a.carbonate *= factor;
            a.porphyry *= factor;
            a.skarn *= factor;
            a.vms *= factor;
            a.sedex *= factor;
            a.mvt *= factor;
            return a;
        }
    };

    class Geology: public TectonicDomain<geodat> {
        protected:
            float last_sea_level;
            float base_unit_size;
            std::vector<std::string> abundant_elements;
            std::array<double,7> abundances;
        public:
            Geology();
            Geology(coordinate d, float unit_size=100.0);
            std::string determine_rock_type();
            void apply_volcanism(coordinate c);
            void magmatic_deposition(coordinate c, geodat before, geodat after);
            void hydrothermal_deposition(coordinate c);
            geodat create_new_unit();
            geodat get_transfer_unit(geodat value, float ratio);
            void subduction_interaction(coordinate from, coordinate to, geodat transfer_unit);
            void apply_rock_cycle();
            void add_carbonate();
            void cycle_action();

            float get_sea_level(float base_water_factor=20);
            float get_height(coordinate c);
            void expand_dimensions_transitional_gaussian(int factor);
    };
}

#endif