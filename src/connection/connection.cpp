#include <iostream>
#include "connection/connection.h"

bool gettingline(std::string &str){
    // to check if any '\n' remains in cin
    if (std::cin.peek() == '\n') {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    std::getline(std::cin, str);
    std::cout<<str<<" entered\n";
    return true;
}


void unconnect(int sock){
    ssize_t bytes = send(sock, "_quit", 5, 0);
    if(bytes == -1){
        std::cerr<<"Failed to send data." << std::endl;
        return;
    }
    in = false;
}

bool quit(int sock){
    char k;
    std::cout << "Do you want to quit ? : Y / N" << std::endl;
    std::cin >> k;
    if(k == 'y' || k == 'Y'){
        unconnect(sock);
        return true;
    }
    if(k== 'n' || k == 'N'){
        return false;
    }
    std::cout << "Press right button" << std::endl;
    return quit(sock);
}