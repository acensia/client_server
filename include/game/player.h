#ifndef PLAYER_H
#define PLAYER_H

#include "game/game.h"
#include "connection/connection.h"


void enter(int sock, Map&);

void send_MSG(int sock);

#endif