#include <iostream>

struct s {
    int i;
    int j;
};

int main() {
    s abc{2,3};
    auto h = std::hash<s>{}(abc);

    return 0;
}