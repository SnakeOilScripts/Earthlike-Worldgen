#include <iostream>
#include <vector>
#include <cmath>
#include <set>
#include <algorithm>

// redefining operators makes addition of coordinates and other classes possible
struct coordinate {
    int x;
    int y;
    friend coordinate operator+(coordinate a, const coordinate& b) {
        a.x += b.x;
        a.y += b.y;
        return a;
    }
    friend coordinate operator-(coordinate a, const coordinate& b) {
        a.x -= b.x;
        a.y -= b.y;
        return a;
    }
    coordinate& operator+=(const coordinate& a) {
        x += a.x;
        y += a.y;
        return *this;
    }
    coordinate& operator-=(const coordinate& a) {
        x -= a.x;
        y -= a.y;
        return *this;
    }
};

void print_coordinate(coordinate c) {
    std::cout << "\t{" << c.x << "," << c.y << "}\n";
}

namespace world_base {

template <typename T>
class ObjectMap {
    private:
        //simplifying dimensions by leaving (0,0) implicit
        coordinate dimensions;
    public:
        std::vector<std::vector<T>> map;
        
        ObjectMap() {
            
        }

        ObjectMap (coordinate d, T base_object) {
            dimensions = d;
            map = create_coordinates(dimensions, base_object);

        }


        std::vector<std::vector<T>> create_coordinates(coordinate dimensions, T base_object) {
            std::vector<std::vector<T>> m;
            for (int x=0; x<dimensions.x; x++) {
                std::vector<T> v;
                m.push_back(v);
                for (int y=0; y<dimensions.y; y++) {
                    m.at(x).push_back(base_object);
                }
            }
            return m;
        }


        std::vector<coordinate> get_all_coordinates() {
            std::vector<coordinate> v;
            for (int x=0; x<dimensions.x; x++) {
                for (int y=0; y<dimensions.y; y++) {
                    coordinate c = {x,y};
                    v.push_back(c);
                }
            }
            return v;
        }


        int coordinate_outside_dimensions(coordinate p) {
            if (p.x < 0 || p.y < 0)
                return 1;
            else if (p.x >= dimensions.x || p.y >= dimensions.y)
                return 1;
            else
                return 0;
        }


        std::vector<coordinate> get_adjacent_coordinates(coordinate p, bool within_dimensions=false, bool nondiagonal=false) {
            std::vector<coordinate> v;
            for (int x=p.x-1; x<=p.x+1; x++) {
                for (int y=p.y-1; y<=p.y+1; y++) {
                    coordinate c = {x,y};
                    if (within_dimensions && coordinate_outside_dimensions(c))
                        continue;
                    if (nondiagonal && (x != p.x && y != p.y))
                        continue;
                    if (x == 0 && y == 0)
                        continue;
                    v.push_back(c);
                }
            }
            return v;
        }

        // putting it into a pointer to allow for error codes
        T get_coordinate_value(coordinate p) {
            return map.at(p.x).at(p.y);
        }


        int set_coordinate_value(coordinate p, T value) {
            if (coordinate_outside_dimensions(p) == true) {
                return -1;
            }
            map.at(p.x).at(p.y) = value;
            return 0;
        }


        float get_distance(coordinate p1, coordinate p2) {
            return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
        }


        float base_vector_angle(coordinate v1, coordinate v2) {
            coordinate base = {0,0};
            float d1 = get_distance(base, v1);
            float d2 = get_distance(base, v2);
            float dot_product = v1.x * v2.x + v1.y * v2.y;
            // improvising a rounding to 2nd decimal
            float angle = std::round(std::acos((dot_product / (d1*d2)) * std::pow(10, 2))) * std::pow(10, 2);
            return angle;
        }


        coordinate resize_vector(coordinate v, float length) {
            coordinate b = {0,0};
            if (get_distance(b, v) == 0)
                return b;
            coordinate r = {v.x * (length / get_distance(b, v)), v.y * (length / get_distance(b, v))};
            return r;
        }


        coordinate standardize_vector(coordinate v) {
            coordinate ret;
            if (v.x == 0 and v.y != 0) {
                ret.y = v.y/std::abs(v.y);
            }
            else if (v.x != 0 and v.y == 0) {
                ret.x = v.x/std::abs(v.x);
            }
            else if (v.x == 0 and v.y == 0) {
                
            }
            else if (std::abs(v.x) > std::abs(v.y)) {
                ret.x = v.x/std::abs(v.x);
                ret.y = v.y/std::abs(v.y);
            }
            else {
                ret.x = v.x/std::abs(v.y);
                ret.y = v.y/std::abs(v.y);
            }
            return ret;
        }


        coordinate get_expanded_dimensions(int factor) {
            coordinate d = dimensions;
            d.x *= factor;
            d.y *= factor;
            return d;
        }


};

template <typename T>
class UpdateMap {
    private:
        ObjectMap<T> map;
        ObjectMap<T> update;
    public:
        coordinate dimensions;
        coordinate update_dimensions;

        UpdateMap(coordinate d, T base_object) {
            dimensions = d;
            update_dimensions = d;
            map = create_map(d, base_object);
            update = create_map(d, base_object);
        }


        ObjectMap<T> create_map(coordinate d, T base_object) {
            ObjectMap<T> m(d, base_object);
            return m;
        }

        // requires the base_object to have a + and += operator defined!!! especially for new structs
        void increment_coordinate_value(coordinate c, T value) {
            T inc;
            if (!update.coordinate_outside_dimensions(c)) {
                inc = update.get_coordinate_value(c);
                update.set_coordinate_value(c, inc + value);
            }
        }

        void apply_changes() {
            map = update;
            dimensions = update_dimensions;
        }

        T get_coordinate_value(coordinate c) {
            return map.get_coordinate_value(c);
        }

};


class SetMap: ObjectMap<std::set<int>> {
    public:

        using ObjectMap::ObjectMap;


        int add_coordinate_value(coordinate c, int value) {
            if (coordinate_outside_dimensions(c))
                return -1;
            map.at(c.x).at(c.y).insert(value);
            return 0;
        }


        int update_coordinate_value(coordinate c, std::set<int> value) {
            if (coordinate_outside_dimensions(c))
                return -1;
            map.at(c.x).at(c.y).merge(value);
            return 0;
        }


        int remove_coordinate_value(coordinate c, int value) {
            if (coordinate_outside_dimensions(c))
                return -1;
            map.at(c.x).at(c.y).erase(value);
            return 0;
        }

        
        std::vector<coordinate> get_neighbors_containing_value(coordinate c, int value) {
            std::vector<coordinate> v;
            std::vector<coordinate> ret;
            if (coordinate_outside_dimensions(c))
                return ret;
            v = get_adjacent_coordinates(c, true);
            std::cout<<"___\n";
            for (auto it = v.begin(); it != v.end(); ++it) {
                std::set<int> current_set = map.at((*it).x).at((*it).y);
                if (current_set.find(value) != current_set.end())
                    ret.push_back(*it);
            }
            return ret;
        }


        std::vector<coordinate> get_all_coordinates_containing_value(int value) {
            std::vector<coordinate> ret;
            std::vector<coordinate> all;

            all = get_all_coordinates();
            for (auto element: all) {
                std::set<int> current_set = map.at(element.x).at(element.y);
                if (current_set.find(value) != current_set.end())
                    ret.push_back(element);
            }
            return ret;
        }
        

};



} // end of namespace world_base


int main() {
    std::set<int> empty;
    world_base::SetMap smap({2,2}, empty);

    std::set<int> s1{3,4};

    smap.add_coordinate_value({0,0}, 1);
    smap.update_coordinate_value({0,1}, s1);
    smap.add_coordinate_value({1,0}, 1);
    smap.update_coordinate_value({1,1}, s1);

    std::vector<coordinate> v1 = smap.get_neighbors_containing_value({0,0}, 2);
    for (auto e: v1) {
        print_coordinate(e);
    }

    return 0;
}