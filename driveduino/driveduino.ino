// #include "MotorControl.h"
// #include "SerialComm.h"
void setup() {
  Serial.begin(9600);  // Set the baud rate to match the Raspberry Pi
}

void loop() {
  if (Serial.available() > 0) {
    int receivedData = Serial.parseInt();  // Read the integer from the serial port

    // Print the received data to the Serial Monitor
    Serial.print("Received Data: ");
    Serial.println(receivedData);
  }
}
