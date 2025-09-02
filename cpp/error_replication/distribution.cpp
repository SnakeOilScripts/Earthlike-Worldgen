#include <iostream>
#include <array>
#include <random>


int main() {
    std::random_device random_device;
    std::mt19937 generator(random_device());

    int nstars = 100;
    int nrolls = 100000;

    std::array<double,8> intervals {0, 1, 2, 3, 4, 5, 6, 7};
    //std::array<double,7> weights {7, 1, 1, 1, 1, 1, 1};
    std::array<double,7> weights {0.282, 0.0823, 0.0563, 0.0415, 0.0236, 0.0233, 0.0209};
    std::piecewise_constant_distribution<double> distribution (intervals.begin(),intervals.end(),weights.begin());
    int p[7] = {};

    for (int i=0; i<nrolls; i++) {
        int roll = distribution(generator);
        ++p[roll];
    }

    for (int i=0; i<7; ++i) {
    std::cout << i << "-" << i+1 << ": ";
    std::cout << std::string(p[i]*nstars/nrolls,'*') << std::endl;
  }

    return 0;
}