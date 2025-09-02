#include <iostream>
#include <vector>
#include <algorithm>

std::vector<int> getv() {
    std::vector<int>v{1,2,3};
    return v;    
}

int main() {
    std::vector<int> v = getv();
    bool found = std::find(v.begin(), v.end(), 3) != v.end();
    std::cout << found << "\n";
    return 0;
}