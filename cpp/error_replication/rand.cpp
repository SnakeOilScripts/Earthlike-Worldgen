#include <iostream>
#include <random>

int main() {
    std::cout << ((float)rand())/RAND_MAX << "\n";
    return 0;
}