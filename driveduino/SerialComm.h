#ifndef SERIALCOMM_H
#define SERIALCOMM_H
#include "Arduino.h"
#include "constants.h"

void initializeComm(int baud);
int recvData();

#endif
