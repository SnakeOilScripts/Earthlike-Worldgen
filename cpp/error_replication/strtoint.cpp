#include <iostream>
#include <string>

int main() {
    std::string s = "hello";
    int r = 0;
    for (auto c:s) {
        r += c;
    }
    std::cout << r << "\n";
    return 0;
}