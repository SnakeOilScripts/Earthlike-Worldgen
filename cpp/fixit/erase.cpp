#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1,2,3,4,5};

    for (auto i:v)
        std::cout << i << " ";
    std::cout << "\n";

    for (auto it=v.begin(); it!=v.end(); it++) {
        while (*it  == 2 || *it == 3)
            v.erase(it);
    }

    for (auto i:v)
        std::cout << i << " ";
    std::cout << "\n";


    return 0;
}