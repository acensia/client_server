#include <iostream>
#include "connection/connection.h"
#include "game/player.h"

bool in = true;
std::string name;

int main () {

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        std::cerr << "Can't create socket" << std::endl;
        return 1;
    }

    struct sockaddr_in serverAddress;

    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(3000); // Replace with your server's port
    inet_pton(AF_INET, "127.0.0.1", &serverAddress.sin_addr); // Replace with your server's IP
        // 은진 address?? != port?


    if (connect(sock, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) == -1) {
        std::cerr << "Can't connect to the server" << std::endl;
        return 1;
    }

    int MS;
    recv(sock, &MS, 8, 0);
    std::cout<<ntohl(MS)<<std::endl;
    Map curr_map(ntohl(MS));
    std::cout<<"What's your name? ";
    do {
        std::cout<<"Write in 20 letters.\n";
        gettingline(name);
    } while(name.length() > 20);
    ssize_t bytes = send(sock, name.c_str(), name.length(), 0);
    if(bytes == -1){
        std::cerr<<"Failed to send name." << std::endl;
        return 1;
    }

    enter(sock, curr_map);
    std::cout<<"Communication starts!\n";
    char buffer[81];
    recv(sock, buffer, 81, 0);
    for(int i=0; i<9; ++i){
        for(int j=0; j<9; ++j) std::cout<<buffer[i*9 + j]<<" ";
        std::cout<<'\n';
    }
    in = true;
    do{
        send_MSG(sock);
    }while(in);

    close(sock); // For Unix/Linux
    // For Windows, use: closesocket(sock);


    return 0;
}