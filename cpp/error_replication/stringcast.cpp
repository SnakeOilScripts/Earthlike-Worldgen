#include <iostream>
#include <string>

int main() {
    int i=50;
    std::string s, t;
    s = std::to_string(i);
    t = std::to_string(43);
    std::cout<<s<<" "<<s.size()<<"\n";
    s += t;
    std::cout<<s<<" "<<s.size()<<"\n";
    std::cout<<std::hash<std::string>(){s} <<"\n";
    return 0;
}