#include <iostream>
#include "game/game.h"

Map::Map(){
    map_size = -1;
}
Map::Map(int s){
    map_size = s;
    MAP = std::vector<std::vector<int>>(s, std::vector<int>(s));
}
Map::~Map(){

}

void Map::setMapSize(int s){
    MAP = std::vector<std::vector<int>>(s, std::vector<int>(s));
}

int Map::getMapSize(){
    return map_size;
}