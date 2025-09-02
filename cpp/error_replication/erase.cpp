#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1,2,3,4,5};

    for (auto i:v)
        std::cout << i << " ";
    std::cout << "\n";

    /*
    for (auto it=v.begin(); it!=v.end(); ++it) {
        while (*it  == 2 || *it == 4)   //throws a segmentation fault when the last item is erased
            v.erase(it);
    }
    */
    /*
    auto it = v.end()-1;
    while (it>=v.begin()) {
        if (*it == 1 || *it == 5)
            v.erase(it);
        it--;
    }
    */
    for (auto it=v.end(); it>=v.begin(); it--) {
        if (*it == 4 || *it == 5)
            v.erase(it);    //invalidates the vector when all elements are removed - pop_back is the safe alternative
    }

    for (auto i:v)
        std::cout << i << " ";
    std::cout << "\n";


    return 0;
}