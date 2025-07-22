#include <iostream>

struct test {
    int elem1;
    int elem2;

    friend test operator+(test a, const test& b) {
        a.elem1 += b.elem2;
        a.elem2 += b.elem2;
        return a;
    }

    test& operator+=(const test& a) {
        *this = *this + a;
        return *this;
    }

    friend test operator*(test a, const int factor) {
        a.elem1 *= factor;
        a.elem2 *= factor;
        return a;
    }
};

int main() {
    test a{1,2};
    test b = a + test{2,2};
    std::cout << b.elem1 << " " << b.elem2 << "\n";
    b += test{3,3};
    std::cout << b.elem1 << " " << b.elem2 << "\n";
    test c = a + b;
    std::cout << c.elem1 << " " << c.elem2 << "\n";
    test d = a * 4;
    std::cout << d.elem1 << " " << d.elem2 << "\n";
    return 0;
}