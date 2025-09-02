#include <iostream>
#include <vector>
#include <algorithm>

class Test {
    public:
        Test() {

        }
        
        virtual int add(int a) {
            std::cout<<"processing: "<<a<<"+1\n";
            return a+1;
        }
        

        void sorting() {
            std::vector<int> v{4,10,3};
            std::sort(v.begin(), v.end(), [this](int a, int b){return add(a) < add(b);});


            for (auto i:v)
                std::cout<<i<<" ";
            std::cout<<"\n";
        }

        void thistest() {
            this->add(1);
            add(1);
        }
};

class Test2:public Test {
    public:

    virtual int add(int a) {
        std::cout<<"processing: "<<a<<"+2\n";
        return a+2;
    }
    /*
    void sorting() {
        std::vector<int> v{4,10,3};
            
            std::sort(v.begin(), v.end(), [this](int a, int b){return add(a) < add(b);});

            for (auto i:v)
                std::cout<<i<<" ";
            std::cout<<"\n";
    }
    */
};

int main() {
    Test2 t;
    //t.thistest();
    t.sorting();
    return 0;
}