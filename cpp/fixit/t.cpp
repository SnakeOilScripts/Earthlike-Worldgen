#include "t.hpp"

namespace aaa {

template<typename T>
ObjectMap<T>::ObjectMap() {
    id = 3;
}

template<typename T>
int ObjectMap<T>::get_id() {
    return id;
}

}
