#ifndef PLAYER_H
#define PLAYER_H

#include "game/game.h"
#include "connection/connection.h"


void enter(int, Map&, int&, Pan&);

void send_MSG(int sock, Pan&);

bool wait_turn(int, Pan&);

#endif