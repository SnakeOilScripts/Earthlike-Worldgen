
#ifndef _COORDINATE_H
#define _COORDINATE_H

namespace world_base {
    // redefining operators makes addition of coordinates and other classes possible
struct coordinate {
    int x;
    int y;
    friend coordinate operator+(coordinate a, const coordinate& b) {
        a.x += b.x;
        a.y += b.y;
        return a;
    }
    friend coordinate operator-(coordinate a, const coordinate& b) {
        a.x -= b.x;
        a.y -= b.y;
        return a;
    }
    coordinate& operator+=(const coordinate& a) {
        x += a.x;
        y += a.y;
        return *this;
    }
    coordinate& operator-=(const coordinate& a) {
        x -= a.x;
        y -= a.y;
        return *this;
    }
    bool operator==(const coordinate& a) {
        return (x == a.x && y ==  a.y);
    }
    friend bool operator<(coordinate a, const coordinate& b) {
        return (a.x+a.y < b.x+b.y);
    }
    
};

struct fvector {
    float x;
    float y;
    friend fvector operator+(fvector a, const fvector& b) {
        a.x += b.x;
        a.y += b.y;
        return a;
    }
    friend fvector operator-(fvector a, const fvector& b) {
        a.x -= b.x;
        a.y -= b.y;
        return a;
    }
    fvector& operator+=(const fvector& a) {
        x += a.x;
        y += a.y;
        return *this;
    }
    fvector& operator-=(const fvector& a) {
        x -= a.x;
        y -= a.y;
        return *this;
    }
    bool operator==(const fvector& a) {
        return (x == a.x && y ==  a.y);
    }
    friend bool operator<(fvector a, const fvector& b) {
        return (a.x+a.y < b.x+b.y);
    }
    
};

    fvector ctofv(coordinate c) {
        fvector v{static_cast<float>(c.x), static_cast<float>(c.y)};
        return v;
    }

}
#endif