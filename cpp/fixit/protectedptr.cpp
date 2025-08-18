#include <iostream>
#include <vector>

class A{
    protected:
        std::vector<int> v;
    public:
        A() {
            v = {3,4,5};
        }
        std::vector<int> *get_value() {
            return &v;
        }
};

int main() {
    A obj = A();
    std::vector<int> *v;
    v = obj.get_value();
    for (auto i:*v)
        std::cout << i << "\n";
    return 0;
}