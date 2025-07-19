#include <iostream>
#include <vector>
#include <cmath>
#include <set>
#include <algorithm>



namespace world_base {

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
    bool operator==(const coordinate& a) {
        return (x == a.x && y ==  a.y);
    }
    friend bool operator<(coordinate a, const coordinate& b) {
        return (a.x+a.y < b.x+b.y);
    }
    
};

void print_coordinate(coordinate c) {
    std::cout << "\t{" << c.x << "," << c.y << "}\n";
}



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


class SetMap: public ObjectMap<std::set<int>> {
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
