#ifndef PLAYER_H
#define PLAYER_H

#include "game/game.h"
#include "connection/connection.h"


void enter(int, Map&, int&);

void send_MSG(int sock);

bool wait_turn(int);

#endif