#include <iostream>
#include <set>
#include <algorithm>

int main() {
    std::set<int> s{1,2,3};
    auto m = std::min_element(s.begin(), s.end());
    std::cout << *m << "\n";
    return 0;
}