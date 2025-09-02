#include "t.hpp"
#include "t.cpp"
#include <iostream>

int main() {
    aaa::ObjectMap<int> m;
    std::cout<<m.get_id()<<"\n";
    return 0;
}