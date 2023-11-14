#include <sys/socket.h> // For socket functions
#include <netinet/in.h> // For sockaddr_in
#include <arpa/inet.h>  // For inet_pton
#include <unistd.h>     // For close
#include <string>     // For memset

extern bool in;


void unconnect(int);
bool quit(int);

bool gettingline(std::string&);
