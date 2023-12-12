#include "SerialComm.h"

void initializeComm(int baud) {
  Serial.begin(baud);
}

int recvData() {
  // Read data from serial port and return it (modify as needed)
  if (Serial.available() > 0) {
    return Serial.read();
  }
  return -1; // Return -1 if no data is available
}
