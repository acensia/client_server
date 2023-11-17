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