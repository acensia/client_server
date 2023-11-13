#include <iostream>
#include <sys/socket.h> // For socket functions
#include <netinet/in.h> // For sockaddr_in
#include <arpa/inet.h>  // For inet_pton
#include <unistd.h>     // For close
#include <string>     // For memset

bool quit(int);
bool in= true;

void unconnect(int sock){
    ssize_t bytes = send(sock, "_quit", 5, 0);
    if(bytes == -1){
        std::cerr<<"Failed to send data." << std::endl;
        return;
    }
    in = false;
}

void send_MSG(int sock){
    std::string msg;
    std::cout << "Write your MSG"<<std::endl;
    std::getline(std::cin, msg);
    if(msg == "_quit") {
        quit(sock);
        return;
    }
    
    ssize_t bytes = send(sock, msg.c_str(), msg.length(), 0);
    if(bytes == -1){
        std::cerr<<"Failed to send data." << std::endl;
        return;
    }

    char buffer[1024] = {0};
    recv(sock, buffer, 1024, 0);
    std::cout << "Server: " << buffer << std::endl;

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

    const char* message = "Hello, Server!";
    send(sock, message, strlen(message), 0);

    char buffer[1024] = {0};
    recv(sock, buffer, 1024, 0);
    std::cout << "Server: " << buffer << std::endl;

    in = true;
    do{
        send_MSG(sock);
    }while(in);

    close(sock); // For Unix/Linux
    // For Windows, use: closesocket(sock);


    return 0;
}