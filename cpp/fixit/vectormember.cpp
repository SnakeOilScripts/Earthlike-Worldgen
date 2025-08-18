#include <iostream>
#include <vector>

struct s{
    int v; 
};

class Test2{
    public:
        s attrib;
        Test2() {

        }
        
        Test2(s init) {
            attrib = init;
        }

        s get_value() {
            return attrib;
        }
};

class Test{
    //protected:
        //std::vector<s> v;
    public:
        std::vector<Test2> v;
        Test() {

        }

        Test(std::vector<Test2>init) {
            v = init;
        }


        void add_value(s new_s) {
            Test2 t(new_s);
            v.push_back(t);
        }

        std::vector<Test2*> get_all() {
            std::vector<Test2*> ret;
            for (auto it=v.begin(); it!=v.end(); ++it) {
                Test2 *ptr = &(*it);
                std::cout<<"inside function "<<ptr->get_value().v<<"\n";
                ret.push_back(ptr);
            }
            return ret;
        }

        s get_value(int at) {
            std::vector<Test2*> all = get_all();
            Test2 *p = all.at(at);
            return p->get_value();
        }
};

int main() {
    Test mobj;
    mobj.add_value({1});
    s res;
    res = mobj.get_value(0);
    std::cout<<res.v<<"\n";
}