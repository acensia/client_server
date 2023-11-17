#include <iostream>
#include "game/player.h"

bool check3000(int a, int b){
    if(a+b != 3000 || a<0 || b<0){
        std::cout<<"Enter the correct value!\n";
    }
    return (a+b != 3000 || a<0 || b<0);
}

bool checkLoc(int x, int y, int ms){
    if((x < 0 || x >= ms) || (y < 0 || y >= ms)){
        std::cout<<"Write the correct location!\n";
    }
    return (x < 0 || x >= ms) || (y < 0 || y >= ms);
}



void enter(int sock, Map& curr_map){
    int x, y, atk, df, pos;
    std::cout<<"Set your location! Map size is "<<curr_map.getMapSize()<<std::endl;
    do {
    std::cout<<"X : ";    std::cin>>x;
    std::cout<<"Y : ";    std::cin>>y;
    } while(checkLoc(x, y, curr_map.getMapSize()));
    std::cout<<"Set your stat! Sum of stat should be 3000\n";
    do{
        std::cout<<"ATK : "; std::cin>>atk;
        std::cout<<"DEF : "; std::cin>>df;
    }while(check3000(atk, df));
    std::cout<<"Set your state! Attack mode : 0, Defend mode : 1\n";
    do{
    std::cout<<"Pose : "; std::cin>>pos;
    }while(pos != 1 && pos != 0);
    const int info[] = {x, y, atk, df, pos};
    send(sock, info, sizeof(info), 0); /// Send your state

    char buffer[64];
    std::string receivedMessage;
    int bytesReceived = 0;

    bytesReceived = recv(sock, buffer, 64, 0);

    if (bytesReceived == -1) {
        // Handle errors
    }
    receivedMessage.append(buffer, bytesReceived);
    std::cout<<receivedMessage<<std::endl;
    return;
}

void send_MSG(int sock){
    std::string msg;
    std::cout << "Write your MSG"<<std::endl;
    gettingline(msg);
    if(msg == "_quit") {
        quit(sock);
        return;
    }
    
    ssize_t bytes = send(sock, msg.c_str(), msg.length(), 0);
    if(bytes == -1){
        std::cerr<<"Failed to send data." << std::endl;
        return;
    }
    std::cout<<"Your message \""<<msg<<"\" has sent"<<std::endl;
    char buffer[1024] = {0};
    recv(sock, buffer, 1024, 0);
    std::cout << "Server: " << buffer << std::endl;
}
