#include <iostream>
#include <vector>
#include <algorithm>

class CC {
    private:
        int n;
    public:
        CC() {
            n = 3;
        }

        void func() {
            std::cout << n << "\n";
        }

        void func2() {
            std::vector<int> v{1,2};
            std::sort(v.begin(), v.end(), [this](int a, int b){this->func(); return a < b;});
        }
};

int main() {
    CC c1;
    CC c2;
    std::vector<CC> v{CC(), CC()};
    for (auto it=v.begin(); it!=v.end(); it++) {
        it->func2();
    }
    return 0;
}