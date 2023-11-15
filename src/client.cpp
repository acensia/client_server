#include <iostream>
#include <sys/socket.h> // For socket functions
#include <netinet/in.h> // For sockaddr_in
#include <arpa/inet.h>  // For inet_pton
#include <unistd.h>     // For close
#include <string>     // For memset
#include "connection/connection.h"

bool in = true;
std::string name;

bool check3000(int a, int b){
    if(a+b != 3000){
        std::cout<<"Enter the correct value!\n";
    }
    return (a+b != 3000);
}

void enter(int sock){
    int x, y, atk, df, pos;
    std::cout<<"Set your location! Map size is 10\n";
    std::cout<<"X : ";    std::cin>>x;
    std::cout<<"Y : ";    std::cin>>y;
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
    send(sock, info, sizeof(info), 0);

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


    if (connect(sock, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) == -1) {
        std::cerr << "Can't connect to the server" << std::endl;
        return 1;
    }
    
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

    enter(sock);
    std::cout<<"Communication starts!\n";
    in = true;
    do{
        send_MSG(sock);
    }while(in);

    close(sock); // For Unix/Linux
    // For Windows, use: closesocket(sock);


    return 0;
}