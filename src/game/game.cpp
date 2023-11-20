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

Pan::Pan(){
    PAN = "";
}

Pan::Pan(std::string p){
    PAN = p;
}

bool Pan::PutDol(int code, bool c){
    if(PAN[code] != '+'){
        std::cout<<"Wrong loc"<<std::endl;
        return false;
    }
    if(c) PAN[code] = self;
    else PAN[code] = opp;
    this->showPan();
    return true;
}

void Pan::setPan(std::string s){
    PAN = s;
}

void Pan::setColor(int s){
    if(s==0) {
        self = '*';
        opp = 'o';
    }
    else {
        self = 'o';
        opp = '*';
    }
}

void Pan::showPan(){
    for(int i=0; i<9; ++i){
        for(int j=0; j<9; ++j){
            std::cout<<PAN[i*9+j]<<" ";
        }std::cout<<std::endl;
    }
}

Pan::~Pan(){

}