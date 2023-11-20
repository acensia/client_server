#include <vector>


class Map{
private:
    int map_size;
    std::vector<std::vector<int>> MAP;
public:
    Map();
    Map(int);
    ~Map();
    void setMapSize(int);
    int getMapSize();
};

class Pan{
private:
    std::string PAN;
    char self;
    char opp;
public:
    Pan();
    Pan(std::string);
    ~Pan();
    bool PutDol(int, bool);
    void showPan();
    void setPan(std::string);
    void setColor(int);
};