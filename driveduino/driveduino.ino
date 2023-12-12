#include "MotorControl.h"
#include "SerialComm.h"
void setup(){
  initializeComm(9600);
};

void loop(){
  recvData();
};
