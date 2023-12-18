#include "MotorControl.h"
#include "SerialComm.h"

// COMMAND MATRIX
// 1->STOP   | 6 ->FWD V2 | 11->DIAG NE V1 | 16->N/A |
// 2->FWD V1 | 7 ->REV V2 | 12->DIAG SE V1 | 17->N/A |
// 3->REV V1 | 8 ->RHT V2 | 13->DIAG SW V1 | 18->N/A |
// 4->RHT V1 | 9 ->LHT V2 | 14->DIAG NW V1 | 19->N/A |
// 5->LHT V1 | 10->N/A    | 15->N/A        | 20->N/A |

int commandDrive(int commandId){
  switch (commandId){
    case 1: stop(); break;
    case 2: forwardSlow(); break;
    case 3: reverseSlow(); break;
    case 4: rightSlow(); break;
    case 5: leftSlow(); break;
    case 6: forwardFast(); break;
    case 7: reverseFast(); break;
    case 8: rightFast(); break;
    case 9: leftFast(); break;
    case 10: stop(); break;
    case 11: stop(); break;
    case 12: stop(); break;
    case 13: stop(); break;
    case 14: stop(); break;
    case 15: stop(); break;
    case 16: stop(); break;
    case 17: stop(); break;
    case 18: stop(); break;
    case 19: stop(); break;
    case 20: stop(); break;
  default:
    Serial.println("Unknown Command!");
    break;
    return 1;
  }
};

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int receivedData = Serial.parseInt();
    Serial.print("Received Data: ");
    Serial.println(receivedData);
    commandDrive(receivedData);
  };  
}
